import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Request

from app.infrastructure.db.models.users_models import UserModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("users")
class TestAuth:
    @pytest.mark.parametrize(
        "username,password", [
            ("admin_ivan", "hashedpass1"),
            ("admin_olena", "hashedpass2"),
            ("user_dmytro", "hashedpass3"),
            ("user_maryna", "hashedpass4"),
            ("user_artem", "hashedpass5"),
            ("user_natali", "hashedpass6"),
        ]
    )
    async def test_login_users(self,client:AsyncClient,username,password):
        response = await client.post(
            url=f"/auth/login?username={username}&password={password}",
        )

        data = response.json()
        print(data)
        assert response.status_code == 201
        assert data.get("access_token")
        assert data.get("refresh_token")
        assert data.get("type") == "bearer"

    @pytest.mark.parametrize(
        "username,status_code,password,exception", [
            ("bad_account",404,"password","User Not Found"),
            ("admin_ivan",401,"password","Incorrect password"),
            ("user_dmytro",401,"password","Incorrect password")
        ]
    )
    async def test_not_login_users(self,client:AsyncClient,username,status_code,password,exception):
        response = await client.post(
            url=f"/auth/login?username={username}&password={password}",
        )

        data = response.json()

        assert response.status_code == status_code
        assert data['detail'] == exception

    @pytest.mark.parametrize(
        "username,password,email,steamid", [
            ("admin_ivanchik", "hashedpass1", "floyse.fake@gmail.com", "steamid"),
            ("test_vadym", "hashedpass2", "new_gmail.com", "steamid"),
        ]
    )
    async def test_register_users(self,session:AsyncSession,client:AsyncClient,username,password,email,steamid):
        data = {
            "username": f"{username}",
            "password": f"{password}",
            "email": f"{email}",
            "steamid": f"{steamid}",
        }
        response = await client.post(
            url = "/auth/register_user/",
            json=data
        )
        assert response.status_code == 201

        async with session() as s:
            stmt = await s.execute(
                select(UserModel).where(UserModel.username == f"{username}")
            )
            result = stmt.scalars().first()

        assert result is not None

    @pytest.mark.parametrize(
        "username,password,email,steamid,status_code,exception", [
            ("user_dmytro", "newPassword", "floyse.fake@gmail.com", "steamid",400,"This username is already registered"),
            ("new_user", "hashed", "dmytro.user@example.com", "steamid",400,"This username is already registered"),
        ]
    )
    async def test_bad_register_users(self,session:AsyncSession,client:AsyncClient,username,password,email,steamid,status_code,exception):
        data = {
            "username": f"{username}",
            "password": f"{password}",
            "email": f"{email}",
            "steamid": f"{steamid}",
        }
        response = await client.post(
            url = "/auth/register_user/",
            json=data
        )
        assert response.status_code == status_code
        assert response.json().get("detail") == exception

