from http import HTTPStatus
from typing import List, Optional

import structlog
from fastapi import (
    Form,
    File,
    HTTPException,
    status,
    APIRouter,
    Depends,
    UploadFile,
    Security,
)

from app.adapters.dependencies.auth import get_current_user
from app.core.skill.model.base import SkillCreate, SkillRead, SkillUpdate
from app.core.skill.skill_service import SkillService
from app.core.user.model.base import UserRead

log = structlog.get_logger()

router = APIRouter(prefix="/skills")


@router.post(
    "",
    response_description="Add new skill",
    response_model=SkillRead,
    status_code=status.HTTP_201_CREATED,
)
async def create_skill(
    skill: SkillCreate,
    _: UserRead = Security(get_current_user, scopes=["skill:write:*"]),
    skill_service: SkillService = Depends(SkillService),
):
    log.debug(f"attempting to create skill with body {skill}")
    return await skill_service.create_skill(skill)


@router.get(
    "",
    response_description="List all skills",
    response_model=List[SkillRead],
)
async def list_skills(
    limit: int = 100,
    skill_service: SkillService = Depends(SkillService),
    _: UserRead = Security(get_current_user, scopes=["skill:read:*"]),
):
    skills = await skill_service.list_skills(limit)
    log.debug("skills found", skills=skills)
    return skills


@router.get(
    "/find", response_description="Find skill by...", response_model=List[SkillRead]
)
async def find_query(
    skill_name: Optional[str] = None,
    limit: int = 10,
    skill_service: SkillService = Depends(SkillService),
    _: UserRead = Security(get_current_user, scopes=["skill:read:*"]),
):
    if skill_name:
        log.info("searching for skills with name", skill_name=skill_name)
        return await skill_service.find_skill(skill_name, limit)

    raise HTTPException(
        status_code=HTTPStatus.BAD_REQUEST, detail="No known search parameter passed"
    )


@router.get(
    "/{skill_id}", response_description="Get a single skill", response_model=SkillRead
)
async def show_skill(
    skill_id: str,
    skill_service: SkillService = Depends(SkillService),
    _: UserRead = Security(get_current_user, scopes=["skill:read:{skill_id}"]),
):
    if (skill := await skill_service.get_skill(skill_id)) is not None:
        return skill

    raise HTTPException(status_code=404, detail=f"skill {skill_id} not found")


@router.put(
    "/{skill_id}", response_description="Update a skill", response_model=SkillRead
)
async def update_skill(
    skill_id: str,
    skill: SkillUpdate,
    skill_service: SkillService = Depends(SkillService),
    _: UserRead = Security(get_current_user, scopes=["skill:write:{skill_id}"]),
):
    return await skill_service.update_skill(skill_id, skill)


@router.delete(
    "/{skill_id}",
    response_description="Delete a skill",
    status_code=HTTPStatus.NO_CONTENT,
)
async def delete_skill(
    skill_id,
    skill_service: SkillService = Depends(SkillService),
    _: UserRead = Security(get_current_user, scopes=["skill:delete:{skill_id}"]),
):
    await skill_service.delete_skill(skill_id)


@router.post("/{skill_id}/icon")
async def skill_icon_upload(
    skill_id: str,
    skill_name: str = Form(...),
    file: UploadFile = File(...),
    _: UserRead = Security(get_current_user, scopes=["skill:write:{skill_id}"]),
    skill_service: SkillService = Depends(SkillService),
):
    log.info(f"Received icon [{file.filename}] for skill [{skill_name}] upload.")
    return await skill_service.update_skill_icon(
        skill_id, skill_name, file.filename, file.file
    )
