from bson import ObjectId
from pydantic import BaseModel, Field

from ..schema.base import PyObjectId


class SkillId(PyObjectId):
    object_name = "item id"


class Skill(BaseModel):
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
    id: PyObjectId

    # Hack around: https://github.com/samuelcolvin/pydantic/issues/565, https://github.com/tiangolo/fastapi/issues/1515
    def __init__(self, *args, **kwargs):
        kwargs['id'] = kwargs.pop('_id')
        super().__init__(*args, **kwargs)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
