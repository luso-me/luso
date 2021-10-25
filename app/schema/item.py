from bson import ObjectId
from pydantic import BaseModel, Field

from ..schema.base import PyObjectId


class ItemId(PyObjectId):
    object_name = "item id"


class Item(BaseModel):
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


class ItemInDB(Item):
    id: ItemId = Field(default_factory=ItemId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
