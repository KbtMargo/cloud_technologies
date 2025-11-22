from dataclasses import dataclass

@dataclass
class DogConfig:

    base_url: str = "https://dog.ceo/api"
    
    min_url_length: int = 10
    max_url_length: int = 500

dog_config = DogConfig()