import shortuuid
from pydantic import BaseModel, Field

from ..schema.base import PyObjectId


class SkillId(PyObjectId):
    object_name = "item id"


class InSkill(BaseModel):
    name: str = Field(...)
    description: str = Field(...)
    web_link: str = Field(...)
    repo_link: str = Field(None)
    icon_link: str = Field(None)
    tags: list = Field(...)
    active: bool = Field(True)

    class Config:
        schema_extra = {
            "example": {
                "name": "Apache Airflow",
                "description": "Airflow is a platform created ...",
                "web_link": "https://airflow.apache.org/",
                "repo_link": "https://github.com/apache/airflow",
                "icon_link": "",
                "tags": ["category:Framework"],
                "active": True
            }
        }


class Skill(InSkill):
    id: str = Field(default_factory=shortuuid.uuid)

    class Config:
        schema_extra = {
            "example": {
                "id": "ABC123",
                "name": "Apache Airflow",
                "description": "Airflow is a platform created ...",
                "web_link": "https://airflow.apache.org/",
                "repo_link": "https://github.com/apache/airflow",
                "icon_link": "",
                "tags": ["category:Framework"],
                "active": True
            }
        }
