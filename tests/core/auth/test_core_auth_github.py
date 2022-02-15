from unittest.mock import patch, AsyncMock
from urllib.parse import urlparse, parse_qs

import pytest

from app.adapters.rest.auth import github
from app.core.auth import github_service
from app.core.auth.exceptions import GithubCredentialsException


class MockGettableDict(dict):
    __getattr__, __setattr__ = dict.get, dict.__setitem__


def test_github_login():
    url = urlparse(github_service.github_login_url())
    query_data = parse_qs(url.query)
    assert query_data.get('scope') == ['user:email']


@pytest.mark.asyncio
async def test_github_callback():
    with patch('app.core.auth.github.github_client.fetch_token',
               new=AsyncMock()) as fetch_token_patch, \
            patch('app.core.auth.github.get_user_info') as get_user_info_patch, \
            patch('app.core.auth.github.get_github_user',
                  new=AsyncMock()) as get_github_user_patch:
        fetch_token_patch.return_value = {
            'access_token': '123'
        }
        get_github_user_patch.return_value = MockGettableDict(id=1)

        token = await github.github_callback("some code")

        assert fetch_token_patch.call_count == 1

        assert get_user_info_patch.call_count == 1
        args, kwargs = get_user_info_patch.call_args_list[0]
        assert kwargs['access_token'] == '123'

        assert token


@pytest.mark.asyncio
async def test_github_callback_no_token():
    with pytest.raises(GithubCredentialsException):
        with patch('app.core.auth.github.github_client.fetch_token',
                   new=AsyncMock()) as fetch_token_patch, \
                patch('app.core.auth.github.get_user_info') as get_user_info_patch:
            fetch_token_patch.return_value = {
                'access_token': None
            }

            await github.github_callback("some code")
