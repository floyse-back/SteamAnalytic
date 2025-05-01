import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.infrastructure.db.models.users_models import UserModel


@pytest.mark.asyncio
@pytest.mark.usefixtures("users")
class TestUser:
    base_url = "/users"

    async def test_users_me_get(self,login):
        new_client = login["client"]
        response = await new_client.get(f"{self.base_url}/user_me")

        assert response.status_code == 200
        assert response.json()["username"]
        assert response.json()["email"]
        assert response.json()["steamid"]


    #ПЕРЕРОБИТИ НЕ ПРАЦЮЄ
    async def test_users_me_put(self, login):
        data = {
            "username": "floysefake",
            "email": "new@gmail.com",  # валідний email
            "steamid": "5444565"
        }
        new_client = login["client"]
        headers = {
            "Authorization": f"Bearer {login['access_token']}"
        }

        response = await new_client.put(
            f"{self.base_url}/user_me",
            params={"password": "password"},
            json=data,
            headers=headers
        )

        assert response.status_code == 201


    #Працює але не коректно (сил виправити вже немає)
    #Суть помилки потрібно переробити contest.py users так щоб коли ми створювали користувача створювались і юзери бо відбувається відкат і не працює
    @pytest.mark.parametrize(
        "user,status_code,expected",
        [("floysefake",200,None)]
    )
    async def test_user_profile(self,login,session:async_sessionmaker[AsyncSession],user,status_code,expected):
        new_client = login["client"]

        async with session() as s:
            user_model = await s.execute(select(UserModel).where(UserModel.username==user))
            result = user_model.scalars().first()

        print(result)

        response = await new_client.get(f"{self.base_url}/user_profile/{result.id}")

        assert response.status_code == status_code
        if expected:
            assert response.json()["detail"] == expected

