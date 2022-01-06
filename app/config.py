from typing import Optional, List

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    mongo_connection_url: str = "localhost:27017"
    mongo_min_pool_size: int = 0
    mongo_max_pool_size: int = 1
    github_client_id: Optional[str]
    github_client_secret: Optional[str]
    cors_allowed_origins: List[str] = ['http://localhost:7000']
    token_secret_key: str
    token_algorithm: str = "HS256"


settings = AppSettings()
