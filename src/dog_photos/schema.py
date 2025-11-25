from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, HttpUrl

from src.database.base_schema import BaseOutModel
from src.dog_photos.config import dog_photo_config as cfg


class DogPhotoBase(BaseModel):
    """Базові поля без id/timestamps."""

    image_url: HttpUrl = Field(
        ...,
        description="URL зображення собаки",
        min_length=cfg.min_url_length,
        max_length=cfg.max_url_length,
    )
    breed: Optional[str] = Field(
        None,
        description="Порода (може бути None)",
        min_length=cfg.min_breed_length,
        max_length=cfg.max_breed_length,
    )
    sub_breed: Optional[str] = Field(
        None,
        description="Підпорода (якщо є)",
        max_length=cfg.max_breed_length,
    )


class DogPhotoCreate(DogPhotoBase):
    """DTO для створення запису (використовується всередині сервісу)."""

    pass


class DogPhotoRead(DogPhotoBase, BaseOutModel):
    """Зображення з БД без статистики."""

    pass


class DogPhotoStatsRead(BaseModel):
    """DTO для статистики по одному фото."""

    photo_id: int
    views: int
    last_viewed_at: Optional[datetime] = None


class DogPhotoWithStats(DogPhotoRead):
    """Зображення + статистика."""

    stats: Optional[DogPhotoStatsRead] = None
