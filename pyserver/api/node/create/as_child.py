from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode, ChildRef
from pyserver.schemas.type_properties import get_extra_properties_for_type
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.node_storage import NodeStorage
import secrets
import time
import logging

router = APIRouter()
logger = logging.getLogger(__name__)

class NodeUnderLabelCreateRequest(BaseModel):
    parent_id: str
    edge_label: str
    object_type: str
    caption: str

@router.post("/as_child")
async def create_node_under_label(
    req: NodeUnderLabelCreateRequest,
    storage: StorageContext = Depends(get_storage_context)
):
    """
    Create a node under a non-folder node with a specific labeled edge.
    """
    try:
        parent_node = await storage.node_storage.get_node(req.parent_id)
        if not parent_node:
            raise HTTPException(status_code=404, detail="Parent node not found")

        if parent_node.object_type.upper() == "FOLDER":
            raise HTTPException(status_code=400, detail="Use /in_folder to add to folders")
        
        # Validate edge_label is allowed for parent node's type
        parent_schema = get_extra_properties_for_type(parent_node.object_type)
        valid_labels = parent_schema.edge_labels

        if req.edge_label not in valid_labels:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid edge label '{req.edge_label}' for parent type '{parent_node.object_type}'. "
                    f"Allowed labels: {valid_labels}"
            )

        logger.info(f"📥 Creating new {req.object_type} node under parent {req.parent_id} via edge '{req.edge_label}'")

        # Create new node
        node_id = secrets.token_hex(16)
        now = int(time.time())
        type_schema = get_extra_properties_for_type(req.object_type)
        extra_props = {
            q.key_name: q.options[0].value if q.options else None
            for q in type_schema.radio_questions
        }
        extra_props.update({
            q.key_name: False for q in type_schema.checkbox_questions
        })
        extra_props.update({
            q.key_name: q.default for q in type_schema.number_questions
        })
        extra_props.update({
            q.key_name: {"date": None if q.has_date else None, "time": None if q.has_time else None}
            for q in type_schema.date_questions
        })

        node = GraphNode(
            node_id=node_id,
            object_type=req.object_type,
            caption=req.caption,
            extra_properties=extra_props,
            parent={"edge_label": req.edge_label, "parent_id": req.parent_id},
            creation_time=now,
        )

        node_storage = NodeStorage(storage.user_id)
        await node_storage.store_node(node)

        # Update parent's children map
        children = parent_node.children or {}
        children.setdefault(req.edge_label, []).append(
            ChildRef(edge_label=req.edge_label, child_id=node_id)
        )
        parent_node.children = children
        await node_storage.store_node(parent_node)

        logger.info(f"✅ Created node {node_id} under {req.parent_id} via edge '{req.edge_label}'")

        return {
            "node_id": node_id,
            "message": f"Node created and linked with label '{req.edge_label}'"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error creating labeled child node: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
