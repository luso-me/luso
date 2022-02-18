from fastapi import APIRouter

from . import base, skill

router = APIRouter(
        tags=['user'],
        redirect_slashes=False
)

router.include_router(
        base.router,
)

router.include_router(
        skill.router,
)
