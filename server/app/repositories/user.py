from typing import Type

from server.app.core.user.model.base import UserCreate, UserRead, UserUpdate
from server.app.repositories.base import BaseRepository


class UserRepository(BaseRepository[UserCreate, UserRead, UserUpdate]):
    @property
    def _read_schema(self) -> Type[UserRead]:
        return UserRead
