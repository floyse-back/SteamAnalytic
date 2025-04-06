import pytest
from httpx import AsyncClient,ASGITransport

from app.infrastructure.db.repository import get_async_db
from app.main import app
from tests.conftest import override_get_db


app.dependency_overrides[get_async_db] = override_get_db

@pytest.mark.asyncio
async def test_client_auth():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        response = await ac.get("/auth/test")

    assert response.status_code == 200
    assert response.json() == {}

@pytest.mark.asyncio
async def test_create_token(register_user):
    # Переозначення залежностей
    user = await register_user  # Дочікуємося результату фікстури

    data = {
        "username": user.username,
        "password": app.utils.utils.hashed_password
    }

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/auth/login", json=data)

    assert response.status_code == 201

    # Після тесту відновлюємо залежності

@pytest.mark.asyncio
def test_token_bug():
    pass

