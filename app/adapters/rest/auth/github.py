from http import HTTPStatus

from fastapi import APIRouter

from app.models.auth import Token
from app.core.auth import github as github_core
from fastapi.responses import RedirectResponse


router = APIRouter()


@router.get('/login')
async def github_login():
    return RedirectResponse(
        github_core.github_login_url(),
        status_code=HTTPStatus.TEMPORARY_REDIRECT
    )


@router.get('/callback')
async def github_callback(code: str, state: str) -> Token:
    return Token(access_token=await github_core.github_callback(code=code), token_type='bearer')
