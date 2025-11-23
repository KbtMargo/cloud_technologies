import json
from typing import Any, Optional
import asyncio
import time

_memory_cache = {}

async def cache_set(key: str, value: Any, ttl: int | None = None) -> None:
    """Set value in memory cache with optional TTL."""
    try:
        expiration = time.time() + ttl if ttl else None
        _memory_cache[key] = {
            'value': value,
            'expires': expiration
        }
        print(f"[CACHE][SET] Saved key: {key}, value: {value}, TTL: {ttl}")
    except Exception as e:
        print(f"[CACHE][SET] Error: {e}")
        raise e

async def cache_get(key: str) -> Optional[Any]:
    """Get value from memory cache."""
    try:
        if key not in _memory_cache:
            print(f"[CACHE][GET] Key not found: {key}")
            return None
        
        item = _memory_cache[key]
        
        if item['expires'] and time.time() > item['expires']:
            del _memory_cache[key]
            print(f"[CACHE][GET] Key expired: {key}")
            return None
        
        print(f"[CACHE][GET] Retrieved key: {key}, value: {item['value']}")
        return item['value']
    except Exception as e:
        print(f"[CACHE][GET] Error: {e}")
        return None

async def cache_delete(key: str) -> bool:
    """Delete key from memory cache."""
    try:
        if key in _memory_cache:
            del _memory_cache[key]
            print(f"[CACHE][DELETE] Deleted key: {key}")
            return True
        return False
    except Exception as e:
        print(f"[CACHE][DELETE] Error: {e}")
        return False

async def cache_exists(key: str) -> bool:
    """Check if key exists in memory cache."""
    try:
        if key not in _memory_cache:
            return False
        
        item = _memory_cache[key]
        if item['expires'] and time.time() > item['expires']:
            del _memory_cache[key]
            return False
        
        return True
    except Exception as e:
        print(f"[CACHE][EXISTS] Error: {e}")
        return False