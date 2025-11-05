"""Simplified FastAPI server for Healthcare Decision Support System."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from agent.crew import answer_question
from agent.session_manager import session_manager
from dotenv import load_dotenv
from typing import Optional
import uuid
from datetime import datetime

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


class QueryModel(BaseModel):
    user_query: str
    session_id: Optional[str] = None

class SessionClearModel(BaseModel):
    session_id: str


@app.post("/ask-reception")
async def ask_reception(data: QueryModel):
    """Process user query using CrewAI with session memory."""
    try:
        # Get or create session
        session_id = data.session_id or str(uuid.uuid4())
        session_data = session_manager.get_session(session_id)
        
        # Extract user info and add message to history
        session_manager.extract_user_info(session_id, data.user_query)
        session_manager.add_message(session_id, 'user', data.user_query)
        
        # Get user info
        user_name = session_manager.get_user_info(session_id, 'name')
        user_role = session_manager.get_user_info(session_id, 'role')
        preferred_hospital = session_manager.get_user_info(session_id, 'preferred_hospital')
        
        # Build query with context
        enhanced_query = data.user_query
        if user_name:
            enhanced_query = f"{data.user_query}\n\n[User's name is {user_name}]"
        
        print(f"\n=== Processing Query ===")
        print(f"Session: {session_id}")
        print(f"Query: {data.user_query}")
        print(f"User: {user_name or 'Anonymous'}")
        print(f"=======================\n")
        
        # Let the LLM handle everything
        result = answer_question(session_id, enhanced_query)
        
        # Add response to history
        session_manager.add_message(session_id, 'assistant', result['answer'])
        
        return {
            "response": result['answer'],
            "session_id": session_id,
            "user_info": {
                "name": user_name,
                "role": user_role,
                "preferred_hospital": preferred_hospital
            }
        }
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            "response": f"Error processing query: {str(e)}", 
            "session_id": data.session_id
        }


@app.get("/")
def home():
    return FileResponse("static/index.html")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/new-session")
async def create_new_session():
    """Create a new conversation session."""
    session_id = session_manager.create_session()
    return {"session_id": session_id}


@app.get("/session/{session_id}")
async def get_session_info(session_id: str):
    """Get session information."""
    session = session_manager.get_session(session_id)
    if session:
        return {
            "session_id": session_id,
            "user_info": session['user_info'],
            "created_at": session['created_at'],
            "last_activity": session['last_activity'],
            "message_count": len(session['conversation_history'])
        }
    return {"error": "Session not found"}


@app.get("/session/{session_id}/history")
async def get_session_history(session_id: str):
    """Get conversation history."""
    session = session_manager.get_session(session_id)
    if session:
        return {"history": session['conversation_history']}
    return {"error": "Session not found"}


@app.post("/clear-session")
async def clear_specific_session(data: SessionClearModel):
    """Clear a specific session."""
    session_id = data.session_id
    if session_id in session_manager.sessions:
        session_manager.sessions[session_id] = {
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'user_info': {},
            'conversation_history': [],
            'preferences': {},
            'context': {}
        }
        return {"message": f"Session {session_id} cleared successfully"}
    return {"message": f"Session {session_id} not found"}


if __name__ == "__main__":
    print("=" * 60)
    print("Healthcare Decision Support System")
    print("=" * 60)
    print("\nAPI running at: http://localhost:8001")
    print("API Documentation: http://localhost:8001/docs")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)