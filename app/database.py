from motor import motor_asyncio  # type: ignore

from app.config import settings


client = motor_asyncio.AsyncIOMotorClient(
    settings.mongo_connection_url,
    minPoolSize=settings.mongo_min_pool_size,
    maxPoolSize=settings.mongo_max_pool_size
)
