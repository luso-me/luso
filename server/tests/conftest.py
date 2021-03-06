import asyncio
from typing import Generator, AsyncGenerator

import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from pytest import MonkeyPatch

mp = MonkeyPatch()
mp.setenv("TOKEN_SECRET_KEY", "123")
mp.setenv("ICONS_S3_BUCKET", "some-bucket")
mp.setenv("ICONS_S3_BUCKET_REGION", "some-region")


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
