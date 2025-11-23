from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from src.storage import router as storage_router
from src.external_api import router as external_router
from src.dog_photos import router as dog_photos_router
from src.cache.router import router as cache_router
from src.external_api.service import service
from src.core.redis_client import close_redis


app = FastAPI(
    title="Library Storage API + Dogs External API",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(storage_router.router)
app.include_router(external_router.router)
app.include_router(dog_photos_router.router)
app.include_router(cache_router)

@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}