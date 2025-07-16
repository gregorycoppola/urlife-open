from redis.asyncio import Redis
from typing import Optional, List
import logging

logger = logging.getLogger(__name__)

class RedisManager:
    def __init__(self):
        self.client: Optional[Redis] = None

    async def connect(self):
        """Create Redis connection."""
        if not self.client:
            self.client = Redis(
                host='localhost',
                port=6379,
                db=0,
                decode_responses=True  # Automatically returns str instead of bytes
            )

    async def close(self):
        """Close Redis connection."""
        if self.client:
            await self.client.close()

    async def get_connection(self) -> Redis:
        """Get Redis connection."""
        if not self.client:
            await self.connect()
        return self.client


# Hash operations

async def map_insert(conn: Redis, key: str, field: str, value: str) -> None:
    """Insert a value into a hash map."""
    await conn.hset(key, field, value)

async def map_get(conn: Redis, key: str, field: str) -> Optional[str]:
    """Get a value from a hash map."""
    return await conn.hget(key, field)

async def map_delete(conn: Redis, key: str, field: str) -> None:
    """Delete a field from a hash map."""
    await conn.hdel(key, field)

async def map_get_all_values(conn: Redis, key: str) -> List[str]:
    """Get all values from a Redis hash map."""
    return await conn.hvals(key)


# Set operations

async def set_add(conn: Redis, key: str, member: str) -> bool:
    """Add a member to a set."""
    logger.debug(f"set_add: key[{key}], member[{member}]")
    return await conn.sadd(key, member)

async def set_delete(conn: Redis, key: str, member: str) -> bool:
    """Remove a member from a set."""
    logger.debug(f"set_delete: key[{key}], member[{member}]")
    return await conn.srem(key, member)

async def set_members(conn: Redis, key: str) -> List[str]:
    """Get all members of a set."""
    return await conn.smembers(key)

async def set_is_member(conn: Redis, key: str, member: str) -> bool:
    """Check if a member exists in a set."""
    return await conn.sismember(key, member)


# List operations

async def seq_push(conn: Redis, key: str, value: str) -> int:
    """Push a value to the end of a list."""
    return await conn.rpush(key, value)

async def seq_pop(conn: Redis, key: str) -> Optional[str]:
    """Pop a value from the start of a list."""
    return await conn.lpop(key)

async def seq_get_all(conn: Redis, key: str) -> List[str]:
    """Get all elements from a list."""
    return await conn.lrange(key, 0, -1)
