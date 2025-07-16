from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
import logging
logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/{node_id}")
async def read_node(
    node_id: str,
    storage: StorageContext = Depends(get_storage_context)
):
    try:
        logger.info(f"Attempting to read node with ID: {node_id}")
        node = await storage.node_storage.get_node(node_id)
        logger.info(f"Successfully retrieved node: {node.dict()}")
        return JSONResponse(content=node.dict())
    except ValueError as e:
        logger.error(f"ValueError while reading node {node_id}: {str(e)}")
        raise HTTPException(status_code=404, detail=str(e))
