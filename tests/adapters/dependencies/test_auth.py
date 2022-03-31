from app.adapters.dependencies.auth import check_permission
from app.core.user.model.base import UserRead


def test_check_permissions():

    token_scopes = ["user:*"]
    required_scopes = ["user:read", "user:write"]

    check_permission(token_scopes, required_scopes)
