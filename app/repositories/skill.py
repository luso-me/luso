import logging
from typing import Optional, List, Type, Dict

from uuid import UUID

from bson import ObjectId

from app.database import client
from app.repositories.base import BaseRepository
from app.schema.skill import Skill, InSkill

skill_collection = client.luso["skill"]

log = logging.getLogger(__name__)


async def insert_skill(skill: Skill) -> Optional[Skill]:
    insert_result = await skill_collection.insert_one(skill.dict())
    return await find_by_mongo_id(insert_result.inserted_id)


async def find_by_mongo_id(_id: ObjectId):
    if skill_found := await skill_collection.find_one({"_id": _id}):
        return skill_found


async def find_by_id(skill_id: UUID) -> Optional[Skill]:
    if skill_found := await skill_collection.find_one({"id": skill_id}):
        return skill_found
    return None


async def find_by_name(skill_name: str, limit) -> Optional[Skill]:
    return await skill_collection.find({"name": skill_name}).to_list(limit)


async def find_skills(limit: int = 100) -> List[Skill]:
    return [Skill(**x) for x in await skill_collection.find().to_list(limit)]


async def update_one(skill_id: UUID, skill: Skill):
    if update_result := await skill_collection.update_one({"id": skill_id}, {"$set": skill.dict()}):
        log.info("Update result %s", update_result)
        return update_result


async def delete_one(skill_id: UUID):
    delete_result = await skill_collection.delete_one({"id": skill_id})
    return delete_result


class SkillsRepository(BaseRepository[InSkill, Skill, dict]):
    @property
    def _schema(self) -> Type[Skill]:
        return Skill

    @property
    def _collection(self) -> Type[Skill]:
        return Skill
