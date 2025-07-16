from typing import List
from .graph_node import GraphNode

class NodeChanger:
    def change_node(self, mutable_node: GraphNode) -> List[dict]:
        """Change a node and return a list of updates."""
        raise NotImplementedError("This method should be implemented by subclasses")
