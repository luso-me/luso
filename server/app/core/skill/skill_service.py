from typing import IO

import structlog

from server.app.config import settings
from server.app.core.media.icon_service import IconService
from server.app.core.media.media_service import MediaService
from server.app.core.skill.model.base import SkillCreate, SkillUpdate, SkillRead
from server.app.database import get_db_client
from server.app.repositories.skill import SkillRepository, SkillAlreadyExistException

log = structlog.get_logger()


class SkillService:
    def __init__(self):
        self.skill_repo = SkillRepository(
            db_client_factory=get_db_client, db_name="luso", collection_name="skills"
        )
        self.media_service = MediaService(
            region=settings.icons_s3_bucket_region, bucket_name=settings.icons_s3_bucket
        )
        self.icon_service = IconService()

    async def list_skills(self, limit: int = 100):
        log.info(f"Fetching [{limit}] skills")
        return await self.skill_repo.list(limit)

    async def find_skill(self, skill_name, limit=100):
        log.info(f"Attempting to find skill with name [{skill_name}]")
        return await self.skill_repo.find({"name": skill_name}, limit=limit)

    async def get_skill(self, skill_id: str):
        log.info(f"Attempting to get skill with id [{skill_id}]")
        return await self.skill_repo.get(skill_id)

    async def delete_skill(self, skill_id: str):
        log.info(f"Deleting skill [{skill_id}]")
        await self.skill_repo.delete(skill_id)

    async def create_skill(self, skill: SkillCreate):
        log.info(f"Attempting to create skill [{skill}]")
        if await self.check_if_skill_exist(skill.name):
            log.error(
                f"Unable to create skill with name: [{skill.name}] because "
                f"it already exists"
            )
            raise SkillAlreadyExistException(f"Skill [{skill.name}] already exist")

        skill.set_default_values(skill)
        await self._set_missing_icon(skill)

        return await self.skill_repo.create(skill)

    async def update_skill(self, skill_id: str, skill: SkillUpdate):
        log.info(f"Updating skill [{skill_id}] with [{skill}]")
        skill.set_default_values(skill)

        return await self.skill_repo.update(skill_id, skill)

    async def update_skill_icon(
        self, skill_id: str, skill_name: str, icon_name: str, icon_file: IO
    ) -> SkillRead:
        log.info(f"Updating icon for skill [{skill_name}] with id [{skill_id}]")

        skill = await self.get_skill(skill_id)
        icon_name = skill.generate_icon_name(skill_name, icon_name)
        skill.icon_link = await self.media_service.upload_image(icon_name, icon_file)

        return await self.skill_repo.update(skill_id, skill)

    async def check_if_skill_exist(self, skill_name: str):
        log.info(f"Checking if skill with name [{skill_name}] exists")
        skill = await self.skill_repo.find({"name": skill_name})

        return True if skill else False

    async def _set_missing_icon(self, skill: SkillCreate):
        skill.icon_link = await self.media_service.upload_image(
            skill.generate_icon_name(skill.name, "default.svg"),
            await self.icon_service.generate_icon(skill.name),
        )
