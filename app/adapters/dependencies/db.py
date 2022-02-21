from typing import AsyncGenerator

from app.database import get_db_client
from app.repositories.skill import SkillRepository
from app.repositories.user import UserRepository


async def user_repository() -> AsyncGenerator[UserRepository, None]:
    yield UserRepository(db_client_factory=get_db_client,
                         db_name='luso',
                         collection_name='users')


async def skill_repository() -> AsyncGenerator[SkillRepository, None]:
    yield SkillRepository(db_client_factory=get_db_client,
                          db_name='luso',
                          collection_name='skills')
