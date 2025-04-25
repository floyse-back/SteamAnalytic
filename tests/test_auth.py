import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

    async def test_delete_users(self,login:AsyncClient,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.delete(
            url=f"/auth/delete_user",
            params={"password":"password"}
        )

        assert response.status_code == 204
        assert new_client.cookies.get("access_token") is None
        assert new_client.cookies.get("refresh_token") is None

        async with session() as s:
            stmt = await s.execute(
                select(UserModel).where(UserModel.username == f"")
            )
            result = stmt.scalars().first()

        assert result is None

    async def test_incorrect_password_delete_users(self,login:AsyncClient,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.delete(
            url=f"/auth/delete_user",
            params={"password":"bad_password"}
        )

        assert response.status_code == 401
        assert response.json().get("detail") == "Incorrect password"
        assert new_client.cookies.get("access_token") is not None
        assert new_client.cookies.get("refresh_token") is not None


    async def test_not_auth_delete_users(self,client:AsyncClient):
        response = await client.delete(
            url=f"/auth/delete_user",
            params={"password":"password"}
        )

        assert response.status_code == 401
        assert response.json().get("detail") == "User Not Authorized"

    async def test_logout_users(self,login:dict,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.get("/auth/logout/")

        assert response.status_code == 204
        assert new_client.cookies.get("access_token") is None
        assert new_client.cookies.get("refresh_token") is None

    async  def test_not_auth_logout_users(self,client:AsyncClient):
        response = await client.get("/auth/logout/")

        assert response.status_code == 401
        assert response.json().get("detail") == "Could not validate credentials"

    async def test_refresh_token(self,login:dict,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.post("/auth/refresh_token")

        print(login["access_token"])

        assert response.status_code == 201
        assert response.json().get("access_token") != login["access_token"]
        assert response.json().get("refresh_token") is not None

    async def test_not_refresh_token(self,client:AsyncClient):
        response = await client.post("/auth/refresh_token")

        assert response.status_code == 401
        assert response.json().get("detail") == "Token not found"
