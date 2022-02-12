from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.skill.models.resource_item import SkillResourceItem


class SkillResource(BaseModel):
    id: str
    name: str
    authors: str
    description: str
    web_link: str
    resource_authored_date: datetime
    resources_added_date: datetime
    tags: List[str]
    community_rating: int
    duration: int
    estimated_effort: int
    intended_levels: List[str]
    skill_resource_items: List[SkillResourceItem]
