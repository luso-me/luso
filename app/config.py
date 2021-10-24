from pydantic import BaseSettings


class AppSettings(BaseSettings):
    mongo_connection_url: str


settings = AppSettings()
