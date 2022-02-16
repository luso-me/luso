import structlog

from app.core.user.model.base import UserCreate, UserUpdate
from app.database import get_db_client
from app.repositories.base import BaseRepository
from app.repositories.user import UserRepository

log = structlog.get_logger()

user_repo = UserRepository(db_client_factory=get_db_client,
                           db_name='luso',
                           collection_name='users')


def create_user(user: UserCreate):
    pass


async def update_user(user_id: str, user: UserUpdate):
    for plan in user.plans:
        if not plan.id:
            log.debug(f'plan id missing for user {user.username}')
            plan.id = BaseRepository.generate_uuid()

    await user_repo.update(user_id, user)


def delete_user(user_id: str):
    pass


def get_user(user_id: str):
    pass


def add_user_skill(user_id, user_skill):
    pass
