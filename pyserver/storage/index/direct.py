import logging
from typing import List

from pyserver.system.redis import RedisManager

logger = logging.getLogger(__name__)

class DirectFolderIndex:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis_manager = RedisManager()

    def _direct_key(self, folder_id: str) -> str:
        return f"urlife:{self.user_id}:direct_folder:{folder_id}"

    async def add(self, folder_id: str, node_id: str) -> None:
        key = self._direct_key(folder_id)
        conn = await self.redis_manager.get_connection()
        logger.info(f"📁 Adding node '{node_id}' to folder '{folder_id}' (key: {key})")
        await conn.sadd(key, node_id)

    async def remove(self, folder_id: str, node_id: str) -> None:
        key = self._direct_key(folder_id)
        conn = await self.redis_manager.get_connection()
        logger.info(f"🗑️ Removing node '{node_id}' from folder '{folder_id}' (key: {key})")
        await conn.srem(key, node_id)

    async def list(self, folder_id: str) -> List[str]:
        key = self._direct_key(folder_id)
        conn = await self.redis_manager.get_connection()
        logger.info(f"📋 Listing nodes in folder '{folder_id}' (key: {key})")
        return await conn.smembers(key)

    async def clear_all_direct_indexes(self) -> None:
        """
        Clears all direct folder index keys for this user.
        Only allowed for test users (to avoid accidental production deletion).
        """
        pattern = f"urlife:{self.user_id}:direct_folder:*"
        logger.debug(f"🧹 Scanning for keys: {pattern}")

        conn = await self.redis_manager.get_connection()
        keys = [key async for key in conn.scan_iter(match=pattern)]

        for key in keys:
            await conn.delete(key)

        logger.info(f"✅ Cleared {len(keys)} direct folder indexes for user '{self.user_id}'")
