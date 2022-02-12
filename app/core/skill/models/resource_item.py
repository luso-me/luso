from pydantic import BaseModel


class SkillResourceItem(BaseModel):
    id: str
    name: str
    summary: str
    duration: int
