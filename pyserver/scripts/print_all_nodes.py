#!/usr/bin/env python3

import asyncio
import argparse
import logging
from pyserver.storage.storage_context import StorageContext
from pyserver.system.graph_node import GraphNode

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_read_all_nodes(user_id: str):
    try:
        storage = StorageContext(user_id=user_id)
        nodes = await storage.node_storage.get_all_nodes()
        logger.info(f"📦 Retrieved {len(nodes)} nodes for user {user_id}")

        for node in nodes:
            print(node.model_dump_json(indent=2))

    except Exception as e:
        logger.error(f"❌ Failed to read all nodes: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Read all nodes for a user from Redis.")
    parser.add_argument("user_id", help="User ID to retrieve nodes for")
    args = parser.parse_args()

    asyncio.run(run_read_all_nodes(args.user_id))
