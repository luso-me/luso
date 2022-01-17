import logging
from typing import List

from fastapi import APIRouter, Depends
from fastapi import HTTPException, status

from app.adapters.dependencies.auth import user_repository
from app.core.user.model.user_skill import UserSkill
from app.repositories.user import UserRepository

router = APIRouter()

log = logging.getLogger(__name__)


@router.get('/{user_id}/skills', response_model=List[UserSkill])
async def get_user_skills(user_id: str, user_repo: UserRepository = Depends(user_repository)):
    user = await user_repo.find({'_id': user_id})

    if len(user) == 1:
        if user[0].skills:
            return user[0].skills
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    else:
        log.error(f'Duplicate user found with id {user_id}')
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)
