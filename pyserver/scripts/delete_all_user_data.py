#!/usr/bin/env python3

import asyncio
import argparse
import logging
from pyserver.storage.storage_context import StorageContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_nuke_all_data(user_id: str):
    try:
        storage = StorageContext(user_id=user_id)
        logger.warning(f"💥 NUKING all data for user: {user_id}")
        await storage.node_storage.clear_all_nodes()
        await storage.folder_tracker.clear_all_indexes()
        logger.info(f"✅ All data nuked for user {user_id}")
    except Exception as e:
        logger.error(f"❌ Failed to nuke all data: {e}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Nuke all data for a user in Redis.")
    parser.add_argument("user_id", help="User ID whose data you want to delete")
    args = parser.parse_args()

    asyncio.run(run_nuke_all_data(args.user_id))
