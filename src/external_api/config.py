from dataclasses import dataclass

@dataclass
class DogConfig:
    """
    Конфігурація ТІЛЬКИ для dog.ceo API.
    Слідує стилю прикладу cat_config.
    """
    base_url: str = "https://dog.ceo/api"
    
    min_url_length: int = 10
    max_url_length: int = 500

dog_config = DogConfig()