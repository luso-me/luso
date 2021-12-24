import logging
from typing import Dict

import httpx
from authlib.integrations.httpx_client import AsyncOAuth2Client  # type: ignore
from jose import jwt, JWTError  # type: ignore

from app.config import settings
from app.core.auth.exceptions import GithubCredentialsException
from app.models.user import UserRead, UserCreate
from app.repositories.user import UserRepository

log = logging.getLogger(__name__)

github_client = AsyncOAuth2Client(client_id=settings.github_client_id,
                                  client_secret=settings.github_client_secret,
                                  scope='user:email')


def github_login_url():
    auth_url, state = github_client.create_authorization_url(
        url='https://github.com/login/oauth/authorize')
    log.info(f'Github auth url [{auth_url}] state [{state}]')
    # TODO: Do something with state
    return auth_url


async def github_callback(code: str) -> Dict:
    token = await github_client.fetch_token(
        url='https://github.com/login/oauth/access_token',
        code=code)

    if access_token := token.get('access_token'):
        return await get_user_info(access_token=access_token)
    else:
        raise GithubCredentialsException()


async def get_user_info(access_token):
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get('https://api.github.com/user', headers={'Authorization': f'token {access_token}'})

        user_data = await resp.json()
        log.info(f'User data {user_data}')

        if user_data.get('email') is None:
            user_data['email'] = await get_user_email(access_token)

        return user_data


async def get_user_email(access_token):
    async with httpx.AsyncClient() as http_client:
        resp = await http_client.get('https://api.github.com/user/emails', headers={'Authorization': f'token {access_token}'})

        email_data = await resp.json()
        log.info(f'Email data {email_data}')

        primary_emails = list(filter(lambda x: x['primary'], email_data))
        print(primary_emails)

        if primary_emails:
            log.info('No usable emails addresses found')
            return None
        else:
            log.info(f'Email addresses found {primary_emails}')
            return primary_emails[0]


async def github_create_user(user_data: dict, user_repo: UserRepository) -> UserRead:
    log.info(f"Creating new user {user_data}")
    user = UserCreate(
        github_user_id=user_data['id'],
        name=user_data['name'],
    )
    return await user_repo.create(user)
