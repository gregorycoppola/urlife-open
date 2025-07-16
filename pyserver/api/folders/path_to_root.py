from fastapi import APIRouter, Depends, HTTPException
from pyserver.system.util import get_path_to_root
from pyserver.api.dependencies import get_storage_context
from pyserver.system.graph_node import GraphNode
from pyserver.storage.storage_context import StorageContext
from typing import Any

router = APIRouter()

@router.get("/path_to_root/{node_id}")
async def path_to_root_route(
    node_id: str,
    storage: StorageContext = Depends(get_storage_context)
):
    """
    Get the path from a node up to the root, following parent links.
    """
    try:
        path = await get_path_to_root(node_id, storage)
        # Return as a list of dicts for JSON serialization
        return [
            {"edge_label": edge_label, "node": node.model_dump(mode="json") if hasattr(node, "model_dump") else node.dict()}
            for edge_label, node in path
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
