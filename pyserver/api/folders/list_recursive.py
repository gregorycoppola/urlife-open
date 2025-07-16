from fastapi import APIRouter, Depends, HTTPException
from typing import List
import logging

from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode

logger = logging.getLogger(__name__)
router = APIRouter()

@router.get("/list_recursive/{folder_id}", response_model=List[GraphNode])
async def list_recursive_folder_contents(
    folder_id: str,
    storage: StorageContext = Depends(get_storage_context)
):
    """
    List all *recursively* indexed contents of a folder, returning full node data.

    This includes all descendants via the recursive folder tracker.

    Args:
        folder_id (str): The ID of the folder to list contents for
        storage (StorageContext): The storage context dependency

    Returns:
        List[GraphNode]: All descendant GraphNodes under this folder

    Raises:
        HTTPException: If any error occurs during listing
    """
    try:
        logger.info(f"📂 Listing recursive contents of folder: {folder_id}")
        node_ids = await storage.folder_tracker.list_recursive(folder_id)
        logger.info(f"🔍 Recursive index returned {len(node_ids)} node IDs")

        nodes: List[GraphNode] = []
        for node_id in node_ids:
            try:
                node = await storage.node_storage.get_node(node_id)
                nodes.append(node)
            except Exception as node_error:
                logger.warning(f"⚠️ Could not load node {node_id}: {str(node_error)}")

        logger.info(f"✅ Returning {len(nodes)} successfully loaded nodes")
        return nodes

    except Exception as e:
        logger.error(f"❌ Error during recursive folder listing: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
