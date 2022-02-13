from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class DurationRange(BaseModel):
    min: str
    max: str
    period: str


class SkillResourceItem(BaseModel):
    id: str
    name: str
    summary: str
    web_link: Optional[str]
    duration: str


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
    community_rating: Optional[int]
    duration: str
    estimated_effort: DurationRange
    intended_levels: List[str]
    items: List[SkillResourceItem]
