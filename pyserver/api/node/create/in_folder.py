from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from pyserver.storage.storage_context import StorageContext
from pyserver.storage.node_factory import create_node_under_folder
from pyserver.api.dependencies import get_storage_context

router = APIRouter()

class NodeInFolderCreateRequest(BaseModel):
    folder_id: str
    object_type: str
    caption: str

@router.post("/in_folder")
async def create_node_in_folder(
    req: NodeInFolderCreateRequest,
    storage: StorageContext = Depends(get_storage_context)
):
    """Create a node inside a folder."""
    try:
        node = await create_node_under_folder(
            storage=storage,
            folder_id=req.folder_id,
            object_type=req.object_type,
            caption=req.caption,
        )
        return {
            "node_id": node.node_id,
            "message": "Node created in folder and added to folder's children"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error creating node in folder: {str(e)}")
