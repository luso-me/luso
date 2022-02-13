from typing import List, Optional

import pydantic
from pydantic import BaseModel, Field

from app.core.user.model.user_skill import UserSkill


class UserFields:
    id = Field(
            description='ID of user',
            example='some id',
            min_length=22,
            max_length=22
    )
    username = Field(
            description='Name',
            example='John Doe',
            min_length=1
    )
    display_name = Field(description='User Display name')
    email = Field(description='Users emails address')
    skills = Field(description='List of skills', default_factory=list)
    plans = Field(description='List of plans', default_factory=list)
    score = Field(description='User Score')
    active = Field(True)


class UserUpdate(BaseModel):
    username: Optional[str] = UserFields.username
    email: Optional[str] = UserFields.email
    skills: Optional[List[UserSkill]] = UserFields.skills


class UserCreate(UserUpdate):
    username: str = UserFields.username
    github_user_id: Optional[str]
    email: str = UserFields.email


class UserRead(UserCreate):
    id: str = UserFields.id

    @pydantic.root_validator(pre=True)
    def _set_user_id(cls, data):
        """Swap the field _id to user_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "user_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data['id'] = document_id
        return data


class UserAdmin(UserRead):
    active: bool = UserFields.active
