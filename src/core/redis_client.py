from redis.asyncio import Redis, ConnectionPool
from redis.exceptions import RedisError
from src.settings import settings

_redis_pool: ConnectionPool | None = None
_redis_client: Redis | None = None

def get_redis_pool() -> ConnectionPool:
    """Get or create Redis connection pool."""
    global _redis_pool
    if _redis_pool is None:
        _redis_pool = ConnectionPool.from_url(
            settings.redis_url,
            encoding="utf-8",
            decode_responses=True,
            max_connections=10
        )
    return _redis_pool

async def get_redis() -> Redis:
    """Get Redis client using connection pool."""
    global _redis_client
    if _redis_client is None:
        pool = get_redis_pool()
        _redis_client = Redis(connection_pool=pool)
        try:
            await _redis_client.ping()
        except RedisError as e:
            raise
    return _redis_client

async def close_redis():
    """Close Redis connection."""
    global _redis_client, _redis_pool
    if _redis_client:
        await _redis_client.close()
        _redis_client = None
    if _redis_pool:
        await _redis_pool.disconnect()
        _redis_pool = None
