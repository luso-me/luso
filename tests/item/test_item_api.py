from fastapi.testclient import TestClient

from app.item.item_api import router

client = TestClient(router)


def test_list_items():
    response = client.get("/items")
    assert response.status_code == 200
