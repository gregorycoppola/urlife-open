from fastapi import APIRouter
from .in_folder import router as in_folder_router
from .as_child import router as as_child_router

router = APIRouter()
router.include_router(in_folder_router)
router.include_router(as_child_router)