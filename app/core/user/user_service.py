import structlog

from app.core.user.model.base import UserUpdate
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

log = structlog.get_logger()

user_repo = UserRepository(
    db_client_factory=get_db_client, db_name="luso", collection_name="users"
)


async def update_user(user_id: str, user: UserUpdate):
    if user.plans is not None:
        for plan in user.plans:
            if not plan.id:
                log.debug(f"plan id missing for user {user.username}")
                plan.id = BaseRepository.generate_uuid()
            for objective in plan.objectives:
                if not objective.id:
                    objective.id = BaseRepository.generate_uuid()

    await user_repo.update(user_id, user)
