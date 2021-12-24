import asyncio
import os
from typing import Generator, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient


TEMP_ENV_VARS = {
    'token_secret_key': 'wqe'
}


def pytest_sessionstart(session):
    # Will be executed before the first test
    old_environ = dict(os.environ)
    os.environ.update(TEMP_ENV_VARS)
    # for env_var in ENV_VARS_TO_SUSPEND:
    #     os.environ.pop(env_var, default=None)

    yield
    # Will be executed after the last test
    os.environ.clear()
    os.environ.update(old_environ)


@pytest.fixture(scope="session")
def event_loop(request) -> Generator:
    """Create an instance of the default event loop for each test case."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture()
def app() -> FastAPI:
    from app.main import app
    return app


@pytest.fixture()
async def async_client(app: FastAPI) -> AsyncGenerator:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac
