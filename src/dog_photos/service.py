from datetime import datetime
from typing import Optional, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from src.dog_photos.models import DogPhoto, DogPhotoStats
from src.dog_photos.repository import DogPhotoRepository
from src.external_api.service import service as dog_api_service

class DogPhotoService:
    async def save_random_photo(
        self,
        db: AsyncSession,
        breed: Optional[str] = None,
    ) -> DogPhoto:
        repo = DogPhotoRepository(db)

        if breed:
            img = dog_api_service.get_image_by_breed(breed)
            if img is None:
                raise ValueError(f"Breed '{breed}' not found.")
            image_url = str(img.message)
            normalized_breed = breed.strip().lower()
            sub_breed = None
        else:
            img = dog_api_service.get_random_image()
            image_url = str(img.message)
            normalized_breed = None
            sub_breed = None

        photo = DogPhoto(
            image_url=image_url,
            breed=normalized_breed,
            sub_breed=sub_breed,
            created_at=datetime.now() 
        )
        db.add(photo)
        await db.commit()
        await db.refresh(photo)
        
        stats = DogPhotoStats(photo_id=photo.id)
        db.add(stats)
        await db.commit()
        
        stmt = (
            select(DogPhoto)
            .where(DogPhoto.id == photo.id)
            .options(selectinload(DogPhoto.stats))
        )
        result = await db.execute(stmt)
        photo_with_stats = result.scalar_one()
        
        return photo_with_stats

    async def list_photos(self, db: AsyncSession, limit: int = 50) -> Sequence[DogPhoto]:
        repo = DogPhotoRepository(db)
        return await repo.list_photos(limit)

    async def get_photo_with_stats(
        self,
        db: AsyncSession,
        photo_id: int,
        increment: bool = True,
    ) -> Optional[DogPhoto]:
        repo = DogPhotoRepository(db)
        photo = await repo.get_by_id(photo_id)
        if not photo:
            return None

        if increment:
            await repo.increment_views(photo_id)

        return photo

dog_photo_service = DogPhotoService()   