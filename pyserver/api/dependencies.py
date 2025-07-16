from fastapi import Depends
from pyserver.api.auth.auth import get_current_user_id
from pyserver.storage.storage_context import StorageContext
from pyserver.storage.user.user_storage import UserStorage

import logging
logger = logging.getLogger(__name__)

def get_user_storage() -> UserStorage:
    return UserStorage()

def get_storage_context(current_user_id: str = Depends(get_current_user_id)) -> StorageContext:
    """
    Get a StorageContext instance for the current authenticated user.
    
    Args:
        current_user_id: The authenticated user's ID
        
    Returns:
        StorageContext: A storage context instance for the user
    """
    logger.info(f"Creating storage context for user: {current_user_id}")
    return StorageContext(user_id=current_user_id)
