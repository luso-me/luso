from fastapi import APIRouter
from . import github

router = APIRouter(
    tags=['authentication']
)

router.include_router(
    github.router,
    prefix='/github'
)
