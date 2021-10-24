from bson import ObjectId
from app.schema.base import PyObjectId
from pydantic import BaseModel, Field


class User(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    items: list = Field(None)
    active: bool = Field(True)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Darth",
                "last_name": "Vader",
                "items": [
                    {
                        "item_id": "000102030406",  # from item
                        "name": "Apache Airflow",  # from item
                        "icon_link": "https://link.to.png",  # from item
                        "tags": ["category:Tools"],  # from item
                        "user_rating": 1,
                        "score": 29,
                        "confidence": 30,
                        "notes": "i love it!",
                        "used": [
                            {
                                "from": "2010",
                                "to": "2012"
                            }
                        ]
                    }
                ],
                "active": True
            }
        }


class UserInDB(User):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")


class UserSkillCategory(BaseModel):
    """
    4 levels for now: beginner , intermediate, advanced, expert
    """
    name: str = Field(...)
    description: str = Field(...)
