from fastapi import APIRouter, HTTPException, Depends
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
from pyserver.system.folders.folder_operations import get_folder_id_for_human_name
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/root_id", response_model=str)
async def get_root_folder_id(
    storage: StorageContext = Depends(get_storage_context)
):
    """
    Return the fixed ID of the root folder if it exists.
    """
    root_id = "User"
    root_node = await storage.node_storage.get_node(root_id)

    if root_node is None:
        raise HTTPException(status_code=404, detail="Root folder not found")

    return root_id
