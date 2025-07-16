from fastapi import APIRouter, HTTPException
from fastapi.logger import logger
from pyserver.schemas.type_properties import get_type_properties_registry

router = APIRouter()

@router.get("/schema/all-type-properties")
async def get_all_type_properties():
    """
    Get extra properties configuration for all supported types.

    Returns:
        Dict[str, ExtraProperties]: Mapping of type names to their extra properties
    """
    try:
        return get_type_properties_registry()
    except Exception as e:
        logger.error(f"Error in get_all_type_properties: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error fetching type properties: {str(e)}")
