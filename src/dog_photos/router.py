from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import get_db_session
from src.dog_photos.schema import DogPhotoRead, DogPhotoWithStats
from src.dog_photos.service import dog_photo_service

router = APIRouter(prefix="/dog-photos", tags=["Dog Photos"])


@router.post(
    "/save",
    response_model=DogPhotoWithStats,
    summary="Отримати випадкове зображення з Dog API та зберегти в БД",
)
async def save_dog_photo(
    breed: Optional[str] = Query(None, description="Опціональна порода (наприклад 'beagle')"),
    db: AsyncSession = Depends(get_db_session),
):
    try:
        photo = await dog_photo_service.save_random_photo(db, breed)
        return photo
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "",
    response_model=List[DogPhotoRead],
    summary="Отримати список збережених зображень",
)
async def list_dog_photos(
    limit: int = Query(50, ge=1, le=100),
    db: AsyncSession = Depends(get_db_session),
):
    photos = await dog_photo_service.list_photos(db, limit)
    return photos


@router.get(
    "/{photo_id}",
    response_model=DogPhotoWithStats,
    summary="Отримати одне зображення з БД (і оновити статистику переглядів)",
)
async def get_dog_photo(
    photo_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db_session),
):
    photo = await dog_photo_service.get_photo_with_stats(db, photo_id, increment=True)
    if not photo:
        raise HTTPException(status_code=404, detail="Dog photo not found")
    return photo
