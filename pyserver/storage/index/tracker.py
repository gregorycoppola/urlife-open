import logging
from typing import List

from pyserver.storage.index.direct import DirectFolderIndex
from pyserver.storage.index.recursive import RecursiveFolderIndex
from pyserver.storage.node_storage import NodeStorage
from pyserver.system.graph_node import GraphNode

logger = logging.getLogger(__name__)

class FolderTracker:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.direct = DirectFolderIndex(user_id)

        # Initialize NodeStorage to enable recursive traversal
        self.node_storage = NodeStorage(user_id)
        self.recursive = RecursiveFolderIndex(user_id)

    async def add_to_folder(self, folder_id: str, node_id: str) -> None:
        logger.info(f"\U0001F4E5 Adding node '{node_id}' to folder '{folder_id}' (user: {self.user_id})")
        await self.direct.add(folder_id, node_id)
        await self.recursive.add(folder_id, node_id)

    async def remove_from_folder(self, folder_id: str, node_id: str) -> None:
        logger.info(f"\U0001F5D1️ Removing node '{node_id}' from folder '{folder_id}' (user: {self.user_id})")
        await self.direct.remove(folder_id, node_id)
        await self.recursive.remove(folder_id, node_id)

    async def list_direct(self, folder_id: str) -> List[str]:
        return await self.direct.list(folder_id)

    async def list_recursive(self, folder_id: str) -> List[str]:
        return await self.recursive.list(folder_id)

    async def clear_all_indexes(self) -> None:
        await self.direct.clear_all_direct_indexes()
        await self.recursive.clear_all_recursive_indexes()

    async def get_parent_chain(self, node_id: str) -> List[str]:
        """
        Walks the parent chain of a node until the root and returns a list of folder IDs.
        """
        parents = []
        try:
            current = await self.node_storage.get_node(node_id)
            while current.parent:
                parent_id = current.parent.parent_id
                parents.append(parent_id)
                current = await self.node_storage.get_node(parent_id)
        except Exception as e:
            logger.warning(f"⚠️ Failed to walk parent chain for {node_id}: {e}")
        return parents
