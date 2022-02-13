from fastapi import APIRouter
from app.adapters.rest.user import base, skill

router = APIRouter(
        tags=['user']
)

router.include_router(
        base.router,
)

router.include_router(
        skill.router,
)
