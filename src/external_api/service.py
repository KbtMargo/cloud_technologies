import requests
from typing import Optional
from src.external_api.models import DogImageResponse, DogBreedListResponse
from src.external_api.config import dog_config as cfg

class DogApiService:
    """
    Сервіс для роботи *тільки* з https://dog.ceo/dog-api/
    Слідує стилю CatService.
    """
    def __init__(self):
        self.base_url = cfg.base_url

    def _make_request(self, endpoint: str) -> dict:
        """ 
        Допоміжний метод для виконання запитів.
        Кидає RuntimeError, якщо запит не вдався.
        """
        full_url = f"{self.base_url}/{endpoint}"
        try:
            response = requests.get(full_url, timeout=10)
            response.raise_for_status() 
            data = response.json()
            
            if data.get("status") != "success":
                raise RuntimeError(data.get('message', 'API returned non-success status'))
            
            return data
        
        except requests.exceptions.HTTPError as http_err:
            raise RuntimeError(f"API error: {http_err.response.text}")
        except requests.exceptions.RequestException as err:
            raise RuntimeError(f"Network request failed: {err}")

    def get_random_image(self) -> DogImageResponse:
        """ Отримує випадкове зображення собаки """
        data = self._make_request("breeds/image/random")
        return DogImageResponse.model_validate(data)

    def get_image_by_breed(self, breed: str) -> Optional[DogImageResponse]:
        """ Отримує випадкове зображення за породою """
        try:
            breed_clean = breed.strip().lower().replace(" ", "/")
            data = self._make_request(f"breed/{breed_clean}/images/random")
            return DogImageResponse.model_validate(data)
        except RuntimeError:
            return None

    def get_all_breeds(self) -> DogBreedListResponse:
        """ Отримує список усіх порід та під-порід """
        data = self._make_request("breeds/list/all")
        return DogBreedListResponse.model_validate(data)
    
service = DogApiService()