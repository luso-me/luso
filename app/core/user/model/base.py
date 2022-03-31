from typing import List, Optional

import pydantic
from pydantic import BaseModel, Field

from app.core.user.model.skill_plan import SkillPlan
from app.core.user.model.user_score import UserScore
from app.core.user.model.user_skill import UserSkill

statuses = ["Todo", "In Progress", "Done"]

user_skill_ratings = [
    "Beginner (typically 0 - 3 years xp)",
    "Intermediate (typically 4 - 7 years xp)",
    "Advanced (typically 7 - 12 years xp)",
    "Expert (typically 12+ years xp)",
]

time_horizons = [
    "1 week - 3 months",
    "3 - 6 months",
    "6 months - 1 year",
    "1 year - 3 years",
    "3+ years",
]


class UserFields:
    id = Field(
        description="ID of user", example="some id", min_length=22, max_length=22
    )
    username = Field(description="Username", example="John Doe")
    display_name = Field(description="User Display name")
    email = Field(description="Users emails address")
    active = Field(True)
    skills = Field(description="List of skills", default_factory=list)
    plans = Field(description="List of plans", default_factory=list)
    score = Field(
        description="User Score", default_factory=lambda: UserScore(gold=0, points=0)
    )
    scopes = Field(description="Users scopes", default_factory=list)


class UserUpdate(BaseModel):
    username: Optional[str] = UserFields.username
    email: Optional[str] = UserFields.email
    skills: Optional[List[UserSkill]] = UserFields.skills
    plans: Optional[List[SkillPlan]] = UserFields.plans
    score: Optional[UserScore] = None
    scopes: Optional[List[str]] = UserFields.scopes


class UserCreate(UserUpdate):
    username: Optional[str] = UserFields.username
    github_user_id: str
    email: str = UserFields.email
    score: UserScore = UserFields.score


class UserRead(UserCreate):
    id: str = UserFields.id

    @pydantic.root_validator(pre=True)
    def _set_user_id(cls, data):
        """Swap the field _id to user_id
        (this could be done with field alias, by setting the field as "_id"
        and the alias as "user_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data["id"] = document_id
        return data


class UserAdmin(UserRead):
    active: bool = UserFields.active
