import logging
from typing import List

from pyserver.system.redis import RedisManager
from pyserver.storage.node_storage import NodeStorage
from pyserver.system.graph_node import GraphNode

logger = logging.getLogger(__name__)

class RecursiveFolderIndex:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis_manager = RedisManager()
        self.node_storage = NodeStorage(user_id)

    def _recursive_key(self, folder_id: str) -> str:
        return f"urlife:{self.user_id}:recursive_folder:{folder_id}"

    async def _get_path_to_root(self, node_id: str) -> List[GraphNode]:
        """
        Follows parent links recursively to get the path to root.
        Returns list of nodes starting from the parent up to root.
        """
        path = []
        current_id = node_id

        while True:
            node = await self.node_storage.get_node(current_id)
            parent_ref = node.parent
            if not parent_ref or not parent_ref.parent_id:
                break
            parent_id = parent_ref.parent_id
            parent_node = await self.node_storage.get_node(parent_id)
            path.append(parent_node)
            current_id = parent_id

        return path

    async def add(self, folder_id: str, node_id: str) -> None:
        """
        Add node to the recursive index of its folder and all ancestor folders.
        """
        conn = await self.redis_manager.get_connection()

        logger.info(f"📥 Adding node '{node_id}' to recursive indexes (starting at folder: {folder_id})")

        path_to_root = await self._get_path_to_root(folder_id)
        folder_ids = [folder_id] + [n.node_id for n in path_to_root]

        for fid in folder_ids:
            key = self._recursive_key(fid)
            await conn.sadd(key, node_id)
            logger.info(f"🔗 Indexed node '{node_id}' under recursive key: {key}")

    async def remove(self, folder_id: str, node_id: str) -> None:
        """
        Remove node from all recursive indexes up the parent chain.
        """
        conn = await self.redis_manager.get_connection()

        logger.info(f"🗑️ Removing node '{node_id}' from recursive indexes (starting at folder: {folder_id})")

        path_to_root = await self._get_path_to_root(folder_id)
        folder_ids = [folder_id] + [n.node_id for n in path_to_root]

        for fid in folder_ids:
            key = self._recursive_key(fid)
            await conn.srem(key, node_id)
            logger.info(f"❌ Removed node '{node_id}' from recursive key: {key}")

    async def list(self, folder_id: str) -> List[str]:
        key = self._recursive_key(folder_id)
        conn = await self.redis_manager.get_connection()
        logger.info(f"📋 Listing recursive contents for folder '{folder_id}' (key: {key})")
        return await conn.smembers(key)

    async def clear_all_recursive_indexes(self) -> None:
        """
        Clears all recursive folder index keys for this user.
        Intended for test environments.
        """
        pattern = f"urlife:{self.user_id}:recursive_folder:*"
        conn = await self.redis_manager.get_connection()
        keys = [key async for key in conn.scan_iter(match=pattern)]
        for key in keys:
            await conn.delete(key)
        logger.info(f"✅ Cleared {len(keys)} recursive folder indexes for user '{self.user_id}'")
