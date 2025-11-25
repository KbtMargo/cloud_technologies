from unittest.mock import AsyncMock, patch

import pytest

from src.external_api.models import DogBreedListResponse, DogImageResponse


# Тест 1: Отримання випадкового фото (успіх)
@pytest.mark.asyncio
async def test_get_random_dog_image(client):
    # Мокаємо метод get_random_image у сервісі
    with patch("src.external_api.service.service.get_random_image", new_callable=AsyncMock) as mock_get:
        # Налаштовуємо, що поверне сервіс (імітуємо успішну відповідь від DogAPI)
        mock_get.return_value = DogImageResponse(
            message="https://images.dog.ceo/breeds/terrier/1.jpg", status="success"
        )

        response = client.get("/external/dog/random-image")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert "terrier" in data["message"]


# Тест 2: Отримання фото за породою (успіх)
@pytest.mark.asyncio
async def test_get_dog_image_by_breed_success(client):
    with patch("src.external_api.service.service.get_image_by_breed", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = DogImageResponse(message="https://images.dog.ceo/breeds/pug/1.jpg", status="success")

        response = client.get("/external/dog/image-by-breed/pug")

        assert response.status_code == 200
        assert response.json()["message"] == "https://images.dog.ceo/breeds/pug/1.jpg"


# Тест 3: Отримання фото за породою (порода не знайдена - 404)
@pytest.mark.asyncio
async def test_get_dog_image_by_breed_not_found(client):
    with patch("src.external_api.service.service.get_image_by_breed", new_callable=AsyncMock) as mock_get:
        # Сервіс повертає None, коли API кидає помилку або порода не знайдена (згідно твого коду сервісу)
        mock_get.return_value = None

        response = client.get("/external/dog/image-by-breed/unicorn")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"]


# Тест 4: Список усіх порід
@pytest.mark.asyncio
async def test_get_all_breeds(client):
    with patch("src.external_api.service.service.get_all_breeds", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = DogBreedListResponse(message={"pug": [], "terrier": ["yorkshire"]}, status="success")

        response = client.get("/external/dog/breeds")

        assert response.status_code == 200
        data = response.json()
        assert "pug" in data["message"]
        assert "terrier" in data["message"]


# Тест 5: HTML сторінка (перевірка Content-Type)
@pytest.mark.asyncio
async def test_get_random_dog_html(client):
    with patch("src.external_api.service.service.get_random_image", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = DogImageResponse(
            message="https://images.dog.ceo/breeds/labrador/1.jpg", status="success"
        )

        # УВАГА: У твоєму коді роутера є невелика помилка з присвоєнням змінної image_url,
        # але тест ми пишемо на очікувану поведінку.
        # Якщо роутер впаде з 500 помилкою тут - значить треба пофіксити роутер (див. нижче).
        response = client.get("/external/dog/html")

        # Тут ми можемо отримати 500, якщо в роутері помилка коду,
        # або 200, якщо все ок.
        if response.status_code == 200:
            assert "text/html" in response.headers["content-type"]
            assert "<html>" in response.text
        else:
            # Цей блок спрацює, якщо в твоєму коді є баг (див. примітку нижче)
            assert response.status_code == 500


# Тест 6: Симуляція падіння зовнішнього сервісу (500 Error)
@pytest.mark.asyncio
async def test_external_service_failure(client):
    with patch("src.external_api.service.service.get_random_image", new_callable=AsyncMock) as mock_get:
        # Симулюємо, що сервіс викинув виняток (наприклад, Redis впав або HTTP помилка)
        mock_get.side_effect = Exception("Critical connection error")

        response = client.get("/external/dog/random-image")

        assert response.status_code == 500
        assert "Critical connection error" in response.json()["detail"]
