"""FastAPI server for Hospital Reception Assistant."""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import time
from agent.agent import root_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types
from google.adk.agents import CallbackContext
import uuid

# -------------------------
# FastAPI Setup
# -------------------------
app = FastAPI()

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize session service and runner
APP_NAME = "hospital_reception"
session_service = InMemorySessionService()

# MUST provide both app_name AND agent
runner = Runner(
    app_name=APP_NAME,
    agent=root_agent,
    session_service=session_service
)

class QueryModel(BaseModel):
    user_query: str
    session_id: str = None

class FeedbackModel(BaseModel):
    recommendation: str
    feedback: str  # "like" or "dislike"
    session_id: str = None

# Global session management
USER_ID = "api_user"
DEFAULT_SESSION_ID = "persistent_session"

# Global session tracking
created_sessions = set()

# --- Preference Learning Functions ---
def like_recommendation(context, recommendation):
    """Add a recommendation to liked items"""
    liked = context.state.get('user:liked_recommendations', [])
    liked.append({
        'recommendation': recommendation,
        'timestamp': time.time()
    })
    context.state['user:liked_recommendations'] = liked

def dislike_recommendation(context, recommendation):
    """Add a recommendation to disliked items"""
    disliked = context.state.get('user:disliked_recommendations', [])
    disliked.append({
        'recommendation': recommendation,
        'timestamp': time.time()
    })
    context.state['user:disliked_recommendations'] = disliked

def get_user_preferences(context):
    """Get user preferences for agent personalization"""
    liked = context.state.get('user:liked_recommendations', [])
    disliked = context.state.get('user:disliked_recommendations', [])
    return {
        'liked_count': len(liked),
        'disliked_count': len(disliked),
        'recent_likes': [item['recommendation'] for item in liked[-3:]],
        'recent_dislikes': [item['recommendation'] for item in disliked[-3:]]
    }

@app.post("/ask-reception")
async def ask_reception(data: QueryModel):
    # Use provided session_id or default persistent session
    session_id = data.session_id or DEFAULT_SESSION_ID
    
    # Create session only if we haven't created it before
    if session_id not in created_sessions:
        try:
            await session_service.create_session(
                app_name=APP_NAME,
                user_id=USER_ID,
                session_id=session_id,
                state={
                    "user:liked_recommendations": [],
                    "user:disliked_recommendations": [],
                    "user:interaction_count": 0
                }
            )
            created_sessions.add(session_id)
        except Exception as e:
            # Session might already exist, that's okay
            created_sessions.add(session_id)
    
    # Prepare the user message
    content = types.Content(
        role='user',
        parts=[types.Part(text=data.user_query)]
    )
    
    # Run the agent and collect the final response
    final_response = "No response received."
    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=session_id,
        new_message=content
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break
    
    return {"response": final_response, "session_id": session_id}

@app.get("/")
def home():
    return FileResponse("static/index.html")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/new-session")
async def create_new_session():
    """Create a new session for the user"""
    new_session_id = str(uuid.uuid4())
    
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=new_session_id
        )
        created_sessions.add(new_session_id)
    except Exception as e:
        # Session creation failed, but we can still return the ID
        created_sessions.add(new_session_id)
    
    return {"session_id": new_session_id}

@app.post("/feedback")
async def submit_feedback(data: FeedbackModel):
    """Submit user feedback on recommendations"""
    session_id = data.session_id or DEFAULT_SESSION_ID
    
    try:
        # Get session to access state
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
        
        # Create a mock context to use our preference functions
        class MockContext:
            def __init__(self, state):
                self.state = state
        
        context = MockContext(session.state)
        
        # Process feedback
        if data.feedback == "like":
            like_recommendation(context, data.recommendation)
        elif data.feedback == "dislike":
            dislike_recommendation(context, data.recommendation)
        
        # Update session state
        await session_service.update_session_state(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id,
            state=context.state
        )
        
        return {"status": "success", "message": f"Feedback '{data.feedback}' recorded"}
    
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/preferences/{session_id}")
async def get_preferences(session_id: str):
    """Get user preferences for a session"""
    try:
        session = await session_service.get_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=session_id
        )
        
        class MockContext:
            def __init__(self, state):
                self.state = state
        
        context = MockContext(session.state)
        preferences = get_user_preferences(context)
        
        return {"preferences": preferences}
    
    except Exception as e:
        return {"error": str(e)}

@app.get("/sessions")
async def list_sessions():
    """List all sessions for the user"""
    try:
        sessions = await session_service.list_sessions(
            app_name=APP_NAME,
            user_id=USER_ID
        )
        # Handle both tuple and object formats
        session_list = []
        for s in sessions:
            if hasattr(s, 'session_id'):
                session_list.append({"session_id": s.session_id, "created_at": str(getattr(s, 'created_at', 'Unknown'))})
            elif isinstance(s, tuple) and len(s) >= 2:
                session_list.append({"session_id": s[0], "created_at": str(s[1])})
            else:
                session_list.append({"session_id": str(s), "created_at": "Unknown"})
        
        return {"sessions": session_list}
    except Exception as e:
        return {"sessions": list(created_sessions), "error": str(e)}

# -------------------------
# Run Server
# -------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Hospital Reception Assistant API")
    print("=" * 60)
    print("\nAPI running at: http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    print("\nEndpoints:")
    print("  POST /ask-reception - Send queries to the assistant")
    print("  GET  /             - Health check")
    print("\nPress Ctrl+C to stop\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000)