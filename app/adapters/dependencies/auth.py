from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError    # type: ignore

from app.adapters.dependencies.db import user_repository
from app.core.auth.auth_service import get_payload
from app.core.auth.exceptions import InvalidCredentialsException
from app.core.user.model.base import UserRead
from app.repositories.user import UserRepository

auth_scheme = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


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
