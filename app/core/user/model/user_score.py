from pydantic import BaseModel


class UserScore(BaseModel):
    gold: int
    points: int
