from datetime import datetime
from typing import List

from pydantic import BaseModel

from app.core.skill.models.resource_item import SkillResourceItem


class DurationRange(BaseModel):
    min: str
    max: str
    period: str


class SkillResource(BaseModel):
    id: str
    name: str
    authors: str
    description: str
    web_link: str
    category: str
    resource_authored_date: datetime
    resource_added_date: datetime
    tags: List[str]
    community_rating: int
    duration: str
    estimated_effort: DurationRange
    intended_levels: List[str]
    items: List[SkillResourceItem]
