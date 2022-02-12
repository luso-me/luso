from typing import List, Optional

from pydantic import BaseModel

from app.core.user.model.user_skill_note import UserSkillNote
from app.core.user.model.user_skill_used import UserSkillUsed


class UserSkill(BaseModel):
    name: Optional[str]
    icon_link: Optional[str]
    tags: Optional[List[str]]
    category: Optional[str]
    user_rating: Optional[int]
    score: Optional[float]
    confidence: Optional[float]
    notes: Optional[List[UserSkillNote]]
    used: Optional[UserSkillUsed]
