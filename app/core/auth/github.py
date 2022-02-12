from typing import Dict, Optional

import httpx
import structlog
from authlib.integrations.httpx_client import AsyncOAuth2Client  # type: ignore
from jose import jwt, JWTError  # type: ignore

from app.config import settings
from app.core.auth.base import create_access_token
from app.core.auth.exceptions import GithubCredentialsException
from app.database import client, get_db_client
from app.core.auth.model import JWTPayload
from app.core.user.model.base import UserRead, UserCreate
from app.repositories.user import UserRepository

log = structlog.get_logger()

github_client = AsyncOAuth2Client(client_id=settings.github_client_id,
                                  client_secret=settings.github_client_secret,
                                  scope='user:email')

user_repo = UserRepository(db_client_factory=get_db_client, db_name='luso', collection_name='users')


def github_login_url():
    auth_url, state = github_client.create_authorization_url(
        url='https://github.com/login/oauth/authorize')
    log.info(f'Github auth url [{auth_url}] state [{state}]')
    # TODO: Do something with state
    return auth_url


async def github_callback(code: str) -> str:
    token = await github_client.fetch_token(
        url='https://github.com/login/oauth/access_token',
        code=code)

    if github_access_token := token.get('access_token'):
        github_user = await get_user_info(access_token=github_access_token)
        user = await get_github_user(github_user)

        jwt_payload = JWTPayload(
            sub=user.id
        )
        return await create_access_token(payload=jwt_payload)
    else:
        raise GithubCredentialsException()


async def get_github_user(github_user):
    users = await user_repo.find({'github_user_id': str(github_user['id'])})

    log.info(f'Github user info {github_user}')

    if len(users) == 0:
        return await github_create_user(github_user)
    elif len(users) == 1:
        return users[0]
    else:
        log.error(f'More than one user found with the same github id users: {users}')
        raise GithubCredentialsException()


async def get_user_info(access_token) -> Dict:
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get('https://api.github.com/user', headers={'Authorization': f'token {access_token}'})

        user_data = resp.json()
        log.info(f'User data {user_data}')

        if user_data.get('email') is None:
            user_data['email'] = await get_user_email(access_token)

        return user_data


async def get_user_email(access_token) -> Optional[str]:
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get('https://api.github.com/user/emails', headers={'Authorization': f'token {access_token}'})

        email_data = resp.json()
        log.info(f'Email data {email_data}')

        primary_emails = list(filter(lambda x: x['primary'], email_data))

        if primary_emails:
            log.info(f'Email addresses found {primary_emails}')
            return primary_emails[0]['email']
        else:
            log.info('No usable emails addresses found')
            return None


async def github_create_user(user_data: dict) -> UserRead:
    log.info(f"Creating new user {user_data}")
    user = UserCreate(
        github_user_id=user_data['id'],
        name=user_data['name'],
        email=user_data['email']
    )
    return await user_repo.create(user)
