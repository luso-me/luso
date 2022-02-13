from fastapi import APIRouter

from app.adapters.rest.auth import github

router = APIRouter(
        tags=['authentication']
)

router.include_router(
        github.router,
        prefix='/github'
)
