from ..schema.user import User
from app.database import client

db = client.luso
collection = "users"


async def insert_user(user: User):
    return await db[collection].insert_one(user)


async def find_one_inserted(user_id: str):
    return await db[collection].find_one({"_id": user_id})


async def find_users():
    return await db[collection].find().to_list(1000)


async def find_one(user_id: str):
    return await db[collection].find_one({"_id": user_id})


async def update_one(user_id: str, user: User):
    return await db[collection].update_one({"_id": user_id}, {"$set": user})


async def delete_one(user_id: str):
    return await db[collection].delete_one({"_id": user_id})
