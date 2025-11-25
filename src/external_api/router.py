from typing import Optional

from fastapi import APIRouter, HTTPException, Path, Query
from fastapi.responses import HTMLResponse
from pydantic import HttpUrl

from src.external_api.models import DogBreedListResponse, DogImageResponse
from src.external_api.service import service

router = APIRouter(prefix="/external", tags=["External API (Dogs)"])


@router.get("/dog/random-image", response_model=DogImageResponse, summary="Випадкове зображення собаки")
async def get_random_dog_image():
    try:
        return await service.get_random_image()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/dog/image-by-breed/{breed_name}", response_model=DogImageResponse, summary="Випадкове зображення за породою"
)
async def get_dog_image_by_breed(
    breed_name: str = Path(..., description="Назва породи (н-д, 'hound', 'pug', 'retriever')")
):
    try:
        item = await service.get_image_by_breed(breed_name)
        if item is None:
            raise HTTPException(status_code=404, detail=f"Breed '{breed_name}' not found.")
        return item
    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dog/breeds", response_model=DogBreedListResponse, summary="Список усіх порід")
async def get_all_breeds():
    try:
        return await service.get_all_breeds()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dog/html", response_class=HTMLResponse, summary="Випадкове зображення (HTML-сторінка)")
async def get_random_dog_html(
    breed: Optional[str] = Query(None, description="Опціонально: фільтр за породою (н-д, 'beagle')")
):
    try:
        if breed:
            item = await service.get_image_by_breed(breed)
            if item is None:
                raise HTTPException(status_code=404, detail=f"Breed '{breed}' not found.")
            title = f"Random {breed.capitalize()}"
        else:
            item = await service.get_random_image()
            title = "Random Dog"

        image_url: HttpUrl = item.message

        return f"""
        <html>
            <head><title>{title}</title></head>
            <body style="font-family:Arial; text-align:center; padding-top: 20px; background-color: #f4f4f4;">
                <h2>{title}</h2>
                <img src="{image_url}" alt="{title}>
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
