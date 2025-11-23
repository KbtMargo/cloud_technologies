import logging
from fastapi import APIRouter, HTTPException
from urllib.parse import unquote

from src.cache.models import CacheItem, CacheResponse, CacheStatus
from src.core.cache import cache_get, cache_set, cache_delete, cache_exists


router = APIRouter(prefix="/cache", tags=["cache"])

def decode_key(key: str) -> str:
    decoded = unquote(key)
    decoded = decoded.strip("'\"")
    return decoded

@router.get("/exists/{key}")
async def check_cache_exists(key: str):
    """
    Перевірити, чи існує ключ в кеші.
    """
    try:
        decoded_key = decode_key(key)
        
        exists = await cache_exists(decoded_key)
        
        return {"key": decoded_key, "exists": exists}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache check error: {str(e)}")

@router.get("/get/{key}", response_model=CacheResponse)
async def get_cache(key: str):
    """
    Отримати значення з кешу за ключем.
    """
    try:
        decoded_key = decode_key(key)
        
        value = await cache_get(decoded_key)
        
        if value is None:
            raise HTTPException(status_code=404, detail="Key not found")
                
        return CacheResponse(key=decoded_key, value=value)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache get error: {str(e)}")

@router.post("/set", response_model=CacheStatus)
async def set_cache(item: CacheItem):
    try:
        decoded_key = decode_key(item.key)
        
        await cache_set(decoded_key, item.value, ttl=item.ttl)
                
        return CacheStatus(status="saved", key=decoded_key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache set error: {str(e)}")

@router.delete("/delete/{key}")
async def delete_cache(key: str):
    """
    Видалити значення з кешу за ключем.
    """
    try:
        decoded_key = decode_key(key)
        
        deleted = await cache_delete(decoded_key)
        
        if not deleted:
            raise HTTPException(status_code=404, detail="Key not found")
                
        return CacheStatus(status="deleted", key=decoded_key)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Cache delete error: {str(e)}")

