from typing import List, Optional

import pydantic
from pydantic import BaseModel, Field


class SkillFields:
    skill_id = Field(
        description='ID of skill',
        example='VxiguUxKdezsawDEoHatoy',
        min_length=22,
        max_length=22
    )
    name = Field(
        description='Name of skill',
        example='Apache Airflow',
        min_length=1
    )
    description = Field(
        description='Description of skill'
    )
    web_link = Field(
        description='Url of skill'
    )
    repo_link = Field(
        description='Repo of skill'
    )
    icon_link = Field(
        description='Icon link'
    )
    tags = Field(
        description='List of tags',
        example=['cncf::Data Engineering']
    )
    active = Field(
        description='Is skill active'
    )


class SkillUpdate(BaseModel):
    name: Optional[str] = SkillFields.name
    description: Optional[str] = SkillFields.description
    web_link: Optional[str] = SkillFields.web_link
    repo_link: Optional[str] = SkillFields.repo_link
    icon_link: Optional[str] = SkillFields.icon_link
    tags: Optional[List[str]] = SkillFields.tags
    active: Optional[bool] = SkillFields.active


class SkillCreate(SkillUpdate):
    name: str = SkillFields.name
    description: str = SkillFields.description


class SkillRead(SkillCreate):
    skill_id: str = SkillFields.skill_id

    @pydantic.root_validator(pre=True)
    def _set_skill_id(cls, data):
        """Swap the field _id to person_id (this could be done with field alias, by setting the field as "_id"
        and the alias as "person_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data['skill_id'] = document_id
        return data