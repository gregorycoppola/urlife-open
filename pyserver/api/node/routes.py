from fastapi import APIRouter
from .create import router as create_router
from .search import router as search_router
from .read import router as read_router
from .read.children import router as children_router

router = APIRouter()
router.include_router(read_router, prefix="/read", tags=["read"])
router.include_router(create_router, prefix="/create", tags=["create"])
router.include_router(search_router, prefix="/search", tags=["search"])
