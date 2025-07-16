from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from datetime import datetime
from pyserver.api.dependencies import get_storage_context
from pyserver.schemas.type_properties import get_extra_properties_for_type
from pyserver.storage.storage_context import StorageContext
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

class NumberUpdatePayload(BaseModel):
    node_id: str
    field: str
    value: float

@router.post("")
async def update_number_field(
    payload: NumberUpdatePayload,
    storage: StorageContext = Depends(get_storage_context)
):
    try:
        node = await storage.node_storage.get_node(payload.node_id)

        # Validate field
        object_type = node.object_type
        schema = get_extra_properties_for_type(object_type)
        num_fields = {q.key_name: q for q in schema.number_questions}

        if payload.field not in num_fields:
            raise HTTPException(status_code=400, detail=f"Field '{payload.field}' is not a valid number field for type {object_type}")

        question = num_fields[payload.field]
        if not (question.min_value <= payload.value <= question.max_value):
            raise HTTPException(status_code=400, detail=f"Value must be between {question.min_value} and {question.max_value}")

        node.extra_properties[payload.field] = payload.value
        node.updated_at = datetime.utcnow().isoformat()

        await storage.node_storage.store_node(node)
        return {"status": "success", "message": f"Field '{payload.field}' updated"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Failed to update number field: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
