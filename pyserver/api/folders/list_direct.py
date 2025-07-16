from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/list_direct/{folder_id}", response_model=List[GraphNode])
async def list_folder_contents(
    folder_id: str,
    storage: StorageContext = Depends(get_storage_context)
):
    """
    List all *direct* contents of a folder, returning full node data.

    Args:
        folder_id (str): The ID of the folder to list contents for
        storage (StorageContext): The storage context dependency

    Returns:
        List[GraphNode]: List of GraphNode objects directly contained in the folder

    Raises:
        HTTPException: If folder is not found or listing fails
    """
    try:
        logger.info(f"📁 Listing direct contents of folder: {folder_id}")
        node_ids = await storage.folder_tracker.list_direct(folder_id)
        logger.info(f"✅ Found {len(node_ids)} items in folder {folder_id}")

        nodes: List[GraphNode] = []
        for node_id in node_ids:
            try:
                node = await storage.node_storage.get_node(node_id)
                nodes.append(node)
            except Exception as node_error:
                logger.warning(f"⚠️ Could not load node {node_id}: {str(node_error)}")

        return nodes

    except Exception as e:
        logger.error(f"❌ Error listing folder contents: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
