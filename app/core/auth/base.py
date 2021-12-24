import logging
from datetime import datetime, timedelta

from authlib.integrations.httpx_client import AsyncOAuth2Client  # type: ignore
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError  # type: ignore

from app.config import settings
from app.core.auth.exceptions import InvalidCredentialsException
from app.models.auth import JWTPayload

log = logging.getLogger(__name__)

DEFAULT_TTL_MINUTES = 15


async def create_access_token(payload: JWTPayload, ttl: timedelta = timedelta(DEFAULT_TTL_MINUTES)) -> str:
    payload.exp = datetime.utcnow() + ttl
    encoded_jwt = jwt.encode(
        claims=payload.dict(exclude_none=True),
        key=settings.token_secret_key,
        algorithm=settings.token_algorithm
    )
    return encoded_jwt


async def get_payload(token: HTTPAuthorizationCredentials) -> JWTPayload:
    try:
        return JWTPayload.parse_obj(
            jwt.decode(token.credentials, settings.token_secret_key, algorithms=[settings.token_algorithm]))
    except JWTError as e:
        log.info(f'Failed to decrypt token with our secret', e)
    raise InvalidCredentialsException
