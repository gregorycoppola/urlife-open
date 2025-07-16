from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pyserver.api.dependencies import get_storage_context
from pyserver.schemas.type_properties import get_extra_properties_for_type
from pyserver.storage.storage_context import StorageContext
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class RadioUpdatePayload(BaseModel):
    node_id: str
    field: str
    value: str


@router.post("")
async def update_radio_field(
    payload: RadioUpdatePayload,
    storage: StorageContext = Depends(get_storage_context)
):
    logger.info("📩 Received radio update request:")
    logger.info(f"   • node_id: {payload.node_id}")
    logger.info(f"   • field: {payload.field}")
    logger.info(f"   • value: {payload.value}")

    try:
        node = await storage.node_storage.get_node(payload.node_id)
        logger.info(f"🔍 Fetched node: {node.node_id} (type: {node.object_type})")

        schema = get_extra_properties_for_type(node.object_type)
        radio_fields = {q.key_name: q for q in schema.radio_questions}
        logger.info(f"🔧 Allowed radio fields: {list(radio_fields.keys())}")

        if payload.field not in radio_fields:
            logger.warning(f"❌ Invalid radio field '{payload.field}' for type {node.object_type}")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid radio field '{payload.field}' for type {node.object_type}"
            )

        question = radio_fields[payload.field]
        valid_options = {opt.value for opt in question.options}
        logger.info(f"✅ Valid options for '{payload.field}': {valid_options}")

        if payload.value not in valid_options:
            logger.warning(f"❌ Invalid value '{payload.value}' for field '{payload.field}'")
            raise HTTPException(
                status_code=400,
                detail=f"Invalid value '{payload.value}' for field '{payload.field}'. Valid options: {valid_options}"
            )

        prev_value = node.extra_properties.get(payload.field)
        node.extra_properties[payload.field] = payload.value
        node.updated_at = datetime.utcnow().isoformat()

        logger.info(f"🔁 Updated field '{payload.field}': '{prev_value}' → '{payload.value}'")
        logger.info(f"🕒 Updated 'updated_at' to: {node.updated_at}")

        await storage.node_storage.store_node(node)
        logger.info(f"💾 Node {node.node_id} stored successfully with updated radio value")

        return {
            "status": "success",
            "message": f"Updated '{payload.field}' to '{payload.value}'"
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating radio field: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
