#!/usr/bin/env python3

import asyncio
import logging
from typing import Optional, List
from pydantic import BaseModel

from pyserver.storage.storage_context import StorageContext
from pyserver.storage.user.user import User

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserListResponse(BaseModel):
    users: List[User]
    total: int

async def list_users_cli(page: int = 1, limit: int = 10, email: Optional[str] = None):
    try:
        # Use a fixed admin user_id or read from env/CLI later
        storage_context = StorageContext(user_id="admin")  
        users = await storage_context.user_storage.list_users(page=page, limit=limit, email=email)
        response = UserListResponse(users=users, total=len(users))
        print(response.model_dump_json(indent=2))
    except Exception as e:
        logger.error(f"❌ Error listing users: {str(e)}", exc_info=True)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="List users from Redis")
    parser.add_argument("--page", type=int, default=1, help="Page number")
    parser.add_argument("--limit", type=int, default=10, help="Number of users per page")
    parser.add_argument("--email", type=str, help="Filter by email (optional)")
    args = parser.parse_args()

    asyncio.run(list_users_cli(page=args.page, limit=args.limit, email=args.email))
