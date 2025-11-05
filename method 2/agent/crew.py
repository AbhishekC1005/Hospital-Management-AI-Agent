"""Simplified CrewAI Healthcare Decision Support System - Let the LLM decide everything."""
from crewai import Agent, Task, Crew, Process
from typing import Dict, Optional
import os
from datetime import datetime
from dotenv import load_dotenv

# Import all tools
from agent.tools.hospital_tools import (
    get_hospital_count_tool,
    get_hospital_names_tool,
    get_hospital_details_tool,
    get_column_names_tool,
    get_date_range_tool,
    calculate_distance_tool,
    get_all_distances_tool,
    get_column_value_tool,
    calculate_travel_cost_tool,
    compare_hospitals_tool,
    analyze_capacity_trends_tool,
    find_nearest_hospital_tool,
    get_system_statistics_tool
)
from agent.tools.rag_function import rag_function_tool

load_dotenv(override=True)

# LLM Configuration
from langchain_openai import ChatOpenAI

default_llm = None
if os.getenv("OPENAI_API_KEY"):
    default_llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.7,
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    print("✓ Using OpenAI GPT-4o-mini")
else:
    print("⚠️ WARNING: No OPENAI_API_KEY found")


# Simple memory per session
class SessionMemory:
    def __init__(self):
        self.sessions = {}
    
    def get_session(self, session_id: str) -> Dict:
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'interactions': [],
                'created_at': datetime.now().isoformat()
            }
        return self.sessions[session_id]
    
    def add_interaction(self, session_id: str, query: str, response: str):
        session = self.get_session(session_id)
        session['interactions'].append({
            'timestamp': datetime.now().isoformat(),
            'query': query,
            'response': response
        })


memory = SessionMemory()


# Single intelligent agent with all tools
healthcare_agent = Agent(
    role='Healthcare Decision Support Assistant',
    goal='Help users with healthcare data queries, analysis, and recommendations using the most appropriate tools.',
    backstory="""You are an intelligent healthcare assistant with access to hospital data and clinical knowledge.
    
    You have these tools available:
    - Hospital data tools: get counts, names, details, column info, date ranges
    - Analysis tools: compare hospitals, analyze trends, get statistics
    - Location tools: calculate distances, find nearest hospitals, estimate travel costs
    - Knowledge tool: rag_function_tool for clinical guidelines and recommendations
    
    Your approach:
    1. Understand what the user is asking
    2. Choose the most appropriate tool(s) to answer
    3. Use the tools to gather information
    4. Provide a clear, helpful response
    
    You are conversational and helpful. Handle greetings naturally, remember user context,
    and provide thoughtful answers whether it's a simple question or complex analysis.
    
    If a tool returns an error, acknowledge it gracefully and suggest alternatives.
    """,
    tools=[
        get_hospital_count_tool,
        get_hospital_names_tool,
        get_hospital_details_tool,
        get_column_names_tool,
        get_date_range_tool,
        calculate_distance_tool,
        get_all_distances_tool,
        get_column_value_tool,
        calculate_travel_cost_tool,
        compare_hospitals_tool,
        analyze_capacity_trends_tool,
        find_nearest_hospital_tool,
        get_system_statistics_tool,
        rag_function_tool
    ],
    llm=default_llm,
    verbose=True,
    max_iter=15,
    memory=True
)


def answer_question(session_id: str, user_query: str) -> Dict:
    """
    Answer healthcare questions using intelligent agent.
    
    Args:
        session_id: User's session ID
        user_query: User's question
        
    Returns:
        Dict with answer and metadata
    """
    try:
        print(f"\n📥 Processing query for session: {session_id[:8]}...")
        
        # Get conversation history for context
        session = memory.get_session(session_id)
        recent_context = ""
        if session['interactions']:
            recent = session['interactions'][-3:]  # Last 3 interactions
            recent_context = "\n\nRecent conversation:\n"
            for interaction in recent:
                recent_context += f"User: {interaction['query']}\n"
                recent_context += f"Assistant: {interaction['response']}\n"
        
        # Create task with context
        task = Task(
            description=f"""
            User Query: {user_query}
            {recent_context}
            
            Instructions:
            - Answer the user's question naturally and helpfully
            - Use tools as needed to gather accurate information
            - Be conversational and remember context from the conversation
            - If you encounter errors, handle them gracefully
            - Provide clear, actionable responses
            """,
            agent=healthcare_agent,
            expected_output="A clear, helpful response that directly answers the user's question."
        )
        
        # Create and run crew
        crew = Crew(
            agents=[healthcare_agent],
            tasks=[task],
            process=Process.sequential,
            verbose=True
        )
        
        start_time = datetime.now()
        result = crew.kickoff()
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds()
        print(f"✅ Completed in {response_time:.2f}s")
        
        # Store interaction
        memory.add_interaction(session_id, user_query, str(result))
        
        return {
            'answer': str(result),
            'metadata': {
                'response_time': f"{response_time:.2f}s",
                'session_interactions': len(session['interactions']) + 1
            }
        }
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {
            'answer': f"I encountered an error: {str(e)}. Please try rephrasing your question.",
            'metadata': {
                'error': True,
                'error_message': str(e)
            }
        }


def get_session_stats(session_id: str) -> Dict:
    """Get statistics for a session."""
    session = memory.get_session(session_id)
    return {
        'session_id': session_id,
        'total_interactions': len(session['interactions']),
        'created_at': session['created_at']
    }


# Export for backward compatibility
healthcare_crew = {
    'healthcare_agent': healthcare_agent,
    'answer_question': answer_question,
    'get_session_stats': get_session_stats,
    'memory': memory
}