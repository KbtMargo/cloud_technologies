from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_sync: str = "postgresql://username:password@localhost:5432/database"
    db_async: str = "postgresql+asyncpg://username:password@localhost:5432/database"

    redis_url: str = "rediss://default:your_redis_password@your-redis-host:6379"
    redis_TTL: int = 60

    azure_storage_connection_string: str = (
        "DefaultEndpointsProtocol=https;AccountName=your_account;AccountKey=your_key;EndpointSuffix=core.windows.net"
    )
    azure_container_name: str = "your_container"

    model_config = ConfigDict(env_file=".env", extra="ignore")


settings = Settings()
