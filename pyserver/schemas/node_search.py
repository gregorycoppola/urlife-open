from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NodeSearchQuery(BaseModel):
    root_id: str
    object_type: str
    query: str
    limit: int = 10

class SearchResultNode(BaseModel):
    node_id: str
    caption: str
    object_type: str
    creation_time: Optional[datetime]
    match_score: int
