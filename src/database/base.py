from sqlalchemy import text
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.pool import NullPool

from src.settings import settings


class Base(DeclarativeBase):
    pass


DATABASE_URL: str = settings.db_async

engine = create_async_engine(
    url=DATABASE_URL,
    poolclass=NullPool,
    echo=True,
)

db_session_factory = async_sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


async def get_db_session():
    async with db_session_factory() as session:
        yield session


async def _init_citext(conn):
    """Initialize PostgreSQL CITEXT extension if supported."""
    try:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext;"))
    except Exception:
        pass


async def _init_db_models():
    """
    Initialize all tables on startup.
    Використовувати тільки якщо НЕ використовуєш Alembic.
    """
    try:
        async with engine.begin() as conn:
            await _init_citext(conn)
            await conn.run_sync(Base.metadata.create_all)
    except IntegrityError:
        pass
    except Exception as error:
        print(f"DB init error: {error}")


async def _init_citext(conn):
    """Initialize PostgreSQL CITEXT extension if supported."""
    try:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS citext;"))
    except Exception:
        pass


async def _init_db_models():
    """
    Initialize all tables on startup.
    Викликається, якщо потрібно створити таблиці напряму (але в тебе це робить Alembic).
    """
    try:
        async with engine.begin() as conn:
            await _init_citext(conn)
            await conn.run_sync(Base.metadata.create_all)
    except IntegrityError:
        pass
    except Exception as error:
        print(f"DB init error: {error}")
