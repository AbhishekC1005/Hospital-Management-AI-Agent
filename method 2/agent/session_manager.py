"""Session management for CrewAI healthcare system."""
from typing import Dict, Optional, Any
from datetime import datetime
import uuid


class SessionManager:
    """Manages user sessions and conversation context."""
    
    def __init__(self):
        self.sessions: Dict[str, Dict[str, Any]] = {}
    
    def create_session(self, session_id: Optional[str] = None) -> str:
        """Create a new session."""
        if session_id is None:
            session_id = str(uuid.uuid4())
        
        self.sessions[session_id] = {
            'created_at': datetime.now().isoformat(),
            'last_activity': datetime.now().isoformat(),
            'user_info': {},
            'conversation_history': [],
            'preferences': {},
            'context': {}
        }
        
        return session_id
    
    def get_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get session data."""
        if session_id not in self.sessions:
            # Create session if it doesn't exist
            self.create_session(session_id)
        return self.sessions.get(session_id)
    
    def update_session(self, session_id: str, data: Dict[str, Any]):
        """Update session data."""
        if session_id in self.sessions:
            self.sessions[session_id].update(data)
            self.sessions[session_id]['last_activity'] = datetime.now().isoformat()
    
    def add_message(self, session_id: str, role: str, content: str):
        """Add a message to conversation history."""
        if session_id in self.sessions:
            self.sessions[session_id]['conversation_history'].append({
                'role': role,
                'content': content,
                'timestamp': datetime.now().isoformat()
            })
    
    def set_user_info(self, session_id: str, key: str, value: Any):
        """Set user information."""
        if session_id in self.sessions:
            self.sessions[session_id]['user_info'][key] = value
    
    def get_user_info(self, session_id: str, key: str) -> Optional[Any]:
        """Get user information."""
        if session_id in self.sessions:
            return self.sessions[session_id]['user_info'].get(key)
        return None
    
    def get_conversation_context(self, session_id: str, last_n: int = 5) -> str:
        """Get recent conversation context."""
        if session_id not in self.sessions:
            return ""
        
        history = self.sessions[session_id]['conversation_history'][-last_n:]
        
        context = "Recent conversation:\n"
        for msg in history:
            context += f"{msg['role']}: {msg['content'][:100]}...\n"
        
        # Add user info if available
        user_info = self.sessions[session_id]['user_info']
        if user_info:
            context += f"\nUser Information:\n"
            for key, value in user_info.items():
                context += f"  {key}: {value}\n"
        
        return context
    
    def extract_user_info(self, session_id: str, user_message: str):
        """Extract and store user information from messages."""
        message_lower = user_message.lower()
        
        # Extract name
        if 'my name is' in message_lower:
            name = user_message.split('my name is', 1)[1].strip().split()[0]
            self.set_user_info(session_id, 'name', name.capitalize())
        elif 'i am' in message_lower and len(user_message.split()) < 5:
            # "I am John" pattern
            parts = user_message.lower().split('i am', 1)
            if len(parts) > 1:
                name = parts[1].strip().split()[0]
                if name.isalpha():
                    self.set_user_info(session_id, 'name', name.capitalize())
        
        # Extract location/hospital preference
        if 'i work at' in message_lower or 'i am at' in message_lower:
            for hospital in ['City General Hospital', 'Regional Medical Center', 
                           'Community Health Center', 'Metropolitan Hospital', 'District Hospital']:
                if hospital.lower() in message_lower:
                    self.set_user_info(session_id, 'preferred_hospital', hospital)
        
        # Extract role
        if 'i am a' in message_lower:
            roles = ['doctor', 'nurse', 'administrator', 'manager', 'staff']
            for role in roles:
                if role in message_lower:
                    self.set_user_info(session_id, 'role', role.capitalize())


# Global session manager instance
session_manager = SessionManager()
