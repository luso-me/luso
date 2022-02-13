from motor.motor_asyncio import AsyncIOMotorClient  # type: ignore

from app.config import settings

client: AsyncIOMotorClient = None


def get_db_client():
    global client

    if client is None:
        client = AsyncIOMotorClient(
                settings.mongo_connection_url,
                minPoolSize=settings.mongo_min_pool_size,
                maxPoolSize=settings.mongo_max_pool_size
        )

    return client
