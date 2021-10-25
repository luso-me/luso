from motor import motor_asyncio

from .config import settings

client = motor_asyncio.AsyncIOMotorClient(settings.mongo_connection_url)
