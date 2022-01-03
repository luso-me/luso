from typing import AsyncGenerator

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import status
from jose import JWTError  # type: ignore

from app.core.auth.base import get_payload
from app.core.auth.exceptions import InvalidCredentialsException
from app.database import get_db_client
from app.models.user import UserRead
from app.repositories.user import UserRepository

auth_scheme = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def user_repository() -> AsyncGenerator[UserRepository, None]:
    yield UserRepository(db_client_factory=get_db_client, db_name='luso', collection_name='users')


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        user_repo: UserRepository = Depends(user_repository)) -> UserRead:

    try:
        payload = await get_payload(token)
        if payload.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except InvalidCredentialsException:
        raise credentials_exception

    user = await user_repo.find({'_id': payload.sub})
    if user and len(user) == 1:
        return user[0]

    raise credentials_exception
