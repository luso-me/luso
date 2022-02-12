from datetime import datetime

from pydantic import BaseModel


class UserSkillNote(BaseModel):
    description: str
    date_added: datetime
