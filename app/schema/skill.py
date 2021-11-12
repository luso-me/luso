import uuid

from bson import ObjectId
from pydantic import BaseModel, Field

from ..schema.base import PyObjectId


class SkillId(PyObjectId):
    object_name = "item id"


class Skill(BaseModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)
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


class SkillInDB(Skill):
    _id: PyObjectId = Field(default_factory=PyObjectId)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str, uuid.UUID: str}
