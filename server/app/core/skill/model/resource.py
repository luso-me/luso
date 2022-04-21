from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class DurationRange(BaseModel):
    min: str
    max: str
    period: str


class SkillResourceItem(BaseModel):
    id: str = Field(default="")
    name: str
    description: str
    web_link: Optional[str]
    duration: Optional[str]


class SkillResource(BaseModel):
    id: str = Field(default="")
    name: str
    authors: str
    description: str
    web_link: str
    category: str
    resource_authored_date: Optional[datetime]
    resource_added_date: Optional[datetime]
    tags: Optional[List[str]] = Field(default_factory=list)
    community_rating: Optional[int] = Field(default=0)
    duration: Optional[str]
    estimated_effort: Optional[DurationRange]
    intended_levels: Optional[List[str]] = Field(default_factory=list)
    items: Optional[List[SkillResourceItem]] = Field(default_factory=list)
