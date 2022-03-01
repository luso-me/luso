from typing import Type

from app.core.skill.model.base import SkillRead, SkillUpdate, SkillCreate
from app.repositories.base import BaseRepository


class SkillRepository(BaseRepository[SkillCreate, SkillRead, SkillUpdate]):
    @property
    def _read_schema(self) -> Type[SkillRead]:
        return SkillRead


class SkillAlreadyExistException(Exception):
    pass
