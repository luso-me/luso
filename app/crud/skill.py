import logging
from typing import Optional, List

from bson import ObjectId

from app.database import client
from app.schema.skill import Skill, SkillInDB

skill_collection = client.luso["skill"]

log = logging.getLogger(__name__)


async def insert_skill(skill: Skill) -> Optional[SkillInDB]:
    insert_result = await skill_collection.insert_one(skill.dict())
    return await find_by_id(insert_result.inserted_id)


async def find_by_id(skill_id: ObjectId) -> Optional[SkillInDB]:
    if skill_found := await skill_collection.find_one({"_id": skill_id}):
        return skill_found


async def find_by_name(skill_name: str, limit) -> Optional[SkillInDB]:
    return await skill_collection.find({"name": skill_name}).to_list(limit)


async def find_skills(limit: int = 100) -> List[SkillInDB]:
    return [SkillInDB(**x) for x in await skill_collection.find().to_list(limit)]


async def update_one(skill_id: ObjectId, skill: Skill):
    if update_result := await skill_collection.update_one({"_id": skill_id}, {"$set": skill.dict()}):
        log.info("Update result %s", update_result)
        return update_result


async def delete_one(skill_id: ObjectId):
    delete_result = await skill_collection.delete_one({"_id": ObjectId(skill_id)})
    return delete_result
