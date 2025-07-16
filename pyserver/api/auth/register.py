from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from pyserver.storage.user.user import User
from pyserver.storage.user.user_storage import UserStorage
from pyserver.storage.storage_context import StorageContext
from pyserver.schemas.folder_structure import initialize_user_folders
import secrets
import bcrypt
from datetime import datetime
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class UserRegistration(BaseModel):
    email: EmailStr
    password: str
    name: str

@router.post("/register")
async def register_user(registration: UserRegistration):
    """Register a new user and initialize their folder structure."""
    try:
        logger.info("🚀 Starting user registration process")
        logger.info(f"📥 Received registration data: {registration.dict()}")

        user_storage = UserStorage()

        logger.info(f"🔍 Checking if user exists with email: {registration.email}")
        existing_user = await user_storage.get_user(registration.email)
        logger.info(f"🔍 User existence check result: {bool(existing_user)}")

        if existing_user:
            logger.info("❌ User already exists")
            raise HTTPException(status_code=400, detail="User already exists")

        logger.info("✅ User does not exist, proceeding with creation")

        user_id = secrets.token_urlsafe(16)
        logger.info(f"🔑 Generated user ID: {user_id}")

        hashed_password = bcrypt.hashpw(
            registration.password.encode(), bcrypt.gensalt()
        ).decode()
        logger.info("🔒 Password hashed successfully")

        user = User(
            id=user_id,
            email=registration.email,
            name=registration.name,
            password_hash=hashed_password,
            is_active=True,
            preferences={},
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        logger.info(f"👤 Created user object: {user.dict()}")

        await user_storage.create_user(user)
        logger.info("✅ User successfully stored in Redis")

        # Initialize folder structure
        try:
            storage = StorageContext(user_id=user_id)
            logger.info(f"📁 Initializing folders for user: {user_id}")
            await initialize_user_folders(storage)
            logger.info("✅ Folder structure initialized")
        except Exception as e:
            logger.error(f"⚠️ Folder initialization failed: {str(e)}", exc_info=True)
            # Optionally: continue, or raise HTTPException

        return {
            "message": "User registered successfully",
            "user_id": user.id
        }

    except HTTPException as he:
        logger.error(f"❌ HTTP Error in register_user: {str(he)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"❌ Error in register_user: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
