#!/usr/bin/env python3

import asyncio
import logging
import argparse
from pyserver.schemas.folder_structure import initialize_user_folders
from pyserver.storage.storage_context import StorageContext

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_create_structure(user_id: str):
    try:
        storage = StorageContext(user_id=user_id)
        logger.info(f"📁 Initializing folders for user: {user_id}")
        await initialize_user_folders(storage)
        logger.info("✅ Successfully initialized user folders")
    except Exception as e:
        logger.error(f"❌ Error initializing folders: {str(e)}", exc_info=True)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Initialize default folder structure for a user")
    parser.add_argument("user_id", help="User ID to initialize folders for")
    args = parser.parse_args()

    asyncio.run(run_create_structure(args.user_id))
