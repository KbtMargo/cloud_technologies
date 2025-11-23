from fastapi import APIRouter, HTTPException, Query, Path
from fastapi.responses import HTMLResponse
from typing import Optional

from pydantic import HttpUrl
from src.external_api.service import service
from src.external_api.models import DogImageResponse, DogBreedListResponse

router = APIRouter(prefix="/external", tags=["External API (Dogs)"])

@router.get(
    "/dog/random-image", 
    response_model=DogImageResponse,
    summary="Випадкове зображення собаки"
)
async def get_random_dog_image():  
    """
    Повертає одне випадкове зображення собаки.
    """
    try:
        return await service.get_random_image()  
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/dog/image-by-breed/{breed_name}", 
    response_model=DogImageResponse,
    summary="Випадкове зображення за породою"
)
async def get_dog_image_by_breed( 
    breed_name: str = Path(..., description="Назва породи (н-д, 'hound', 'pug', 'retriever')")
):
    """
    Повертає одне випадкове зображення собаки за вказаною породою.
    """
    try:
        item = await service.get_image_by_breed(breed_name)  
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
async def get_all_breeds(): 
    """
    Повертає повний список усіх порід та їхніх під-порід.
    """
    try:
        return await service.get_all_breeds() 
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get(
    "/dog/html", 
    response_class=HTMLResponse,
    summary="Випадкове зображення (HTML-сторінка)"
)
async def get_random_dog_html(
    breed: Optional[str] = Query(None, description="Опціонально: фільтр за породою (н-д, 'beagle')")
):
    """
    Повертає просту HTML-сторінку з випадковим зображенням.
    """
    try:
        image_url: HttpUrl
        if breed:
            item = await service.get_image_by_breed(breed)
            title = f"Random {breed.capitalize()}"
            if item is None:
                raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found.")
        else:
            item = await service.get_random_image()  
            title = "Random Dog"

        return f"""
        <html>
            <head><title>{title}</title></head>
            <body style="font-family:Arial; text-align:center; padding-top: 20px; background-color: #f4f4f4;">
                <h2>{title}</h2>
                <img src="{image_url}" alt="{title}" style="max-width:90%; max-height: 80vh; border-radius:10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);">
            </body>
        </html>
        """
    except Exception as e:
        detail = str(e)
        status = 500
        if isinstance(e, HTTPException):
            detail = e.detail
            status = e.status_code
        return f"<html><body style='font-family:Arial;'><h2>Error {status}</h2><p>{detail}</p></body></html>"