from httpx import AsyncClient

import pytest

from app.infrastructure.logger.logger import logger
from app.utils.config import ServicesConfig

host = "http://127.0.0.1:8000"

service_config = ServicesConfig()


@pytest.mark.asyncio
class TestAnalitic:
    PATH = f"{service_config.analytic_service.path}"

    @pytest.mark.parametrize(
        "user1,user2",
        [
            ("floysefake","76561199054741771"),
            ("76561199054741771","floysefake"),
            ("76561199054741771","76561199093545741"),
            ("floysefake","pacukevich")
        ]
    )
    async def test_user_battle(self,login,user1,user2):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}/user_battle",
                                        params={
                                            f"user1_id":user1,
                                            f"user2_id":user2,
                                        }
                                        )

        assert response.status_code == 200 or response.status_code == 502
        if response.status_code == 502:
            assert response.json().get("detail")

    @pytest.mark.parametrize(
        "user1,user2,expected",
        [("54546576543rgrgrer","3454grbgfytyu","Steam user not found")]
    )
    async def test_bad_user_battle(self,login,user1,user2,expected):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}/user_battle",
                                        params={
                                            f"user1_id":f"{user1}",
                                            f"user2_id":f"{user2}",
                                        }
                                        )

        assert response.status_code == 404
        assert response.json()["detail"] == expected

    @pytest.mark.parametrize(
        "user,status_code,expected",
        [
            ("76561199054741771", 200, None),
            ("54546576543rgrgrer",404,"Steam user not found"),
         ]
    )
    async def test_user_score_list(self, login, user, status_code, expected):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}/user_score",
                                        params={
                                            f"user":user,
                                        }
                                        )

        assert response.status_code == status_code
        if expected:
            assert response.json()['detail'] == expected
        else:
            assert isinstance(response.json()["user_rating"],int)

    @pytest.mark.parametrize(
        "user,status_code,expected",
        [("76561199054741771",200,None),
         ("54546576543rgrgrer",404, "Steam user not found"),
         ]
    )
    async def test_user_friends_list(self,login,user,status_code,expected):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}/friends_list",
                                        params={
                                            "user":user,
                                        }
                                        )

        assert response.status_code == status_code or response.status_code == 502
        if response.status_code == status_code:
            if expected:
                assert response.json()['detail'] == expected
            else:
                assert response.json()["friends"] != None

    @pytest.mark.parametrize(
        "new_url,user,status_code,expected",
        [
        ("/games_for_you","76561199054741771",200,None),
         ("/games_for_you","54546576543rgrgrer", 404, "Steam user not found"),
         ("/salling_for_you", "76561199054741771", 200, None),
          ("/salling_for_you", "54546576543rgrgrer", 404, "Steam user not found")
         ]
    )
    @pytest.mark.usefixtures("steamgames","games")
    async def test_block_for_you(self,login,user,status_code,expected,new_url):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}{new_url}",
                                        params={
                                            "user":user,
                                        }
                                        )

        assert response.status_code == status_code or response.status_code == 404
        if expected:
            assert response.json()['detail'] == expected

    async def test_get_free_games(self,login,steamgames):
        new_client = login["client"]
        response = await new_client.get(f"{self.PATH}/free_games")

        assert response.status_code == 200
        if response.json():
            assert response.json() != False

    async def test_bad_free_games(self,login):
        new_client = login["client"]
        response = await new_client.get(f"{self.PATH}/free_games")

        assert response.status_code == 200
        assert response.json()['detail'] == False

    @pytest.mark.parametrize(
        "app_id,steam_id,status_code,expected",
        [
            ("730","76561199054741771",200,None),
            ("760","54546576543rgrgrer", 404, "Steam user not found"),
            ("740", "76561199054741771", 404, None),
            ("745", "54546576543rgrgrer", 404, "Steam user not found")

        ]
    )
    async def test_user_user_achivements(self,login,steam_id,app_id,status_code,expected):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.PATH}/user_achivements",
                                        params={
                                            "app_id":app_id,
                                            "steam_id":steam_id
                                        }
                                        )

        assert response.status_code == status_code
        if expected:
            assert response.json()['detail'] == expected
        else:
            assert response.json() != None


    @pytest.mark.parametrize(
        "url,status_code,expected",
        [
            ("/user_battle?user1_id=76561199667157069&user2_id=76561199054741771",401,"Token not found"),
            ("/user_score?user=76561199054741771", 401, "Token not found"),
            ("/friends_list?user=76561199054741771", 401, "Token not found"),
            ("/games_for_you?user=76561199054741771", 401, "Token not found"),
            ("/salling_for_you?user=76561199054741771", 401, "Token not found"),
            ("/user_achivements?steam_id=760&app_id=76561199054741771", 401, "Token not found"),
            ("/free_games",401,"Token not found")
        ]
    )
    async def test_not_authenticated_endpoints(self,client:AsyncClient,url,status_code,expected):
        response = await client.get(f"{self.PATH}{url}")

        assert response.status_code == status_code
        assert response.json()["detail"] == expected
