from typing import Optional, Dict, Any, List
import logging
from ..system.redis import RedisManager, map_get

logger = logging.getLogger(__name__)

class FileStorage:
    def __init__(self, user_id: str):
        """
        Storage for files.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id
        self.redis_manager = RedisManager()
        self.backend = RedisFileStorage(user_id)

    def store_file(self, file_id: str, content: bytes) -> None:
        """Store a file in Redis."""
        with self.redis_manager.get_connection() as conn:
            self.backend.store_file(conn, file_id, content)

    def get_file(self, file_id: str) -> Optional[bytes]:
        """Get a file from Redis."""
        with self.redis_manager.get_connection() as conn:
            return self.backend.get_file(conn, file_id)

    def delete_file(self, file_id: str) -> None:
        """Delete a file from Redis."""
        with self.redis_manager.get_connection() as conn:
            self.backend.delete_file(conn, file_id)

    def list_files(self) -> List[str]:
        """List all files."""
        with self.redis_manager.get_connection() as conn:
            return self.backend.list_files(conn)


class RedisFileStorage:
    def __init__(self, user_id: str):
        """
        Redis-specific implementation of file storage.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id

    def store_file(self, conn: Any, file_id: str, content: bytes) -> None:
        """Store a file in Redis."""
        map_insert(conn, f"urlife:{self.user_id}:files", file_id, content)

    def get_file(self, conn: Any, file_id: str) -> Optional[bytes]:
        """Get a file from Redis."""
        value = map_get(conn, f"urlife:{self.user_id}:files", file_id)
        if value:
            return bytes(value)
        return None

    def delete_file(self, conn: Any, file_id: str) -> None:
        """Delete a file from Redis."""
        map_delete(conn, f"urlife:{self.user_id}:files", file_id)

    def list_files(self, conn: Any) -> List[str]:
        """List all files in Redis."""
        try:
            keys = map_get_all_keys(conn, f"urlife:{self.user_id}:files")
            logger.info(f"Found {len(keys)} files in Redis")
            return list(keys)
        except Exception as e:
            logger.error(f"Error listing files: {e}")
            raise
