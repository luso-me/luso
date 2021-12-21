from typing import List, Optional, Dict

import pydantic
from pydantic import BaseModel, Field

from app.models.skill import SkillRead


class UserFields:
    user_id = Field(
        description='ID of user',
        example='VxiguUxKdezsawDEoHatoy',
        min_length=22,
        max_length=22
    )
    username = Field(
        description='Username',
        example='john',
        min_length=1
    )
    name = Field(
        description='Name',
        example='John Doe',
        min_length=1
    )
    skills = Field(
        description='List of skills'
    )
    active = Field(True)


class UserUpdate(BaseModel):
    name: Optional[str] = UserFields.name
    skills: Optional[List[SkillRead]] = UserFields.skills


class UserCreate(UserUpdate):
    username: str = UserFields.username
    name: str = UserFields.name
    github_user_id: str


class UserRead(UserCreate):
    id: str = UserFields.user_id

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
