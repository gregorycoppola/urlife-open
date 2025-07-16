from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
import logging

from pyserver.storage.storage_context import StorageContext
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.node_storage import GraphNode

logger = logging.getLogger(__name__)

router = APIRouter()

class ChildNodeResponse(BaseModel):
    node_id: str
    caption: str
    object_type: str
    creation_time: Optional[int] = None

@router.get("/{node_id}")
async def get_children(
    node_id: str,
    edge_label: str = Query(..., description="The edge label to filter children by"),
    storage: StorageContext = Depends(get_storage_context)
) -> List[ChildNodeResponse]:
    """
    Get children of a node filtered by edge label.
    """
    try:
        parent_node: GraphNode = await storage.node_storage.get_node(node_id)
        if not parent_node:
            raise HTTPException(status_code=404, detail=f"Node {node_id} not found")

        children = parent_node.children or {}
        edge_children = children.get(edge_label, [])
        child_ids = [child.child_id for child in edge_children]

        child_nodes = []
        for child_id in child_ids:
            child = await storage.node_storage.get_node(child_id)
            if child:
                child_nodes.append(ChildNodeResponse(
                    node_id=child.node_id,
                    caption=child.caption,
                    object_type=child.object_type,
                    creation_time=child.creation_time
                ))
        return child_nodes
    except Exception as e:
        logger.error(f"Error getting children for node {node_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting children: {str(e)}")
