from fastapi import APIRouter

from server.app.adapters.rest.auth import github

router = APIRouter(tags=["authentication"], redirect_slashes=False, prefix="/auth")

router.include_router(github.router)
