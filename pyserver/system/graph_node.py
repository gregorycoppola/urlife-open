from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field

class ParentRef(BaseModel):
    edge_label: str
    parent_id: str

    class Config:
        arbitrary_types_allowed = True

class ChildRef(BaseModel):
    edge_label: str
    child_id: str

    class Config:
        arbitrary_types_allowed = True

class GraphNode(BaseModel):
    node_id: str
    object_type: str = Field(alias="node_type")
    caption: str
    extra_properties: Optional[Dict[str, Any]] = None
    children: Optional[Dict[str, List[ChildRef]]] = None
    parent: Optional[ParentRef] = None
    creation_time: Optional[int] = None
    updated_at: Optional[str] = None

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
