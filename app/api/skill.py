import logging
from http import HTTPStatus
from typing import List, Optional

from fastapi import HTTPException, status, APIRouter

import app.repositories.skill as skill_crud
from app.database import client
from app.models.skill import SkillCreate, SkillRead, SkillUpdate

log = logging.getLogger(__name__)

router = APIRouter(
    tags=["skill"],
    responses={404: {"description": "Not found"}},
)

skill_repository = skill_crud.SkillRepository(db_session=client, db_name='luso', collection='skill')


@router.post("/", response_description="Add new skill", response_model=SkillRead, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: SkillCreate):
    log.debug(f"attempting to create skill with body {skill}")
    return await skill_repository.create(skill)


@router.get("/", response_description="List all skills", response_model=List[SkillRead])
async def list_skills(limit: int = 100):
    return await skill_repository.list(limit)


@router.get("/find", response_description="Find skill by...", response_model=List[SkillRead])
async def find_query(skill_name: Optional[str] = None, limit: int = 10):
    if skill_name:
        return await skill_repository.find({'name': skill_name})

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No known search parameter passed")


@router.get("/{skill_id}", response_description="Get a single skill", response_model=SkillRead)
async def show_skill(skill_id: str):
    if (skill := await skill_repository.get(skill_id)) is not None:
        return skill

    raise HTTPException(status_code=404, detail=f"skill {skill_id} not found")


@router.put("/{skill_id}", response_description="Update a skill", response_model=SkillRead)
async def update_skill(skill_id: str, skill: SkillUpdate):
    return await skill_repository.update(skill_id, skill)


@router.delete("/{skill_id}", response_description="Delete a skill")
async def delete_skill(skill_id):
    await skill_repository.delete(skill_id)
