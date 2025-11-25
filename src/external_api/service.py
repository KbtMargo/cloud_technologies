from typing import Optional

import httpx
import sentry_sdk

from src.core.cache import cache_get, cache_set
from src.external_api.config import dog_config as cfg
from src.external_api.models import DogBreedListResponse, DogImageResponse
from src.settings import settings


class DogApiService:
    def __init__(self):
        self.base_url = cfg.base_url
        self.client = httpx.AsyncClient(timeout=10.0)

    async def _make_request(self, endpoint: str) -> dict:
        full_url = f"{self.base_url}/{endpoint}"
        try:
            response = await self.client.get(full_url)
            response.raise_for_status()
            data = response.json()

            if data.get("status") != "success":
                raise RuntimeError(data.get("message", "API returned non-success status"))

            return data

        except httpx.HTTPError as http_err:
            sentry_sdk.capture_exception(http_err)
            raise RuntimeError(f"API error: {str(http_err)}")
        except Exception as err:
            sentry_sdk.capture_exception(err)
            raise RuntimeError(f"Request failed: {err}")

    async def get_random_image(self) -> DogImageResponse:
        cache_key = "cache:external:dog_random"
        cached = await cache_get(cache_key)
        if cached:
            return DogImageResponse.model_validate(cached)

        data = await self._make_request("breeds/image/random")
        await cache_set(cache_key, data, settings.redis_TTL)
        return DogImageResponse.model_validate(data)

    async def get_image_by_breed(self, breed: str) -> Optional[DogImageResponse]:
        cache_key = f"cache:external:dog_breed:{breed.lower()}"
        cached = await cache_get(cache_key)
        if cached:
            return DogImageResponse.model_validate(cached)

        try:
            breed_clean = breed.strip().lower().replace(" ", "/")
            data = await self._make_request(f"breed/{breed_clean}/images/random")
            await cache_set(cache_key, data, settings.redis_TTL)
            return DogImageResponse.model_validate(data)
        except RuntimeError:
            return None

    async def get_all_breeds(self) -> DogBreedListResponse:
        cache_key = "cache:external:dog_breeds"
        cached = await cache_get(cache_key)
        if cached:
            return DogBreedListResponse.model_validate(cached)

        data = await self._make_request("breeds/list/all")
        await cache_set(cache_key, data, settings.redis_TTL)
        return DogBreedListResponse.model_validate(data)

    async def close(self):
        await self.client.aclose()


service = DogApiService()
