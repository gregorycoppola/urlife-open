from typing import Optional, Dict, Any
import logging
from ..system.redis import RedisManager, map_get

logger = logging.getLogger(__name__)

class SettingsStorage:
    def __init__(self, user_id: str):
        """
        Storage for user settings.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id
        self.redis_manager = RedisManager()
        self.backend = RedisSettingsStorage(user_id)

    def get_setting(self, key: str) -> Optional[str]:
        """Get a setting value."""
        with self.redis_manager.get_connection() as conn:
            return self.backend.get_setting(conn, key)

    def set_setting(self, key: str, value: str) -> None:
        """Set a setting value."""
        with self.redis_manager.get_connection() as conn:
            self.backend.set_setting(conn, key, value)

    def delete_setting(self, key: str) -> None:
        """Delete a setting."""
        with self.redis_manager.get_connection() as conn:
            self.backend.delete_setting(conn, key)


class RedisSettingsStorage:
    def __init__(self, user_id: str):
        """
        Redis-specific implementation of settings storage.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id

    def get_setting(self, conn: Any, key: str) -> Optional[str]:
        """Get a setting value from Redis."""
        value = map_get(conn, f"urlife:{self.user_id}:settings", key)
        if value:
            return str(value)
        return None

    def set_setting(self, conn: Any, key: str, value: str) -> None:
        """Set a setting value in Redis."""
        map_insert(conn, f"urlife:{self.user_id}:settings", key, value)

    def delete_setting(self, conn: Any, key: str) -> None:
        """Delete a setting from Redis."""
        map_delete(conn, f"urlife:{self.user_id}:settings", key)
