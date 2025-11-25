from typing import Dict, List

from pydantic import BaseModel, ConfigDict, Field, HttpUrl

from src.external_api.config import dog_config as cfg

model_config = ConfigDict(from_attributes=True, extra="ignore")


class BaseDogResponse(BaseModel):
    """Базова модель відповіді, яка має поле 'status'"""

    status: str
    model_config = model_config


class DogImageResponse(BaseModel):
    """
    Відповідь, що містить URL зображення.
    Відповідає /breeds/image/random
    """

    message: HttpUrl = Field(
        ..., description="URL to the dog image", min_length=cfg.min_url_length, max_length=cfg.max_url_length
    )
    status: str
    model_config = model_config


class DogBreedListResponse(BaseModel):
    """
    Відповідь, що містить список порід.
    Відповідає /breeds/list/all
    """

    message: Dict[str, List[str]]
    status: str
    model_config = model_config
