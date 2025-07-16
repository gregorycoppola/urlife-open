from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from pyserver.api.dependencies import get_storage_context
from pyserver.storage.storage_context import StorageContext
import logging
logger = logging.getLogger(__name__)

from fastapi import APIRouter
from .node import router as node_router
from .children import router as children_router

router = APIRouter()
router.include_router(node_router, prefix="/node", tags=["read"])
router.include_router(children_router, prefix="/children", tags=["children"])
