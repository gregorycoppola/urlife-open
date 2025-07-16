from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
import logging
from datetime import datetime

router = APIRouter()
logger = logging.getLogger(__name__)


class UpdateCaptionRequest(BaseModel):
    node_id: str
    new_caption: str


@router.post("")
async def update_caption(
    req: UpdateCaptionRequest,
    storage: StorageContext = Depends(get_storage_context),
):
    try:
        logger.info(f"🔧 Updating caption for node: {req.node_id}")
        node = await storage.node_storage.get_node(req.node_id)

        if not node:
            raise HTTPException(status_code=404, detail="Node not found")

        node.caption = req.new_caption
        node.updated_at = datetime.utcnow().isoformat()
        # node.updated_at = int(time.time())
        await storage.node_storage.store_node(node)

        logger.info(f"✅ Caption updated for node: {req.node_id}")
        return {"message": "Caption updated successfully", "node_id": node.node_id}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error updating caption: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal server error")
