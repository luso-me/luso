from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class SkillPlanObjective(BaseModel):
    id: str
    resource_id: str
    resource_name: str
    resource_web_link: str
    resource_item_id: str
    resource_item_name: str
    resource_item_web_link: Optional[str]
    duration: str
    start_date: Optional[datetime]
    end_date: Optional[datetime]
    status: str


class SkillPlan(BaseModel):
    id: str
    plan_name: str
    skill_id: str
    skill_name: str
    web_link: str
    start_date: datetime
    end_date: datetime
    time_horizon: str
    notes: Optional[str]
    status: str
    objectives: List[SkillPlanObjective]
