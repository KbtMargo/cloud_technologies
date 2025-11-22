from dataclasses import dataclass


@dataclass
class DogPhotoConfig:
    """Конфіг для валідації DTO dog_photos."""

    min_breed_length: int = 2
    max_breed_length: int = 50

    min_url_length: int = 10
    max_url_length: int = 500


dog_photo_config = DogPhotoConfig()
