from datetime import datetime

from pydantic import BaseModel


class UserSkillUsed(BaseModel):
    start: datetime
    end: datetime
    location: str
