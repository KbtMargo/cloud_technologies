import requests
from typing import Optional
# Імпортуємо нові, правильні моделі
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
            # Кидаємо помилку, якщо status code 4xx або 5xx
            response.raise_for_status() 
            data = response.json()
            
            # Важлива перевірка: dog.ceo повертає 200 OK, але status: "error"
            # (наприклад, для породи, якої не існує)
            if data.get("status") != "success":
                raise RuntimeError(data.get('message', 'API returned non-success status'))
            
            return data
        
        except requests.exceptions.HTTPError as http_err:
            # Це спрацює для 404 (порода не знайдена)
            # Ми кидаємо помилку, щоб роутер міг її зловити
            raise RuntimeError(f"API error: {http_err.response.text}")
        except requests.exceptions.RequestException as err:
            # Це для проблем з мережею, DNS, таймаутами
            raise RuntimeError(f"Network request failed: {err}")

    def get_random_image(self) -> DogImageResponse:
        """ Отримує випадкове зображення собаки (аналог get_cat_image) """
        data = self._make_request("breeds/image/random")
        return DogImageResponse.model_validate(data)

    def get_image_by_breed(self, breed: str) -> Optional[DogImageResponse]:
        """ Отримує випадкове зображення за породою """
        try:
            # Очищуємо та форматуємо назву породи
            breed_clean = breed.strip().lower().replace(" ", "/")
            data = self._make_request(f"breed/{breed_clean}/images/random")
            return DogImageResponse.model_validate(data)
        except RuntimeError:
             # Якщо _make_request кинув помилку (н-д, 404), повертаємо None
            return None

    def get_all_breeds(self) -> DogBreedListResponse:
        """ Отримує список усіх порід та під-порід """
        data = self._make_request("breeds/list/all")
        return DogBreedListResponse.model_validate(data)
    
# Створюємо єдиний екземпляр сервісу (як у прикладі)
service = DogApiService()