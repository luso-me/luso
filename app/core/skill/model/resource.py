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
    description: str
    web_link: Optional[str]
    duration: Optional[str]


class SkillResource(BaseModel):
    id: str
    name: str
    authors: str
    description: str
    web_link: str
    category: str
    resource_authored_date: Optional[datetime]
    resource_added_date: Optional[datetime]
    tags: Optional[List[str]]
    community_rating: Optional[int]
    duration: Optional[str]
    estimated_effort: Optional[DurationRange]
    intended_levels: Optional[List[str]]
    items: Optional[List[SkillResourceItem]]
