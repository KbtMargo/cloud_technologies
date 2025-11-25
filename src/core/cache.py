import json
from typing import Any, Optional

from src.core.redis_client import get_redis


async def cache_set(key: str, value: Any, ttl: int | None = None) -> None:
    """Set value in Redis cache with optional TTL."""
    redis = await get_redis()
    try:
        serialized_value = json.dumps(value)
        if ttl:
            await redis.setex(key, ttl, serialized_value)
        else:
            await redis.set(key, serialized_value)
    except Exception as e:
        raise e


async def cache_get(key: str) -> Optional[Any]:
    """Get value from Redis cache."""
    redis = await get_redis()
    try:
        data = await redis.get(key)
        if data is None:
            return None
        result = json.loads(data)
        return result
    except Exception as e:
        return None


async def cache_exists(key: str) -> bool:
    """Check if key exists in Redis cache."""
    redis = await get_redis()
    try:
        result = await redis.exists(key)
        exists = result > 0
        return exists
    except Exception as e:
        return False


async def cache_delete(key: str) -> bool:
    """Delete key from Redis cache."""
    redis = await get_redis()
    try:
        result = await redis.delete(key)
        success = result > 0
        return success
    except Exception as e:
        return False
