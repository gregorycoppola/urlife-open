from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
from pyserver.schemas.type_properties import get_extra_properties_for_type
from pyserver.system.graph_node import GraphNode
import logging
import time
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)

class UpdateCheckboxRequest(BaseModel):
    node_id: str
    key_name: str
    value: bool

@router.post("")
async def update_checkbox(
    request: UpdateCheckboxRequest,
    storage: StorageContext = Depends(get_storage_context)
):
    try:
        logger.info(f"🛠 Updating checkbox: {request.key_name} → {request.value} for node {request.node_id}")

        # Step 1: Load node
        node = await storage.node_storage.get_node(request.node_id)

        # Step 2: Validate key_name against allowed checkboxes for this type
        props = get_extra_properties_for_type(node.object_type)
        valid_keys = [q.key_name for q in props.checkbox_questions]
        if request.key_name not in valid_keys:
            raise HTTPException(status_code=400, detail=f"Invalid checkbox key: {request.key_name}")

        # Step 3: Update extra_properties
        if node.extra_properties is None:
            node.extra_properties = {}
        node.extra_properties[request.key_name] = request.value
        node.updated_at = datetime.utcnow().isoformat()

        # Step 4: Store updated node
        await storage.node_storage.store_node(node)
        logger.info(f"✅ Updated checkbox field '{request.key_name}' for node {node.node_id}")

        return {"message": f"Checkbox '{request.key_name}' updated successfully", "node_id": node.node_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update checkbox: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update checkbox field")
