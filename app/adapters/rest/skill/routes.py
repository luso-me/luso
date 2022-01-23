from fastapi import APIRouter

from . import base

router = APIRouter(
    tags=['skills']
)

router.include_router(
    base.router,
    prefix='/skills'
)
