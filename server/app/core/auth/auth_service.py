from datetime import datetime, timedelta

import structlog
from authlib.integrations.httpx_client import AsyncOAuth2Client  # type: ignore
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt, JWTError  # type: ignore

from server.app.config import settings
from server.app.core.auth.exceptions import InvalidCredentialsException
from server.app.core.auth.model.base import JWTPayload

log = structlog.get_logger()

DEFAULT_TTL_MINUTES = 10080  # 7 days


async def create_access_token(
    payload: JWTPayload, ttl: timedelta = timedelta(minutes=DEFAULT_TTL_MINUTES)
) -> str:
    payload.exp = datetime.utcnow() + ttl
    encoded_jwt = jwt.encode(
        claims=payload.dict(exclude_none=True),
        key=settings.token_secret_key,
        algorithm=settings.token_algorithm,
    )
    return encoded_jwt


async def get_payload(token: HTTPAuthorizationCredentials) -> JWTPayload:
    try:
        return JWTPayload.parse_obj(
            jwt.decode(
                token.credentials,
                settings.token_secret_key,
                algorithms=[settings.token_algorithm],
            )
        )
    except JWTError as e:
        log.info(f"Failed to decrypt token with our secret", error=e)
    raise InvalidCredentialsException
