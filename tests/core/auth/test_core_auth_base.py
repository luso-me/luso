import ast
from datetime import datetime, timezone

import pytest
from fastapi.security import HTTPAuthorizationCredentials

from app.core.auth.base import create_access_token, get_payload
from app.core.auth.exceptions import InvalidCredentialsException
from app.core.auth.model import JWTPayload
import base64


@pytest.fixture
async def jwt_token():
    payload = JWTPayload(
        sub='test'
    )
    payload.scopes.append('me:read')
    yield await create_access_token(payload)


@pytest.mark.asyncio
async def test_create_access_token(jwt_token):
    token_parts = jwt_token.split('.')
    assert ast.literal_eval(base64.b64decode(token_parts[0]).decode('utf-8')) == {'alg': 'HS256', 'typ': 'JWT'}
    assert token_parts[1] != ''
    assert token_parts[2] != ''


@pytest.mark.asyncio
async def test_get_payload(jwt_token):
    cred = HTTPAuthorizationCredentials(
        credentials=jwt_token,
        scheme='Bearer')
    payload = await get_payload(cred)
    assert payload.sub == 'test'
    assert payload.scopes == ['me:read']
    assert payload.exp > datetime.utcnow().astimezone(tz=timezone.utc)


@pytest.mark.asyncio
async def test_get_payload_expired():
    cred = HTTPAuthorizationCredentials(
        credentials='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjowLCJzY29wZXMiOlsibWU6cmVhZCJdfQ.5g1ixq_2ZZOwkCvaMNDBLmM0m7IkCAud_Kb8yx-g9XM',
        scheme='Bearer')
    with pytest.raises(InvalidCredentialsException):
        await get_payload(cred)


@pytest.mark.asyncio
async def test_get_payload_invalid():
    with pytest.raises(InvalidCredentialsException):
        cred = HTTPAuthorizationCredentials(
            credentials='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0IiwiZXhwIjoxNjQxNDczNzY4fQ.i61MZ7INrwaxOXnydpp-VTK5hyFxN5gWzVXoH_KNKT0',
            scheme='Bearer')
        await get_payload(cred)
