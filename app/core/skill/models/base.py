from typing import List, Optional

import pydantic
from pydantic import BaseModel, Field

from app.core.skill.models.resource import SkillResource

resource_categories = ["Book", "Website", "Course", "Other"]

skill_categories = ["Languages & Frameworks", "Platforms",
                    "Tools", "Techniques"]


class SkillFields:
    id = Field(
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

    description = Field(description='Description of skill')
    web_link = Field(description='Url of skill')
    repo_link = Field(description='Repo of skill')
    icon_link = Field(description='Icon link')

    tags = Field(
            description='List of tags',
            example=['cncf::Data Engineering']
    )
    category = Field(description='Category of the Skill')
    active = Field(description='Is skill active')
    resources = Field(description='List of skill resources')


class SkillUpdate(BaseModel):
    name: Optional[str] = SkillFields.name
    description: Optional[str] = SkillFields.description
    web_link: Optional[str] = SkillFields.web_link
    repo_link: Optional[str] = SkillFields.repo_link
    icon_link: Optional[str] = SkillFields.icon_link
    tags: Optional[List[str]] = SkillFields.tags
    category: Optional[str] = SkillFields.category
    active: Optional[bool] = SkillFields.active
    resources: Optional[List[SkillResource]] = SkillFields.resources


class SkillCreate(SkillUpdate):
    name: str = SkillFields.name
    description: str = SkillFields.description
    web_link: str = SkillFields.web_link
    category: str = SkillFields.category
    active: bool = SkillFields.active


class SkillRead(SkillCreate):
    id: str = SkillFields.id

    @pydantic.root_validator(pre=True)
    def _set_skill_id(cls, data):
        """Swap the field _id to skill_id
        (this could be done with field alias, by setting the field as "_id"
        and the alias as "skill_id", but can be quite confusing)"""
        document_id = data.get("_id")
        if document_id:
            data['id'] = document_id
        return data
