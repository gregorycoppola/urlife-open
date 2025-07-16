from fastapi import APIRouter
from .root_id import router as root_id_router
from .list_direct import router as list_direct_router
from .list_recursive import router as list_recursive_router
from .create_folder import router as create_folder_router
from .path_to_root import router as path_to_root_router

router = APIRouter()

router.include_router(root_id_router, prefix="/folder", tags=["folders"])
router.include_router(list_direct_router, prefix="/folder", tags=["folders"])
router.include_router(list_recursive_router, prefix="/folder", tags=["folders"])
router.include_router(create_folder_router, prefix="/folder", tags=["folders"])
router.include_router(path_to_root_router, prefix="/folder", tags=["folders"])
