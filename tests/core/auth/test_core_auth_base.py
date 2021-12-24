import ast

import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.config import AppSettings
from app.core.auth.base import create_access_token, get_payload
from app.core.auth.exceptions import InvalidCredentialsException
from app.models.auth import JWTPayload
import base64


@pytest.fixture
def app_settings():
    yield AppSettings(
        mongo_connection_url='localhost:27017',
        github_client_id='dne',
        github_client_secret='dne',
        cors_allowed_origins=['http://localhost:7000'],
        token_secret_key='1234',
        token_algorithm='HS256',
    )


@pytest.mark.asyncio
async def test_create_access_token(app_settings):
    payload = JWTPayload(
        sub='test'
    )
    payload.scopes.append('me:read')
    print(payload)
    token = await create_access_token(payload)
    token_parts = token.split('.')
    assert ast.literal_eval(base64.b64decode(token_parts[0]).decode('utf-8')) == {'alg': 'HS256', 'typ': 'JWT'}
    assert token_parts[1] != ''
    assert token_parts[2] != ''


@pytest.mark.asyncio
async def test_get_payload(app_settings):
    cred = HTTPAuthorizationCredentials(
        credentials='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjQxNTY5MjE4LCJzY29wZXMiOlsibWU6cmVhZCJdfQ.KKEH151l-jbFdU0brt8CyQCD3O_So86lKHmKwHX8I0g',
        scheme='Bearer')
    payload = await get_payload(cred)
    assert payload.sub == 'test'
    assert payload.scopes == ['me:read']
    assert isinstance(payload.exp, int)


@pytest.mark.asyncio
async def test_get_payload_invalid(app_settings):
    with pytest.raises(InvalidCredentialsException):
        cred = HTTPAuthorizationCredentials(
            credentials='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjQxNDczNzY4fQ.i61MZ7INrwaxOXnydpp-VTK5hyFxN5gWzVXoH_KNKT0',
            scheme='Bearer')
        await get_payload(cred)
