from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import HTMLResponse
from typing import Optional
from src.external_api.service import service
from src.external_api.models import DogImageResponse, DogBreedListResponse

router = APIRouter(prefix="/external", tags=["External API (Dogs)"])

@router.get(
    "/dog/random-image", 
    response_model=DogImageResponse,
    summary="Випадкове зображення собаки"
)
def get_random_dog_image():
    """
    Повертає одне випадкове зображення собаки.
    """
    try:
        return service.get_random_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/dog/image-by-breed/{breed_name}", 
    response_model=DogImageResponse,
    summary="Випадкове зображення за породою"
)
def get_dog_image_by_breed(
    breed_name: str = Path(..., description="Назва породи (н-д, 'hound', 'pug', 'retriever')")
):
    """
    Повертає одне випадкове зображення собаки за вказаною породою.
    """
    try:
        item = service.get_image_by_breed(breed_name)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found.")
        return item
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/dog/breeds", 
    response_model=DogBreedListResponse,
    summary="Список усіх порід"
)
def get_all_breeds():
    """
    Повертає повний список усіх порід та їхніх під-порід.
    """
    try:
        return service.get_all_breeds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
