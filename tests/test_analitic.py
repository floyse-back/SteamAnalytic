from httpx import AsyncClient

import pytest

host = "http://127.0.0.1:8000"

@pytest.mark.asyncio
class TestAnalitic:
    base_url = f"/api/v1/analytics"

    @pytest.mark.parametrize(
        "user1,user2",
        [
            ("floysefake","76561199054741771"),
            ("76561199054741771","floysefake"),
            ("76561199054741771","76561199190491252"),
            ("floysefake","pacukevich")
        ]
    )
    async def test_user_battle(self,login,user1,user2):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.base_url}/user_battle",
                                        params={
                                            f"user1_id":user1,
                                            f"user2_id":user2,
                                        }
                                        )

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "user1,user2,expected",
        [("54546576543rgrgrer","3454grbgfytyu","Steam user not found")]
    )
    async def test_bad_user_battle(self,login,user1,user2,expected):
        new_client = login["client"]
        response = await new_client.get(url=f"{self.base_url}/user_battle",
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
        response = await new_client.get(url=f"{self.base_url}/user_score",
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
        response = await new_client.get(url=f"{self.base_url}/friends_list",
                                        params={
                                            "user":user,
                                        }
                                        )

        assert response.status_code == status_code
        if expected:
            assert response.json()['detail'] == expected
        else:
            assert response.json()["friends"] != None


    @pytest.mark.parametrize(
        "url,status_code,expected",
        [
            ("/user_battle?user1_id=76561199667157069&user2_id=76561199054741771",401,"Token not found"),
            ("/user_score?user=76561199054741771", 401, "Token not found"),
            ("/friends_list?user=76561199054741771", 401, "Token not found"),
            ("/games_for_you?user=76561199054741771", 401, "Token not found"),
            ("/salling_for_you?user=76561199054741771", 401, "Token not found"),
            ("/user_achivements?steam_id=760&app_id=76561199054741771", 401, "Token not found"),
        ]
    )
    async def test_not_authenticated_endpoints(self,client:AsyncClient,url,status_code,expected):
        response = await client.get(f"{self.base_url}{url}")

        assert response.status_code == status_code
        assert response.json()["detail"] == expected
