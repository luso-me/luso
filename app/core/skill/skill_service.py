from datetime import datetime
from typing import IO

import structlog

from app.config import settings
from app.core.media.media_service import MediaService
from app.core.skill.model.base import SkillCreate, SkillUpdate
from app.core.skill.model.resource import SkillResource, SkillResourceItem
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.skill import SkillRepository, SkillAlreadyExistException

log = structlog.get_logger()


class SkillService:
    def __init__(self):
        self.skill_repo = SkillRepository(
            db_client_factory=get_db_client, db_name="luso", collection_name="skills"
        )
        self.media_service = MediaService(
            region=settings.icons_s3_bucket_region,
            bucket_name=settings.icons_s3_bucket,
            random_suffix=True,
        )

    async def list_skills(self, limit: int = 100):
        return await self.skill_repo.list(limit)

    async def find_skill(self, skill_name, limit=100):
        return await self.skill_repo.find({"name": skill_name}, limit=limit)

    async def get_skill(self, skill_id: str):
        return await self.skill_repo.get(skill_id)

    async def delete_skill(self, skill_id: str):
        await self.skill_repo.delete(skill_id)

    async def create_skill(self, skill: SkillCreate):
        if await self.check_if_skill_exist(skill.name):
            log.error(
                f"Unable to create skill with name: [{skill.name}] because "
                f"it already exists"
            )
            raise SkillAlreadyExistException(f"Skill [{skill.name}] already exist")

        self._set_default_values(skill)

        await self.skill_repo.create(skill)

    async def update_skill(self, skill_id: str, skill: SkillUpdate):
        self._set_default_values(skill)

        await self.skill_repo.update(skill_id, skill)

    async def check_if_skill_exist(self, skill_name: str):
        skill = await self.skill_repo.find({"name": skill_name})
        log.info(f"Skill is {skill}")

        if skill:
            return True

        return False

    def _set_default_values(self, skill):
        if skill.resources is not None:
            for resource in skill.resources:
                if not resource.resource_added_date:
                    self._set_resource_added_date(resource)
                if not resource.id:
                    self._set_resource_id(skill, resource)
                for item in resource.items:
                    if not item.id:
                        self._set_resource_item_id(resource, item)

    @staticmethod
    def _set_resource_added_date(resource: SkillResource):
        log.info(f"resource added date missing for resource: [{resource.name}]")
        resource.resource_added_date = datetime.utcnow()

    @staticmethod
    def _set_resource_id(skill, resource: SkillResource):
        log.info(f"resource id missing for skill: [{skill.name}]")
        resource.id = BaseRepository.generate_uuid()

    @staticmethod
    def _set_resource_item_id(resource: SkillResource, item: SkillResourceItem):
        log.info(f"item id missing for resource: [{resource.name}]")
        item.id = BaseRepository.generate_uuid()

    async def update_skill_icon(self, skill_id: str, icon_name: str, icon_file: IO):
        skill = SkillUpdate()
        skill.icon_link = await self.media_service.upload_image(icon_name, icon_file)

        return await self.skill_repo.update(skill_id, skill)
