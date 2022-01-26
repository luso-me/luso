from typing import Type

from app.core.skill.models.base import SkillRead, SkillUpdate, SkillCreate
from app.repositories.base import BaseRepository


class SkillRepository(BaseRepository[SkillCreate, SkillRead, SkillUpdate]):
    @property
    def _read_schema(self) -> Type[SkillRead]:
        return SkillRead
