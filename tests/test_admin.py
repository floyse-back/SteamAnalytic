import pytest
from httpx import AsyncClient
from sqlalchemy import select

from app.infrastructure.db.models.users_models import UserModel
from app.utils.config import ServicesConfig

service_config = ServicesConfig()

@pytest.mark.asyncio
@pytest.mark.usefixtures("users")
class TestAdmin:
    PATH = service_config.admin_service.path

    @pytest.mark.parametrize(
        "username,email,status_code,expected",
        [("admin_ivan",None,200,None),
         ("floysefake",None,200,None),
         (None,"ivan.admin@example.com",200,None),
         ("baduser",None,404,"User Not Found"),
         ("ivanka",None,404,"User Not Found"),
         ]
    )
    async def test_user_info(self,login_admin:dict,username,email,status_code,expected):
        new_client = login_admin["client"]
        params = {"email":email} if username == None else {"username": username}
        response = await new_client.get(f"{self.PATH}/user_info",params=params)
        data = response.json()

        assert response.status_code == status_code
        if expected:
            assert data["detail"] == expected
        elif username:
            assert data["username"] == username
        else:
            assert data["email"] == email

    @pytest.mark.parametrize(
        "username,email,status_code,expected",
        [("user_dmytro",None,204,None),
         ("user_artem",None, 204, None),
         (None,"dmytro.user@example.com",204,None),
         ("admin_ivan",None,401,"User not permitions"),
         ("baduser",None,404,"User Not Found"),
         ]
    )
    async def test_user_delete(self,session,login_admin,username,email,status_code,expected):
        new_client = login_admin["client"]
        params = {"email":email} if username == None else {"username": username}
        response = await new_client.delete(f"{self.PATH}/user_delete", params=params)

        assert response.status_code == status_code
        if expected:
            assert response.json()["detail"] == expected
        else:
            async with session() as s:
                user_model = await s.execute(select(UserModel).where(UserModel.username == username))
                assert user_model.scalars().first() is None

    @pytest.mark.parametrize(
        "url,method,status_code,expected",
        [(f"/user_info?username=admin_ivan","GET",401,"Token not found"),
         ("/user_delete?username=user_dmytro","DELETE",401,"Token not found"),
         ]
    )
    async def test_user_not_auth(self,client:AsyncClient,url,method,status_code,expected):
        response = await client.request(method=method,url=f"{self.PATH}{url}")

        assert response.status_code == status_code
        assert response.json()["detail"] == expected

@pytest.mark.asyncio
@pytest.mark.parametrize(
    "username,status_code,expected",
    [("admin_ivan", 401, "User not permitions"),
     ("baduser", 401, "User not permitions"),
     ("ivanka", 401, "User not permitions"),
     ]
)
class TestBadRequest:
    PATH = service_config.admin_service.path

    async def test_bad_user_info(self, login: dict, session, username, status_code, expected):
        new_client = login["client"]

        response = await new_client.get(f"{self.PATH}/user_info", params={"username": username})
        data = response.json()

        assert response.status_code == status_code
        assert data["detail"] == expected

    async def test_bad_user_delete(self,login,session,username,status_code,expected):
        new_client = login["client"]

        response = await new_client.delete(f"{self.PATH}/user_delete", params={"username": username})
        data = response.json()

        assert response.status_code == status_code
        assert data["detail"] == expected