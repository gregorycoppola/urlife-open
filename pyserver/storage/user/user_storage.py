import json
from typing import Optional, Dict, Any, List
import logging
from datetime import datetime

from pyserver.system.redis import RedisManager, map_get, map_delete, map_insert
from pyserver.storage.user.user import User

logger = logging.getLogger(__name__)

class UserStorage:
    def __init__(self):
        """Storage for user data (stateless)."""
        self.redis_manager = RedisManager()

    def _get_user_key(self, user_id: str) -> str:
        return f"urlife:users:{user_id}"

    def _get_email_key(self, email: str) -> str:
        return f"urlife:users:email:{email}"

    async def create_user(self, user: User) -> User:
        conn = await self.redis_manager.get_connection()
        user.created_at = datetime.utcnow()
        user.updated_at = datetime.utcnow()
        user_data = user.dict()
        user_data['created_at'] = user_data['created_at'].isoformat()
        user_data['updated_at'] = user_data['updated_at'].isoformat()

        await map_insert(conn, self._get_user_key(user.id), "data", json.dumps(user_data))
        await map_insert(conn, self._get_email_key(user.email), "user_id", user.id)
        return user

    async def get_user(self, email: str) -> Optional[User]:
        conn = await self.redis_manager.get_connection()
        user_id = await map_get(conn, self._get_email_key(email), "user_id")
        if not user_id:
            return None
        value = await map_get(conn, self._get_user_key(user_id), "data")
        if value:
            return User.parse_raw(value)
        return None

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        conn = await self.redis_manager.get_connection()
        logger.debug(f"🔍 Getting user by ID: {user_id}")
        value = await map_get(conn, self._get_user_key(user_id), "data")
        if not value:
            logger.debug(f"🔍 No user found for ID: {user_id}")
            return None

        data = json.loads(value)
        logger.debug(f"🔍 Found user data: {data}")
        data['created_at'] = datetime.fromisoformat(data['created_at'])
        data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return User(**data)

    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[User]:
        conn = await self.redis_manager.get_connection()
        value = await map_get(conn, self._get_user_key(user_id), "data")
        if not value:
            return None

        user = User.parse_raw(value)
        old_email = user.email

        for key, val in updates.items():
            if hasattr(user, key):
                setattr(user, key, val)

        user.updated_at = datetime.utcnow()
        user_data = user.model_dump()
        user_data['created_at'] = user_data['created_at'].isoformat()
        user_data['updated_at'] = user_data['updated_at'].isoformat()

        if 'email' in updates:
            await map_delete(conn, self._get_email_key(old_email), "user_id")
            await map_insert(conn, self._get_email_key(user.email), "user_id", user_id)

        await map_insert(conn, self._get_user_key(user_id), "data", json.dumps(user_data))
        return user

    async def delete_user(self, user_id: str) -> None:
        conn = await self.redis_manager.get_connection()
        value = await map_get(conn, self._get_user_key(user_id), "data")
        if value:
            user = User.parse_raw(value)
            await map_delete(conn, self._get_email_key(user.email), "user_id")

        await map_delete(conn, self._get_user_key(user_id), "data")

    async def list_users(self, page: int, limit: int, email: Optional[str] = None) -> List[User]:
        conn = await self.redis_manager.get_connection()

        if email:
            user_id = await map_get(conn, self._get_email_key(email), "user_id")
            if not user_id:
                return []
            user_data = await map_get(conn, self._get_user_key(user_id), "data")
            if not user_data:
                return []
            data = json.loads(user_data)
            data['created_at'] = datetime.fromisoformat(data['created_at'])
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
            return [User(**data)]

        # Get all keys matching user pattern
        keys = await conn.keys("urlife:users:*")

        # Safely decode keys and filter out email mapping keys
        user_ids = []
        for key in keys:
            if isinstance(key, bytes):
                key = key.decode()
            if "email" not in key:
                user_ids.append(key.split(":")[-1])

        # Sort and paginate
        user_ids = sorted(user_ids)
        start = (page - 1) * limit
        end = start + limit
        user_ids = user_ids[start:end]

        users = []
        for user_id in user_ids:
            user_data = await map_get(conn, self._get_user_key(user_id), "data")
            if user_data:
                data = json.loads(user_data)
                data['created_at'] = datetime.fromisoformat(data['created_at'])
                data['updated_at'] = datetime.fromisoformat(data['updated_at'])
                users.append(User(**data))

        return users

