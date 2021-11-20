from typing import List, Optional

from bson import ObjectId
from pydantic import BaseModel, Field

from app.models.base import PyObjectId


class User(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    skill: Optional[List[str]]
    active: bool = Field(True)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "first_name": "Darth",
                "last_name": "Vader",
                "skills": [
                    {
                        "skill_id": "000102030406",  # from skill
                        "name": "Apache Airflow",  # from skill
                        "icon_link": "https://link.to.png",  # from skill
                        "tags": ["category:Tools"],  # from skill
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
