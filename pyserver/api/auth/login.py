from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pyserver.api.dependencies import get_user_storage
from pyserver.storage.user.user_storage import UserStorage
from pyserver.api.auth.auth import create_jwt_token
from .routes import LoginResponse, authenticate_user
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/login", response_model=LoginResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    user_storage: UserStorage = Depends(get_user_storage),
):
    try:
        logger.info(f"🚀 Starting login process for user: {form_data.username}")
        logger.debug(f"🔍 Raw form data: {form_data}")

        user = await authenticate_user(form_data.username, form_data.password, user_storage)

        if not user:
            logger.warning("❌ Authentication failed")
            raise HTTPException(status_code=401, detail="Incorrect username or password")

        logger.info(f"✅ User authenticated successfully: {user.email}")
        logger.debug(f"🔍 Authenticated user ID: {user.id}")

        token = create_jwt_token({"user_id": user.id})
        logger.info("✅ JWT token created successfully")

        return LoginResponse(
            access_token=token,
            token_type="bearer",
            user=user
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error in login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
