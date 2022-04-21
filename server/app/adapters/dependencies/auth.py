from typing import List

import structlog
from fastapi import Depends, HTTPException
from fastapi import status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer, SecurityScopes
from jose import JWTError  # type: ignore
from starlette.requests import Request

from server.app.adapters.dependencies.db import user_repository
from server.app.core.auth.auth_service import get_payload
from server.app.core.auth.exceptions import InvalidCredentialsException
from server.app.core.user.model.base import UserRead
from server.app.repositories.user import UserRepository

auth_scheme = HTTPBearer()

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)

log = structlog.get_logger(__name__)


async def get_current_user(
    security_scopes: SecurityScopes,
    request: Request,
    token: HTTPAuthorizationCredentials = Depends(auth_scheme),
    user_repo: UserRepository = Depends(user_repository),
) -> UserRead:
    try:
        payload = await get_payload(token)
        if payload.sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    except InvalidCredentialsException:
        raise credentials_exception

    user = await user_repo.find({"_id": payload.sub})

    if user and len(user) == 1:
        log.info(f"user {user[0].id} scopes:{security_scopes.scopes}")

        check_permission(payload.scopes, security_scopes.scopes, request.path_params)
        return user[0]

    raise credentials_exception


def _map_scope_by_resource(scopes, params):
    resource_action_map = {}
    for scope in scopes:
        resource, action, id_ = scope.split(":")
        log.debug("params", params=params)
        id_ = id_.format(**params)
        if resource in resource_action_map:
            resource_action_map[f"{resource}:{action}"] += [id_]
        else:
            resource_action_map[f"{resource}:{action}"] = [id_]

    return resource_action_map


def check_permission(token_scopes: List[str], required_scopes: List[str], params):
    required_scopes_map = _map_scope_by_resource(required_scopes, params)
    token_scopes_map = _map_scope_by_resource(token_scopes, params)

    log.debug("required scopes", scopes=required_scopes_map)
    log.debug("token scopes", scopes=token_scopes_map)

    for resource_action, ids in required_scopes_map.items():
        if "*" in ids:
            return
        try:
            token_resource_id = token_scopes_map[resource_action]
            if "*" in token_resource_id:
                return
            else:
                for id_ in ids:
                    if id_ in token_resource_id:
                        return

            log.debug("no matching permissions for resource found")

        except KeyError as e:
            log.debug("error when looking for resource and action", error=e)

        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
