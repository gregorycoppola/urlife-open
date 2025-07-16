from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from typing import Optional
from pyserver.storage.folder_storage import FolderStorage

router = APIRouter()

class CreateFolderRequest(BaseModel):
    name: str
    parent_id: Optional[str] = None

@router.post("/create")
async def create_folder(request: Request, body: CreateFolderRequest):
    """
    Create a new folder for the current user.
    """
    # You may want to extract user_id from auth/session in real use
    user_id = request.headers.get("x-user-id") or "test_user5"
    storage = FolderStorage(user_id)
    try:
        folder_id = await storage.create_folder(name=body.name, parent_id=body.parent_id)
        return {"id": folder_id}
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
