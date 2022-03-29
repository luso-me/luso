from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from pydantic.fields import Field


class SkillPlanObjective(BaseModel):
    id: str
    resource_id: str
    resource_item_id: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str


class SkillPlan(BaseModel):
    id: str
    plan_name: str
    skill_id: str
    start_date: datetime
    end_date: datetime
    time_horizon: str
    notes: Optional[str]
    status: str
    objectives: List[SkillPlanObjective] = Field(default_factory=list)
