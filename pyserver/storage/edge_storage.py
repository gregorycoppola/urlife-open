from typing import Optional, List, Dict, Any
import logging
from ..system.redis import RedisManager, map_get
from ..system.graph_node import GraphNode

logger = logging.getLogger(__name__)

class EdgeStorage:
    def __init__(self, user_id: str):
        """
        Storage for graph edges.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id
        self.redis_manager = RedisManager()
        self.backend = RedisEdgeStorage(user_id)

    def store_edge(self, edge: Dict[str, Any]) -> None:
        """Store an edge in Redis."""
        with self.redis_manager.get_connection() as conn:
            self.backend.store_edge(conn, edge)

    def delete_edge(self, edge_id: str) -> None:
        """Delete an edge from Redis."""
        with self.redis_manager.get_connection() as conn:
            self.backend.delete_edge(conn, edge_id)

    def get_edge(self, edge_id: str) -> Optional[Dict[str, Any]]:
        """Get an edge from Redis."""
        with self.redis_manager.get_connection() as conn:
            return self.backend.get_edge(conn, edge_id)

    def retrieve_all_edges(self) -> List[Dict[str, Any]]:
        """Retrieve all edges from Redis."""
        with self.redis_manager.get_connection() as conn:
            return self.backend.retrieve_all_edges(conn)


class RedisEdgeStorage:
    def __init__(self, user_id: str):
        """
        Redis-specific implementation of edge storage.
        
        Args:
            user_id: The user ID for this storage instance
        """
        self.user_id = user_id

    def store_edge(self, conn: Any, edge: Dict[str, Any]) -> None:
        """Store an edge in Redis."""
        edge_id = edge.get('id')
        if not edge_id:
            raise ValueError("Edge must have an ID")
        map_insert(conn, f"urlife:{self.user_id}:edge", edge_id, edge.json())

    def delete_edge(self, conn: Any, edge_id: str) -> None:
        """Delete an edge from Redis."""
        map_delete(conn, f"urlife:{self.user_id}:edge", edge_id)

    def get_edge(self, conn: Any, edge_id: str) -> Optional[Dict[str, Any]]:
        """Get an edge from Redis."""
        value = map_get(conn, f"urlife:{self.user_id}:edge", edge_id)
        if value:
            return dict(value)
        return None

    def retrieve_all_edges(self, conn: Any) -> List[Dict[str, Any]]:
        """Retrieve all edges from Redis."""
        try:
            values = map_get_all_values(conn, f"urlife:{self.user_id}:edge")
            logger.info(f"Found {len(values)} edges in Redis")
            
            edges = []
            for value in values:
                try:
                    edge = dict(value)
                    edges.append(edge)
                    logger.debug(f"Parsed edge: {edge}")
                except Exception as e:
                    logger.error(f"Error parsing edge: {e}")
            
            return edges
        except Exception as e:
            logger.error(f"Error retrieving edges: {e}")
            raise
