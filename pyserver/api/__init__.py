from fastapi import APIRouter
from .node import router as node_router
from .folders import router as folders_router
from .auth.routes import router as auth_router
from .schema import router as schema_router

router = APIRouter()

router.include_router(node_router, prefix="/nodes", tags=["nodes"])
router.include_router(folders_router, tags=["folders"])
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(schema_router, prefix="/schema", tags=["schema"])