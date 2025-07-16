from typing import Optional, List, Dict, Any
import logging
from pyserver.system.redis import RedisManager, map_get, map_insert, map_get_all_values
from pyserver.system.graph_node import GraphNode
from pyserver.system.node_changer import NodeChanger

logger = logging.getLogger(__name__)

class NodeStorage:
    def __init__(self, user_id: str):
        self.user_id = user_id
        self.redis_manager = RedisManager()

    async def clear_all_nodes(self):
        """
        Clears all Redis keys for this test user.
        Only works for user IDs starting with 'test_user'.
        """

        pattern = f"urlife:{self.user_id}:*"
        logger.debug(f"🧹 Clearing Redis keys matching: {pattern}")

        conn = await self.redis_manager.get_connection()
        keys = [key async for key in conn.scan_iter(match=pattern)]

        for key in keys:
            await conn.delete(key)

        logger.info(f"✅ Cleared {len(keys)} Redis keys for user '{self.user_id}'")

    def _get_node_key(self, node_id: str) -> str:
        return f"urlife:{self.user_id}:node"

    async def store_node(self, node: GraphNode) -> str:
        """
        Store a node in Redis with detailed logging.
        
        Args:
            node: The GraphNode to store
            
        Returns:
            str: The node ID that was stored
            
        Raises:
            Exception: If there's an error storing the node
        """
        try:
            logger.info(f"Starting store_node for node: {node.node_id}")
            logger.debug(f"Node type: {node.object_type}")
            logger.debug(f"Node caption: {node.caption}")
            logger.debug(f"Node parent: {node.parent}")
            
            # Get Redis connection
            conn = await self.redis_manager.get_connection()
            logger.info("Got Redis connection")
            
            # Get node ID and key
            node_id = node.node_id
            node_key = self._get_node_key(node_id)
            logger.info(f"Using Redis key: {node_key}")
            
            # Convert node to JSON
            node_json = node.json()
            logger.debug(f"Node JSON: {node_json}")
            
            # Store in Redis
            await map_insert(conn, node_key, node_id, node_json)
            logger.info(f"Successfully stored node: {node_id}")
            
            return node_id
            
        except Exception as e:
            logger.error(f"Error storing node {node_id}: {str(e)}", exc_info=True)
            raise

    async def delete_node(self, node_id: str) -> None:
        conn = await self.redis_manager.get_connection()
        await conn.hdel(self._get_node_key(node_id), node_id)

    async def get_node(self, node_id: str) -> GraphNode:
        try:
            conn = await self.redis_manager.get_connection()
            node_key = self._get_node_key(node_id)
            logger.info(f"🔍 Attempting to get node with ID: {node_id}")
            logger.info(f"🔍 Using Redis key: {node_key}")
            
            value = await map_get(conn, node_key, node_id)
            if not value:
                logger.error(f"❌ Node not found in Redis: {node_id}")
                return None

            logger.info(f"✅ Found node: {node_id}")
            node = GraphNode.model_validate_json(value)
            logger.info(f"🔍 Node type: {node.object_type}")
            return node
        except Exception as e:
            logger.error(f"❌ Error getting node {node_id}: {str(e)}", exc_info=True)
            raise

    async def change_node(self, node_id: str, node_changer: NodeChanger) -> None:
        node = await self.get_node(node_id)
        if not node:
            raise ValueError(f"Node {node_id} not found")

        updates = node_changer.change_node(node)
        logger.info(f"change_node: result {node}")
        await self.store_node(node)

    async def get_all_nodes(self) -> List[GraphNode]:
        try:
            conn = await self.redis_manager.get_connection()
            values = await map_get_all_values(conn, self._get_node_key(""))
            logger.info(f"Found {len(values)} nodes in Redis")

            nodes = []
            for value in values:
                try:
                    node = GraphNode.model_validate_json(value)
                    logger.info(f"Read node: {node}")
                    nodes.append(node)
                except Exception as e:
                    logger.error(f"Error parsing node: {e}")
            return nodes
        except Exception as e:
            logger.error(f"Error retrieving nodes: {e}")
            raise
