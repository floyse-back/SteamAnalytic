import pytest
from httpx import AsyncClient
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.db.models.users_models import UserModel
from app.utils.utils import verify_password


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
            ("admin_ivanchikes", "hashedpass1", "floyse.fake@gmail.com", "65465543"),
            ("user_artemxs","hashedpass4","artemxs.user@example.com","432432"),
            ("test_vadymit", "hashedpass2", "new_test@_gmail.com", "65543534"),
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
            ("user_dmytro", "newPassword", "floyse.fake@gmail.com", "steamid",401,"User email or username already exists"),
            ("new_user", "hashed", "dmytro.user@example.com", "steamid",401,"User email or username already exists"),
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

    async def test_delete_users(self,login:dict,create_tokens,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.delete(
            url=f"/auth/delete_user/{create_tokens['delete_token']}",
            params={"password":"password"}
        )

        assert response.status_code == 204
        assert new_client.cookies.get("access_token") is None
        assert new_client.cookies.get("refresh_token") is None

        async with session() as s:
            stmt = await s.execute(
                select(UserModel).where(UserModel.username == f"floysefake")
            )
            result = stmt.scalars().first()

        assert result is None

    async def test_incorrect_password_delete_users(self,login:AsyncClient,create_tokens,session:AsyncSession):
        new_client = login["client"]
        response = await new_client.delete(
            url=f"/auth/delete_user/{create_tokens['delete_token']}",
            params={"password":"bad_password"}
        )

        assert response.status_code == 401
        assert response.json().get("detail") == "Incorrect password"
        assert new_client.cookies.get("access_token") is not None
        assert new_client.cookies.get("refresh_token") is not None

    @pytest.mark.parametrize(
        "token_type,status_code,password,excepted",
        [
            ("verify_token",401,"password","Token not found"),
            ("forgot_password",401,"password","Token not found"),
        ]
    )
    async def test_bad_create_tokens(self,login:dict,create_tokens,session:AsyncSession,token_type,status_code,password,excepted):
        new_client = login["client"]
        response = await new_client.delete(
            url=f"/auth/delete_user/{create_tokens[f'{token_type}']}",
            params={"password":f"{password}"}
        )

        assert response.status_code == status_code
        assert response.json().get("detail") == excepted


    async def test_not_auth_delete_users(self,client:AsyncClient,create_tokens):
        response = await client.delete(
            url=f"/auth/delete_user/{create_tokens['delete_token']}",
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
        print(login["access_token"])
        response = await new_client.post("/auth/refresh_token")

        data = response.json()
        assert response.status_code == 201
        assert response.cookies.get("access_token") is not None
        assert data["refresh_token"] is not None

    async def test_not_refresh_token(self,client:AsyncClient):
        response = await client.post("/auth/refresh_token")

        assert response.status_code == 401
        assert response.json().get("detail") == "Token not found"

    @pytest.mark.parametrize(
        "token_type,status_code,password,excepted",
        [
        ("verify_token",401,"password","Token not found"),
        ("delete_token",401,"password","Token not found"),
        ("forgot_password",204,"new_password",None)
        ]
    )
    async def test_forgot_password(self,login:dict,session,create_tokens:dict,token_type,status_code,password,excepted):
        new_client = login["client"]
        response = await new_client.put(
            url=f"/auth/forgot_password/{create_tokens[f'{token_type}']}",
            params = {"new_password":f"{password}"}
        )

        assert response.status_code == status_code
        if excepted:
            assert response.json().get("detail") == excepted
        else:
            async with session() as s:
                stmt = await s.execute(select(UserModel).filter(UserModel.username == login["username"]))
                result = stmt.scalars().first()

                assert verify_password(password=password,hashed_password=result.hashed_password)

    @pytest.mark.parametrize(
            "token_type,status_code,excepted",
            [
            ("verify_token",200,None),
            ("delete_token",401,"Token not found"),
            ("forgot_password",401,"Token not found")
            ]
        )
    async def test_verify_email(self,login:dict,session,create_tokens:dict,token_type,status_code,excepted):
        new_client = login["client"]
        response = await new_client.get(
            url=f"/auth/verify_email/{create_tokens[f'{token_type}']}",
        )

        assert response.status_code == status_code
        if excepted:
            assert response.json().get("detail") == excepted
        else:
            async with session() as s:
                stmt = await s.execute(select(UserModel).filter(UserModel.username == login["username"]))
                result = stmt.scalars().first()

                assert result.is_active == True
