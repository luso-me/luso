from motor import motor_asyncio  # type: ignore

from .config import settings

client = motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
