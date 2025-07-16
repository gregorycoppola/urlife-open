from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional
from pyserver.api.auth.auth import Token, create_jwt_token
from pyserver.storage.user.user import User
from pyserver.storage.user.user_storage import UserStorage
from pyserver.storage.storage_context import StorageContext

import logging
logger = logging.getLogger(__name__)

router = APIRouter()

class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    user: User

from typing import Optional
import bcrypt
from pyserver.storage.user.user import User

async def authenticate_user(username: str, password: str, user_storage: UserStorage) -> Optional[User]:
    """Authenticate a user by username and password."""
    try:
        logger.info(f"🔍 Attempting to authenticate user: {username}")
        
        # Get user from user storage
        user = await user_storage.get_user(username)
        if not user or not user.is_active:
            logger.info("❌ User not found or inactive")
            return None
            
        # Verify password
        if bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            logger.info("✅ Password verified successfully")
            return user
            
        logger.info("❌ Password verification failed")
        return None
        
    except Exception as e:
        logger.error(f"❌ Error in authenticate_user: {str(e)}", exc_info=True)
        return None


# Import the login router from the new login.py file
from .login import router as login_router

# ... rest of the file ...

# At the end of the file or where routers are included:
router.include_router(login_router, tags=["auth"])  # Ensure /auth/login endpoint is available

from .me import router as me_router
from .register import router as register_router

router.include_router(me_router, tags=["auth"])  # Include the /auth/me endpoint
router.include_router(register_router, tags=["auth"])  # Include the /auth/register endpoint

