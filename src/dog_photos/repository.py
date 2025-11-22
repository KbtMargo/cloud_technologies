from datetime import datetime, timezone
from typing import Optional, Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base_repository import BaseRepository
from src.dog_photos.models import DogPhoto, DogPhotoStats


class DogPhotoRepository(BaseRepository[DogPhoto]):
    """
    Репозиторій для DogPhoto.
    Наслідується від загального BaseRepository і додає специфічні методи.
    """

    def __init__(self, session: AsyncSession):
        super().__init__(DogPhoto, session)

    async def create_with_stats(
        self,
        *,
        image_url: str,
        breed: Optional[str],
        sub_breed: Optional[str],
    ) -> DogPhoto:
        """Створює DogPhoto + DogPhotoStats в одній транзакції."""
        try:
            photo = DogPhoto(
                image_url=image_url,
                breed=breed,
                sub_breed=sub_breed,
            )
            self.session.add(photo)
            await self.session.flush()

            stats = DogPhotoStats(photo_id=photo.id, views=0)
            self.session.add(stats)

            await self.session.commit()
            await self.session.refresh(photo)
            return photo
        except Exception:
            await self.session.rollback()
            raise

    async def list_photos(self, limit: int = 50) -> Sequence[DogPhoto]:
        stmt = (
            select(DogPhoto)
            .order_by(DogPhoto.created_at.desc())
            .limit(limit)
        )
        res = await self.session.execute(stmt)
        return res.scalars().unique().all()

    async def increment_views(self, photo_id: int) -> Optional[DogPhotoStats]:
        stmt = select(DogPhotoStats).where(DogPhotoStats.photo_id == photo_id)
        res = await self.session.execute(stmt)
        stats = res.scalars().first()
        if not stats:
            return None

        stats.views += 1
        stats.last_viewed_at = datetime.now(timezone.utc).replace(tzinfo=None)
        await self.session.commit()
        await self.session.refresh(stats)
        return stats
