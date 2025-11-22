# src/settings.py
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    # Database URLs
    db_sync: str = "postgresql://localuser:localpass@localhost:5432/localdb"
    db_async: str = "postgresql+asyncpg://localuser:localpass@localhost:5432/localdb"
    
    # Azure Storage (додайте ці поля)
    azure_storage_connection_string: str = ""
    azure_container_name: str = "lab5"
    
    model_config = ConfigDict(
        env_file=".env",
        extra="ignore"  # Дозволити додаткові змінні в .env
    )

settings = Settings()