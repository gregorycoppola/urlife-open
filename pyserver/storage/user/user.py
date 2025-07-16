from pydantic import BaseModel, EmailStr
from typing import Optional, Dict, Any
from datetime import datetime

class User(BaseModel):
    """Represents a user in the system."""
    
    id: str
    """Unique identifier for the user"""
    
    email: EmailStr
    """User's email address"""
    
    name: Optional[str] = None
    """User's display name"""
    
    password_hash: Optional[str] = None
    """Hashed password for the user"""
    
    created_at: datetime
    """When the user was created"""
    
    updated_at: datetime
    """When the user was last updated"""
    
    is_active: bool = True
    """Whether the user account is active"""
    
    preferences: Dict[str, Any] = {}
    """User preferences stored as a dictionary"""
    
    class Config:
        """Pydantic configuration"""
        from_attributes = True
        """Allows working with SQLAlchemy ORM models"""
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        }
        """Custom JSON encoding for datetime objects"""

    def __str__(self):
        """String representation of the user"""
        return f"User(id={self.id}, email={self.email}, name={self.name})"
