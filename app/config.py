from typing import Optional

from pydantic import BaseSettings


class AppSettings(BaseSettings):
    mongo_connection_url: str
    github_client_id: Optional[str]
    github_client_secret: Optional[str]
    secret_key: str


settings = AppSettings()
