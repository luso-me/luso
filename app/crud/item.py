import logging
from typing import Optional, List

from bson import ObjectId

from app.database import client
from app.schema.item import Item, ItemInDB

item_collection = client.luso["item"]

log = logging.getLogger(__name__)


async def insert_item(item: Item) -> Optional[ItemInDB]:
    insert_result = await item_collection.insert_one(item.dict())
    return await find_by_id(insert_result.inserted_id)


async def find_by_id(item_id: ObjectId) -> Optional[ItemInDB]:
    if item_found := await item_collection.find_one({"_id": item_id}):
        return item_found


async def find_items(limit: int = 100) -> List[ItemInDB]:
    return await item_collection.find().to_list(limit)


async def update_one(item_id: ObjectId, item: Item):
    if update_result := await item_collection.update_one({"_id": item_id}, {"$set": item.dict()}):
        log.info("Update result %s", update_result)
        return update_result


async def delete_one(item_id: ObjectId):
    delete_result = await item_collection.delete_one({"_id": ObjectId(item_id)})
    return delete_result
