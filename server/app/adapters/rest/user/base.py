from typing import List

import structlog
from fastapi import HTTPException, status, Depends, APIRouter, Security

from server.app.adapters.dependencies.auth import get_current_user, user_repository
from server.app.core.user.model.base import UserCreate, UserUpdate, UserRead
from server.app.core.user.user_service import UserService
from server.app.repositories.user import UserRepository

log = structlog.get_logger()

router = APIRouter(prefix="/users")


@router.post(
    "",
    response_description="Add new user",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(
    user: UserCreate,
    user_repo: UserRepository = Depends(user_repository),
    _: UserRead = Security(get_current_user, scopes=["user:write"]),
):
    return await user_repo.create(user)


@router.get("", response_description="List all users", response_model=List[UserRead])
async def list_users(
    limit: int = 100,
    user_repo: UserRepository = Depends(user_repository),
    _: UserRead = Security(get_current_user, scopes=["user:read:*"]),
):
    return await user_repo.list(limit)


@router.get("/me", response_model=UserRead)
async def read_users_me(
    current_user: UserRead = Security(get_current_user, scopes=["user:read:*"])
):
    return current_user


@router.get(
    "/{user_id}", response_description="Get a single user", response_model=UserRead
)
async def show_user(
    user_id: str,
    user_repo: UserRepository = Depends(user_repository),
    _: UserRead = Security(get_current_user, scopes=["user:read:{user_id}"]),
):
    if (user := await user_repo.get(user_id)) is not None:
        return user

    raise HTTPException(status_code=404, detail=f"user {user_id} not found")


@router.put("/{user_id}", response_description="Update a user", response_model=UserRead)
async def update_user(
    user_id: str,
    user: UserUpdate,
    _: UserRead = Security(get_current_user, scopes=["user:write:{user_id}"]),
    user_service=Depends(UserService),
):
    log.info(f"Attempting to update user: {user}")
    return await user_service.update_user(user_id, user)


@router.delete("/{user_id}", response_description="Delete a user")
async def delete_user(
    user_id: str,
    user_repo: UserRepository = Depends(user_repository),
    _: UserRead = Security(get_current_user, scopes=["user:delete:{user_id}"]),
):
    await user_repo.delete(user_id)
