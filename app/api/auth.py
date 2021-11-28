import http
from datetime import datetime, timedelta
from typing import Optional

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client  # type: ignore
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from fastapi.responses import RedirectResponse
from jose import jwt, JWTError  # type: ignore
from fastapi import status

from app.config import settings
from app.database import client
from app.models.auth import TokenData, Token
from app.models.user import UserRead
from app.repositories.user import UserRepository

SECRET_KEY = ""
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
        tags=["authentication"],
)

github_client = AsyncOAuth2Client(client_id=settings.github_client_id,
                                  client_secret=settings.github_client_secret,
                                  scope='user:email')

auth_scheme = HTTPBearer()


async def user_repository():
    yield UserRepository(db_session=client, db_name='luso', collection='users')


@router.get('/github')
async def github_login():
    auth_url, state = github_client.create_authorization_url(
            url='https://github.com/login/oauth/authorize')
    return RedirectResponse(url=auth_url,
                            status_code=http.HTTPStatus.TEMPORARY_REDIRECT)


@router.get('/github/callback')
async def auth_callback(code: str,
                        user_repo: UserRepository = Depends(
                                user_repository)) -> Token:
    token = await github_client.fetch_token(
            url='https://github.com/login/oauth/access_token',
            code=code)
    print(token)

    async with httpx.AsyncClient() as http_client:
        user_data = (await http_client.get(
                'https://api.github.com/user',
                headers={'Authorization': f'token {token.get("access_token")}'}
        )).json()
        print(user_data)
        username = user_data['login']
        user = await user_repo.find({"username": username})

        if not user:
            raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Incorrect username or password",
                    headers={"WWW-Authenticate": "Bearer"},
            )

        if len(user) > 1:
            raise HTTPException(
                    status_code=500,
                    detail="More than one user found"
            )

        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
                data={"sub": user[0].username},
                expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type='bearer')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
        token: HTTPAuthorizationCredentials = Depends(auth_scheme),
        user_repo: UserRepository = Depends(user_repository)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY,
                             algorithms=[ALGORITHM])
        print(payload)
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = await user_repo.find({'username': token_data.username})
    if user is None or len(user) > 1:
        raise credentials_exception
    return user[0]


@router.get("/users/me/", response_model=UserRead)
async def read_users_me(current_user: UserRead = Depends(get_current_user)):
    return current_user
