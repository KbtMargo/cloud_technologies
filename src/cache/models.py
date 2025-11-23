from typing import Any, Optional
from pydantic import BaseModel, Field

class CacheItem(BaseModel):
    key: str = Field(..., description="Ключ для зберігання в кеші")
    value: Any = Field(..., description="Значення для зберігання")
    ttl: Optional[int] = Field(None, description="Час життя в секундах")

class CacheResponse(BaseModel):
    key: str
    value: Any

class CacheStatus(BaseModel):
    status: str
    key: str