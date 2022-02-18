from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from app.core.auth import github_service as github_core
from app.core.auth.model.base import Token

router = APIRouter(
    prefix='/github'
)


@router.get('/login')
async def github_login():
    return RedirectResponse(
            github_core.github_login_url(),
            status_code=HTTPStatus.TEMPORARY_REDIRECT
    )


@router.get('/callback')
async def github_callback(code: str) -> Token:
    return Token(access_token=await github_core.github_callback(code=code),
                 token_type='bearer')
