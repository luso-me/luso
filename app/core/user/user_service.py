from typing import List, Optional, Dict

import structlog

from app.core.user.model.base import UserUpdate, UserCreate, UserRead
from app.core.user.model.skill_plan import SkillPlan, SkillPlanObjective
from app.core.user.model.user_score import UserScore
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

log = structlog.get_logger()


class UserService:
    def __init__(self):
        self.user_repo = UserRepository(
            db_client_factory=get_db_client, db_name="luso", collection_name="users"
        )

    async def create_user(self, user: UserCreate):
        self._set_ids(user)

        await self.user_repo.create(user)

    async def update_user(self, user_id: str, user: UserUpdate):
        old_user = await self.user_repo.get(user_id)

        self._set_ids(user)
        self._remove_scopes(user)

        log.debug(f"updating user points", points=user.score)
        self._set_user_score(old_user, user)
        log.debug(f"updating user points", points=user.score)

        await self.user_repo.update(user_id, user)

    def _remove_scopes(self, user: UserUpdate):
        user.scopes = None

    def _set_ids(self, user):
        if user.plans is not None:
            for plan in user.plans:
                if not plan.id:
                    log.debug(f"plan id missing for user {user.username}")
                    plan.id = BaseRepository.generate_uuid()
                for objective in plan.objectives:
                    if not objective.id:
                        objective.id = BaseRepository.generate_uuid()

    def _set_user_score(self, current_user: UserRead, updated_user: UserUpdate):
        updated_user.score = current_user.score

        current_plan_objective_map = self._generate_plan_objective_map(
            current_user.plans
        )
        updated_plan_objective_map = self._generate_plan_objective_map(
            updated_user.plans
        )

        for updated_plan_id, updated_objectives in updated_plan_objective_map.items():
            current_plan = current_plan_objective_map.get(updated_plan_id)
            if current_plan is None:
                log.debug(f"updated plan does not exist in db", plan_id=updated_plan_id)
                continue

            self._calculate_and_update_user_score(
                updated_objectives, current_plan, updated_user
            )

    def _calculate_and_update_user_score(
        self, updated_objectives, current_plan, updated_user
    ):
        for updated_objective_id, updated_objective in updated_objectives.items():
            current_objective = current_plan.get(updated_objective_id)
            if current_objective is None:
                log.debug(
                    "updated plan objective does not exist in db",
                    objective=updated_objective,
                )

            updated_user.score += self._calculate_user_points(
                current_objective, updated_objective
            )

    def _generate_plan_objective_map(self, user_plan: List[SkillPlan]):
        plan_objective_map: Dict[str, dict] = {}
        for up in user_plan:
            plan_objective_map[up.id] = {}
            for obj in up.objectives:
                plan_objective_map[up.id][obj.id] = obj
        return plan_objective_map

    def _calculate_user_points(
        self,
        current_objective: SkillPlanObjective,
        update_objective: SkillPlanObjective,
    ) -> UserScore:
        if current_objective is None:
            return self._calculate_score(
                current_status=None, updated_status=update_objective.status
            )
        return self._calculate_score(
            current_status=current_objective.status,
            updated_status=update_objective.status,
        )

    def _calculate_score(
        self, current_status: Optional[str], updated_status: str
    ) -> UserScore:
        points = UserScore(gold=0, points=0)
        if current_status == "Done":
            points += UserScore(gold=-1, points=-1)

        if updated_status == "Done":
            points += UserScore(gold=1, points=1)
        log.debug(
            f"calculating score for {current_status} -> {updated_status} score {points}"
        )

        return points
