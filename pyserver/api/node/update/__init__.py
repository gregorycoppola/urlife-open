from fastapi import APIRouter
from .caption import router as caption_router
from .checkbox import router as checkbox_router
from .number import router as number_router
from .radio import router as radio_router

router = APIRouter()

router.include_router(caption_router, prefix="/caption", tags=["node-update-caption"])
router.include_router(checkbox_router, prefix="/checkbox", tags=["node-update-checkbox"])
router.include_router(number_router, prefix="/number", tags=["node-update-number"])
router.include_router(radio_router, prefix="/radio", tags=["node-update-radio"])
