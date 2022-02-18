from fastapi import APIRouter

from . import base

router = APIRouter(
        tags=['skills'],
        redirect_slashes=False,
)

router.include_router(
        base.router,
)
