from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from alembic.config import Config
from alembic import command

from src.storage import router as storage_router
from src.external_api import router as external_router
from src.dog_photos import router as dog_photos_router


def run_migrations() -> None:
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")


app = FastAPI(title="Library Storage API + Dogs External API")

# @app.on_event("startup")
# def on_startup():
#     run_migrations()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(storage_router.router)
app.include_router(external_router.router)
app.include_router(dog_photos_router.router)


@app.get("/")
def root():
    return {"ok": True, "docs": "/docs"}
