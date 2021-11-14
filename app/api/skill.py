import logging
from http import HTTPStatus
from typing import List, Optional
from uuid import UUID

from fastapi import HTTPException, status, APIRouter
from fastapi.responses import Response

import app.repositories.skill as skill_crud
from app.schema.skill import Skill

log = logging.getLogger(__name__)

router = APIRouter(
    tags=["skill"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_description="Add new skill", response_model=Skill, status_code=status.HTTP_201_CREATED)
async def create_skill(skill: Skill):
    log.debug(f"attempting to create skill with body {skill}")
    new_skill = await skill_crud.insert_skill(skill)
    return new_skill


@router.get("/", response_description="List all skills", response_model=List[Skill])
async def list_skills(limit: int = 100):
    return await skill_crud.find_skills(limit)


@router.get("/find", response_description="Find skill by...", response_model=List[Skill])
async def find_query(skill_name: Optional[str] = None, limit: int = 10):
    if skill_name:
        return await skill_crud.find_by_name(skill_name, limit)

    raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="No known search parameter passed")


@router.get("/{skill_id}", response_description="Get a single skill", response_model=Skill)
async def show_skill(skill_id: UUID):
    if (skill := await skill_crud.find_by_id(skill_id)) is not None:
        return skill

    raise HTTPException(status_code=404, detail=f"skill {skill_id} not found")


@router.put("/{skill_id}", response_description="Update a skill", response_model=Skill)
async def update_skill(skill_id: UUID, skill: Skill):
    if update_result := await skill_crud.update_one(skill_id, skill):
        if update_result.matched_count == 1:
            return await skill_crud.find_by_id(skill_id)

    raise HTTPException(status_code=404, detail=f"skill {skill_id} not found")


@router.delete("/{skill_id}", response_description="Delete a skill")
async def delete_skill(skill_id: UUID):
    delete_result = await skill_crud.delete_one(skill_id)

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"skill {skill_id} not found")
