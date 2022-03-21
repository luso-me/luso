import pytest
from httpx import AsyncClient


@pytest.mark.integration
@pytest.mark.asyncio
async def test_root(async_client: AsyncClient):
    response = await async_client.get("/skills/")
    assert response.status_code == 200
    assert response.json() == []
