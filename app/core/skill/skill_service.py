from datetime import datetime

import structlog

from app.core.skill.model.base import SkillCreate, SkillUpdate
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.skill import SkillRepository, SkillAlreadyExistException

log = structlog.get_logger()

skill_repo = SkillRepository(
    db_client_factory=get_db_client, db_name="luso", collection_name="skills"
)


async def create_skill(skill: SkillCreate):
    if await check_if_skill_exist(skill.name):
        log.error(
            f"Unable to create skill with name: [{skill.name}] because "
            f"it already exists"
        )
        raise SkillAlreadyExistException(f"Skill [{skill.name}] already exist")

    _set_default_values(skill)

    await skill_repo.create(skill)


async def update_skill(skill_id: str, skill: SkillUpdate):
    _set_default_values(skill)

    await skill_repo.update(skill_id, skill)


async def check_if_skill_exist(skill_name: str):
    skill = await skill_repo.find({"name": skill_name})
    log.info(f"Skill is {skill}")

    if skill:
        return True

    return False


def _set_default_values(skill):
    if skill.resources is not None:
        for resource in skill.resources:
            if not resource.resource_added_date:
                log.info(f"resource added date missing for resource: [{resource.name}]")
                resource.resource_added_date = datetime.utcnow()
            if not resource.id:
                log.info(f"resource id missing for skill: [{skill.name}]")
                resource.id = BaseRepository.generate_uuid()
            for item in resource.items:
                if not item.id:
                    log.info(f"item id missing for resource: [{resource.name}]")
                    item.id = BaseRepository.generate_uuid()
