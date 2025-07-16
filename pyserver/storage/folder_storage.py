from typing import Optional
from logging import getLogger
from datetime import datetime
import uuid
from pyserver.storage.node_storage import NodeStorage
from pyserver.system.graph_node import GraphNode, ParentRef
from pyserver.system.redis import RedisManager
from pyserver.system.folders.folder_operations import get_folder_id_for_human_name

logger = getLogger(__name__)

class FolderStorage:
    def __init__(self, user_id: str):
        """
        Storage for folder operations.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id
        self.redis_manager = RedisManager()
        self.node_storage = NodeStorage(user_id)

    async def get_folder_by_id(self, folder_id: str) -> Optional[dict]:
        """
        Get folder information by ID.

        Args:
            folder_id: The ID of the folder to retrieve

        Returns:
            dict: Folder information if found, None otherwise
        """
        try:
            logger.info(f"🔍 Fetching folder node for ID: {folder_id}")
            folder_node = await self.node_storage.get_node(folder_id)

            if not folder_node:
                logger.error(f"❌ Folder node not found for ID: {folder_id}")
                return None

            if folder_node.object_type != "FOLDER":
                logger.warning(f"⚠️ Node {folder_id} is not a folder (type: {folder_node.object_type})")
                return None

            folder_info = {
                "id": folder_id,
                "name": folder_node.caption,
                "object_type": folder_node.object_type,
                "caption": folder_node.caption,
                "entry_method": getattr(folder_node, "entry_method", "UNKNOWN"),
            }
            logger.debug(f"✅ Returning folder info: {folder_info}")
            return folder_info

        except Exception as e:
            logger.error(f"❌ Error in get_folder_by_id: {e}", exc_info=True)
            return None

    async def get_folder_by_name(self, name: str) -> Optional[dict]:
        """
        Get folder information by human-readable name with detailed logging.
        
        Args:
            name: The human-readable name of the folder
            
        Returns:
            dict: Folder information if found, None otherwise
            
        Raises:
            Exception: If there's an error during folder lookup
        """
        try:
            logger.info(f"🔍 Starting folder lookup for name: {name}")
            logger.debug(f"🔍 User ID: {self.node_storage.user_id}")
            
            # Get folder ID
            logger.info("🔍 Getting folder ID from human name")
            folder_id = await get_folder_id_for_human_name(self.node_storage, name)
            logger.debug(f"🔍 Folder ID lookup result: {folder_id}")
            
            if not folder_id:
                logger.error(f"❌ Folder '{name}' not found")
                logger.debug(f"❌ No folder found with name: {name}")
                return None
            
            logger.info(f"✅ Found folder ID: {folder_id} for name: {name}")
            
            # Get folder node
            logger.info(f"🔍 Fetching folder node for ID: {folder_id}")
            folder_node = await self.node_storage.get_node(folder_id)
            
            if not folder_node:
                logger.error(f"❌ Folder node not found for ID: {folder_id}")
                logger.debug(f"❌ Node storage returned None for ID: {folder_id}")
                return None
            
            logger.debug(f"🔍 Folder node type: {folder_node.object_type}")
            logger.debug(f"🔍 Folder node caption: {folder_node.caption}")
            # logger.debug(f"🔍 Folder node created_at: {folder_node.created_at}")
            logger.debug(f"🔍 Folder node entry_method: {getattr(folder_node, 'entry_method', 'None')}")
            logger.debug(f"🔍 Folder node parent: {folder_node.parent}")
            
            # Prepare response
            folder_info = {
                "id": folder_id,
                "name": name,
                "object_type": folder_node.object_type,
                "caption": folder_node.caption,
                # "created_at": folder_node.created_at,
                "entry_method": folder_node.entry_method if hasattr(folder_node, "entry_method") else "UNKNOWN"
            }
            logger.debug(f"🔍 Returning folder info: {folder_info}")
            
            return folder_info

        except Exception as e:
            logger.error(f"❌ Error in folder lookup: {e}", exc_info=True)
            logger.error(f"❌ Error occurred while looking up folder: {name}")
            raise

    async def list_folder_contents(self, folder_id: str) -> list:
        """
        List contents of a folder.

        Args:
            folder_id: The ID of the folder to list contents for

        Returns:
            list: List of node dicts (or IDs) contained in the folder
        """
        try:
            logger.info(f"📂 Listing contents of folder: {folder_id}")
            all_nodes = await self.node_storage.get_all_nodes()

            children = []
            for node in all_nodes:
                if hasattr(node, "parent") and node.parent and node.parent.parent_id == folder_id:
                    node_info = {
                        "id": node.node_id,
                        "type": node.object_type,
                        "caption": node.caption
                    }
                    children.append(node_info)

            logger.info(f"✅ Found {len(children)} children in folder {folder_id}")
            return children

        except Exception as e:
            logger.error(f"❌ Error listing folder contents: {e}", exc_info=True)
            return []

    async def create_folder(self, name: str, parent_id: Optional[str] = None) -> str:
        """
        Create a new folder.
        
        Args:
            name: The human-readable name of the folder
            parent_id: ID of the parent folder (optional)
            
        Returns:
            str: The ID of the newly created folder
            
        Raises:
            ValueError: If a folder with the same name already exists
        """
        try:
            logger.info(f"Creating folder: {name} (parent: {parent_id})")
            
            # Check if a folder with this name already exists
            existing_folder = await self.get_folder_by_name(name)
            if existing_folder:
                logger.error(f"Folder '{name}' already exists")
                raise ValueError(f"Folder '{name}' already exists")
            
            # Create the folder node with unique ID
            folder_node = GraphNode(
                node_id=str(uuid.uuid4()),
                object_type="FOLDER",
                caption=name,
                extra_properties={
                    "entry_method": "USER",
                    "created_at": datetime.now().isoformat()
                }
            )
            
            # If parent_id is provided, set the parent relationship
            if parent_id:
                folder_node.parent = ParentRef(
                    edge_label="CHILD_OF",
                    parent_id=parent_id
                )
            
            # Store the folder node
            folder_id = await self.node_storage.store_node(folder_node)
            logger.info(f"Created folder: {name} with ID: {folder_id}")
            
            return folder_id
            
        except Exception as e:
            logger.error(f"Error creating folder: {str(e)}")
            raise
