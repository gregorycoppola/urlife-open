from fastapi import APIRouter, Depends
from typing import List
from rapidfuzz import fuzz
from pyserver.api.dependencies import get_storage_context
from pyserver.schemas.node_search import NodeSearchQuery, SearchResultNode
from pyserver.storage.storage_context import StorageContext

router = APIRouter()

@router.post("", response_model=List[SearchResultNode])
async def search_nodes(
    query: NodeSearchQuery,
    storage: StorageContext = Depends(get_storage_context)
):
    try:
        # 1. Get all descendant node IDs from root folder
        node_ids = await storage.folder_tracker.list_recursive(query.root_id)

        # 2. Load and filter nodes by object_type
        filtered = []
        for node_id in node_ids:
            node = await storage.node_storage.get_node(node_id)
            if node and node.object_type == query.object_type:
                filtered.append(node)

        # 3. Fuzzy rank
        ranked = sorted(
            filtered,
            key=lambda node: fuzz.partial_ratio(query.query.lower(), node.caption.lower()),
            reverse=True
        )

        # 4. Format and return top N results
        results = [
            SearchResultNode(
                node_id=node.node_id,
                caption=node.caption,
                object_type=node.object_type,
                creation_time=node.creation_time,
                match_score=fuzz.partial_ratio(query.query.lower(), node.caption.lower())
            )
            for node in ranked[:query.limit]
        ]

        return results

    except Exception as e:
        # Optionally log error or re-raise
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")
