from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class UserSkillUsed(BaseModel):
    from_date: str
    to_date: str
    at: str


class UserSkill(BaseModel):
    skill_id: str
    user_rating: Optional[str]
    score: Optional[float]
    confidence: Optional[float]
    notes: Optional[str]
    used: Optional[List[UserSkillUsed]] = Field(default_factory=list)
