import structlog

from app.core.user.model.base import UserUpdate, UserCreate, UserRead
from app.core.user.model.skill_plan import SkillPlan
from app.core.user.model.user_score import UserScore
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

log = structlog.get_logger()


class UserService:
    def __init__(self):
        self.transition_points = {
            ("Todo", "Done"): UserScore(gold=1, points=1),
            ("In progress", "Done"): UserScore(gold=1, points=1),
            ("Done", "In progress"): UserScore(gold=-1, points=-1),
            ("Done", "Todo"): UserScore(gold=-1, points=-1),
        }

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

        self._set_user_points(old_user, user)

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

    def _set_user_points(self, old_user: UserRead, updated_user: UserUpdate):
        updated_user.score = old_user.score

        if old_user.plans == updated_user.plans:
            return

        current_plans = {p.id: p for p in old_user.plans}
        new_plans = {p.id: p for p in updated_user.plans}

        for p_id, p in new_plans.items():
            log.debug(p)
            updated_user.score += self._calculate_user_points(
                current_plans.get(p_id), p
            )

    def _calculate_user_points(
        self, old_skill_plan: SkillPlan, new_skill_plan: SkillPlan
    ):
        if old_skill_plan is None:
            log.debug("skill plan did not exist in db")
            if new_skill_plan.status == "Done":  # use enum?
                log.debug("skill was marked as done")
                return UserScore(gold=1, points=1)
            return UserScore(gold=0, points=0)
        return self._calculate_score(
            old_status=old_skill_plan.status, new_status=new_skill_plan.status
        )

    def _calculate_score(self, old_status: str, new_status: str):
        points = self.transition_points.get((old_status, new_status))
        log.debug(f"transition {old_status} -> {new_status} assigning points {points}")
        if points:
            return points
        else:
            log.debug(
                f"skill plan transition for {old_status} -> {new_status} does not exist"
            )
            return UserScore(gold=0, points=0)
