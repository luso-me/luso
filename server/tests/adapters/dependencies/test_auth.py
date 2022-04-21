import pytest
from fastapi import HTTPException

from server.app.adapters.dependencies.auth import check_permission


def test_check_permissions():

    token_scopes = ["user:read:123", "skill:read:*"]

    check_permission(token_scopes, ["user:read:{user_id}"], {"user_id": "123"})

    check_permission(token_scopes, ["skill:read:test"], {})

    check_permission(token_scopes, ["user:read:*"], {})

    with pytest.raises(HTTPException):
        check_permission(token_scopes, ["skill:write:test"], {})
