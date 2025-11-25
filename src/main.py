from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.cache.router import router as cache_router

# Імпорти налаштувань логування та Sentry
# (перевір шляхи, якщо раптом файли лежать інакше, але судячи з історії - так)
from src.core.logging.logging_config import setup_logging

# Імпорти роутерів
from src.core.logging.sentry import init_sentry
from src.core.redis_client import close_redis
from src.dog_photos import router as dog_photos_router
from src.external_api import router as external_router

# Імпорти сервісів для закриття з'єднань
from src.external_api.service import service
from src.storage import router as storage_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- STARTUP (Запуск) ---
    setup_logging()  # Налаштовуємо логування
    init_sentry()  # Підключаємо Sentry

    yield

    # --- SHUTDOWN (Вимкнення) ---
    await service.close()  # Закриваємо клієнт зовнішнього API
    await close_redis()  # Закриваємо Redis


app = FastAPI(
    title="Library Storage API + Dogs External API", lifespan=lifespan  # <-- ВАЖЛИВО: Підключаємо lifespan сюди
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
