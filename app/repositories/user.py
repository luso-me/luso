from typing import Type

from app.models.user import UserCreate, UserRead, UserUpdate
from app.repositories.base import BaseRepository, READ_SCHEMA


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate]):
    @property
    def _read_schema(self) -> Type[UserRead]:
        return UserRead
