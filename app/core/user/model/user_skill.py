from typing import List, Optional

from pydantic import BaseModel


class UserSkillUsed(BaseModel):
    from_date: str
    to_date: str
    at: str


class UserSkill(BaseModel):
    skill_id: str
    name: str
    web_link: str
    icon_link: Optional[str]
    tags: Optional[List[str]]
    category: str
    user_rating: Optional[str]
    score: Optional[float]
    confidence: Optional[float]
    notes: Optional[str]
    used: Optional[List[UserSkillUsed]]
