from structlog import get_logger
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.adapters.dependencies.auth import user_repository
from app.core.user.model.base import UserUpdate
from app.core.user.model.user_skill import UserSkill
from app.repositories.user import UserRepository

router = APIRouter()

log = get_logger(__name__)


@router.get('/{user_id}/skills', response_model=List[UserSkill])
async def get_user_skills(user_id: str, user_repo: UserRepository = Depends(user_repository)):
    user = await user_repo.find({'_id': user_id})

    if len(user) == 1:
        return user[0].skills
    else:
        log.error(f'Duplicate user found with id {user_id}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)


@router.post('/{user_id}/skills', response_model=List[UserSkill])
async def add_user_skills(user_id: str, user_skills: List[UserSkill], user_repo: UserRepository = Depends(user_repository)):
    user = await user_repo.find({'_id': user_id})

    if user:
        if len(user) == 1:
            update_user = UserUpdate.parse_obj(user[0])
            update_user.skills = user_skills
            await user_repo.update(user_id, update_user)
            return user_skills
        else:
            log.error('user_id corresponded to more than one user', user_id=user_id)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
