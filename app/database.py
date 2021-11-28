from motor import motor_asyncio  # type: ignore

from app.config import settings

client = motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
