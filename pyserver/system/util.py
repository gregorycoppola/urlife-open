from typing import List, Tuple

from pyserver.system.graph_node import GraphNode
from pyserver.storage.storage_context import StorageContext

async def get_path_to_root(
    node_id: str,
    storage: StorageContext
) -> List[Tuple[str, "GraphNode"]]:
    """
    Follow parent links from the given node up to the root.

    Returns:
        A list of (edge_label, GraphNode) pairs, one for each step upward.
    """
    path: List[Tuple[str, GraphNode]] = []

    current_id = node_id
    while True:
        node = await storage.node_storage.get_node(current_id)
        if not node:
            raise ValueError(f"Node {current_id} not found")

        parent_ref = node.parent
        if not parent_ref:
            break  # We've reached the root

        parent_node = await storage.node_storage.get_node(parent_ref.parent_id)
        if not parent_node:
            raise ValueError(f"Parent node {parent_ref.parent_id} not found")

        path.append((parent_ref.edge_label, parent_node))
        current_id = parent_ref.parent_id  # Move upward

    return path
