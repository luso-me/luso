import os
from datetime import datetime
from typing import List, Optional

import pydantic
import shortuuid  # type: ignore
import structlog
from pydantic import BaseModel, Field

from app.core.skill.model.resource import SkillResource, SkillResourceItem

log = structlog.get_logger()
resource_categories = ["Book", "Website", "Course", "Other"]
skill_categories = ["Languages & Frameworks", "Platforms", "Tools", "Techniques"]


class SkillFields:
    id = Field(
        description="ID of skill",
        example="VxiguUxKdezsawDEoHatoy",
        min_length=22,
        max_length=22,
    )
    name = Field(description="Name of skill", example="Apache Airflow", min_length=1)

    description = Field(description="Description of skill")
    web_link = Field(description="Url of skill")
    repo_link = Field(description="Repo of skill")
    icon_link = Field(description="Icon link")

    tags = Field(
        description="List of tags",
        example=["cncf::Data Engineering"],
        default_factory=list,
    )

    category = Field(description="Category of the Skill")
    active = Field(description="Is skill active")
    resources = Field(description="List of skill resources", default_factory=list)


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

    def generate_icon_name(self, skill_name: str, icon_name: str):
        log.info(f"Generating icon name [{icon_name}] for [{skill_name}]")
        new_icon_name = skill_name.lower()
        basename, ext = os.path.splitext(icon_name)

        return f"{new_icon_name}{ext}"

    def set_default_values(self, skill):
        log.info(f"Setting default values on skill")
        if skill.resources is not None:
            for resource in skill.resources:
                if not resource.resource_added_date:
                    self._set_resource_added_date(resource)
                if not resource.id:
                    self._set_resource_id(skill, resource)
                for item in resource.items:
                    if not item.id:
                        self._set_resource_item_id(resource, item)

    def _set_resource_added_date(self, resource: SkillResource):
        log.info(f"resource added date missing for resource: [{resource.name}]")
        resource.resource_added_date = datetime.utcnow()

    def _set_resource_id(self, skill, resource: SkillResource):
        log.info(f"resource id missing for skill: [{skill.name}]")
        resource.id = shortuuid.uuid()

    def _set_resource_item_id(self, resource: SkillResource, item: SkillResourceItem):
        log.info(f"item id missing for resource: [{resource.name}]")
        item.id = shortuuid.uuid()


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
            data["id"] = document_id
        return data
