from datetime import datetime, timedelta
import jwt
from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from typing import Optional
from pyserver.storage.storage_context import StorageContext

import logging
logger = logging.getLogger(__name__)

# Security settings
SECRET_KEY = "your-secret-key-here"  # TODO: Move to environment variable
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[str] = None

async def get_current_user_id(request: Request) -> str:
    """Get the current user ID from the JWT token."""
    try:
        logger.info("🔍 Starting token validation...")
        
        # Get and log the Authorization header
        auth = request.headers.get("Authorization")
        logger.info(f"🔍 Authorization header: {auth}")
        
        if not auth:
            logger.error("❌ No Authorization header found")
            raise HTTPException(status_code=401, detail="Not authenticated")
            
        # Extract and log the token
        token = auth.removeprefix("Bearer ").strip()
        logger.info(f"🔍 Token length: {len(token)} characters")
        
        # Decode and log the token payload
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            logger.info(f"🔍 Token payload: {payload}")
            
            user_id = payload.get("user_id")
            if user_id is None:
                logger.error("❌ Token missing user_id")
                raise HTTPException(status_code=401, detail="Invalid token")
                
            logger.info(f"✅ Valid token for user: {user_id}")
            return user_id
            
        except jwt.ExpiredSignatureError:
            logger.error("❌ Token has expired")
            raise HTTPException(status_code=401, detail="Token has expired")
        except jwt.InvalidTokenError:
            logger.error("❌ Invalid token format")
            raise HTTPException(status_code=401, detail="Invalid token format")
        except Exception as e:
            logger.error(f"❌ Error decoding token: {str(e)}", exc_info=True)
            raise HTTPException(status_code=401, detail="Could not validate credentials")
            
    except Exception as e:
        logger.error(f"❌ Unexpected error in get_current_user_id: {str(e)}", exc_info=True)
        raise HTTPException(status_code=401, detail="Authentication error")

def create_jwt_token(data: dict) -> str:
    """Create a JWT token with the given data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
