from fastapi import APIRouter, Depends, HTTPException
from pyserver.api.auth.auth import get_current_user_id
from pyserver.storage.user.user_storage import UserStorage
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/me")
async def get_current_user(
    user_id: str = Depends(get_current_user_id),
):
    """Get the current authenticated user's information."""
    try:
        logger.info("🚀 Starting get_current_user request")
        logger.debug(f"🔍 Received user_id: {user_id}")

        user_storage = UserStorage()
        user = await user_storage.get_user_by_id(user_id)

        if not user:
            logger.error(f"❌ User not found for ID: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")

        logger.info(f"✅ Found user: {user.id} - {user.email}")

        return {
            "user_id": user.id,
            "email": user.email,
            "name": user.name,
            "is_active": user.is_active
        }

    except HTTPException as he:
        logger.error(f"❌ HTTP Error: {str(he)}", exc_info=True)
        raise
    except Exception as e:
        logger.error(f"❌ Unexpected error: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
