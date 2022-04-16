from pydantic import BaseModel


class UserScore(BaseModel):
    gold: int
    points: int

    def __add__(self, other: "UserScore"):
        self.gold += other.gold
        self.points += other.points
        return self

    def __sub__(self, other: "UserScore"):
        self.gold -= other.gold
        self.points -= other.points
        return self
