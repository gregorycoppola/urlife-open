from typing import Optional, List
from logging import getLogger
from redis import Connection
from pyserver.storage.node_storage import NodeStorage

logger = getLogger(__name__)

ROOT_FOLDER_NAME = "User"

async def get_folder_id_for_human_name(
    context: NodeStorage,
    human_name: str
) -> Optional[str]:
    """
    Retrieve the folder ID for a given human-readable name with detailed logging.
    
    Args:
        context: Node storage context
        human_name: Human-readable name of the folder
        
    Returns:
        Optional[str]: Folder ID if found, None otherwise
        
    Raises:
        Exception: If there's an error retrieving the folder ID
    """
    try:
        logger.info(f"🔍 Starting folder ID lookup for: {human_name}")
        logger.debug(f"🔍 User ID: {context.user_id}")
        
        # Retrieve all nodes
        logger.info("🔍 Retrieving all nodes from storage")
        all_nodes = await context.get_all_nodes()
        logger.debug(f"🔍 Found {len(all_nodes)} nodes")
        
        # Process each node
        found_folders = []
        for node in all_nodes:
            logger.debug(f"🔍 Processing node: {node.node_id}")
            logger.debug(f"🔍 Node type: {node.object_type}")
            logger.debug(f"🔍 Node caption: {node.caption}")
            
            if node.object_type == "FOLDER":
                found_folders.append(node.node_id)
                logger.debug(f"🔍 Found folder: {node.node_id}")
                
                if node.caption == human_name:
                    logger.info(f"✅ Found matching folder: {human_name} (ID: {node.node_id})")
                    logger.debug(f"✅ Folder details: {node}")
                    return node.node_id
        
        if not found_folders:
            logger.error("❌ No folders found in storage")
        else:
            logger.error(f"❌ No folder found with name '{human_name}'")
            logger.debug(f"❌ Found folders: {found_folders}")
        
        return None
        
    except Exception as e:
        logger.error(f"❌ Error in folder ID lookup: {str(e)}", exc_info=True)
        logger.error(f"❌ Failed to look up folder: {human_name}")
        raise

async def get_folder_id_for_root_human_name(
    context: NodeStorage
) -> Optional[str]:
    """
    Retrieve the ID of the root folder.
    
    Args:
        connection: Redis connection
        context: Node storage context
        
    Returns:
        Optional[str]: Root folder ID if found, None otherwise
    """
    return await get_folder_id_for_human_name(context, ROOT_FOLDER_NAME)
