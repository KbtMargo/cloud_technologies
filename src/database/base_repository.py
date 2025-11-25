import logging
from typing import Generic, List, Optional, Type, TypeVar

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import Base

ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    """Generic CRUD repository for SQLAlchemy ORM models."""

    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self) -> List[ModelType]:
        """Return all records of the model."""

        try:
            stmt = select(self.model)
            result = await self.session.execute(stmt)
            items = result.scalars().all()

            return items

        except Exception as e:
            raise

    async def get_by_id(self, obj_id: int) -> Optional[ModelType]:
        """Return a record by primary key."""

        try:
            stmt = select(self.model).where(self.model.id == obj_id)
            result = await self.session.execute(stmt)
            item = result.scalar_one_or_none()

            return item

        except Exception as e:
            raise

    async def create(self, data: dict) -> ModelType:
        """Create and store a new record."""

        try:
            obj = self.model(**data)
            self.session.add(obj)
            await self.session.commit()
            await self.session.refresh(obj)

            return obj

        except Exception as e:
            await self.session.rollback()
            raise

    async def update(self, obj_id: int, data: dict) -> Optional[ModelType]:
        """Update an existing record and return the updated model instance."""

        try:
            stmt = update(self.model).where(self.model.id == obj_id).values(**data).returning(self.model)
            result = await self.session.execute(stmt)
            updated = result.scalar_one_or_none()
            await self.session.commit()

            return updated

        except Exception as e:
            await self.session.rollback()
            raise

    async def delete(self, obj_id: int) -> None:
        """Delete a record by ID."""

        try:
            stmt = delete(self.model).where(self.model.id == obj_id)
            await self.session.execute(stmt)
            await self.session.commit()

        except Exception as e:
            await self.session.rollback()
            raise
