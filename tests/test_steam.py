import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
class TestUsersFullStats:
    base_url = "/api/v1/steam/users_full_stats/"
    @pytest.mark.parametrize(
        "user, status_code,expected",[
            ("floysefake",200,None),
            ("76561199054741771", 200,None),
            ("ytgfdbltootpphrhtrhltfbflgf",404,"Steam user not found"),
            ("765611990544643434",404,"Steam user not found"),
        ]
    )
    async def test_default_request(self,client:AsyncClient,user,status_code,expected):
        response = await client.get(f"{self.base_url}{user}")

        assert response.status_code == status_code

        if not expected:
            data:dict = response.json()
            assert data.get("user_data")["player"]
            assert data.get("user_friends_list")
            assert data.get("user_badges")
            assert data.get("user_games")
        else:
            assert response.json() == {"detail": expected}

    @pytest.mark.parametrize(
        "user,status_code,user_badges,friends_details,user_games",
        [
        ("76561199054741771", 200, "false", "false", "false"),
        ("76561199054741771", 200, "false", "false", "true"),
        ("76561199054741771", 200, "false", "true", "false"),
        ("76561199054741771", 200, "false", "true", "true"),
        ("76561199054741771", 200, "true", "false", "false"),
        ("76561199054741771", 200, "true", "false", "true"),
        ("76561199054741771", 200, "true", "true", "false"),
        ("floysefake", 200, "false", "false", "false"),
        ("floysefake", 200, "true", "false", "true"),
        ("floysefake", 200, "false", "true", "true"),
        ("floysefake", 200, "true", "true", "false"),
         ]
    )
    async def test_query_request(self,client:AsyncClient,user,status_code,user_badges,friends_details,user_games):
        response = await client.get(f"{self.base_url}{user}?user_badges={user_badges}&friends_details={friends_details}&user_games={user_games}")

        assert response.status_code == status_code

        if user_badges == "false":
            assert response.json()["user_badges"] == None

        if friends_details == "false":
            user_list = response.json()["user_friends_list"].get("friends")
            assert isinstance(user_list,list)

        if user_games == "false":
            assert response.json()["user_games"] == None

    async def test_private_user(self,client:AsyncClient):
        response_1 = await client.get("/api/v1/steam/users_full_stats/76561198061916691")

        assert response_1.status_code == 403
        assert response_1.json().get("detail")

@pytest.mark.asyncio
class TestUserGamesPlay:
    base_url = "/api/v1/steam/user_games_played"

    @pytest.mark.parametrize(
        "user, status_code,expected",[
            ("floysefake",200,None),
            ("76561199054741771",200,None),
            ("ytgfdbltootpphrhtrhltfbflgf", 404, "Steam user not found"),
            ("765611990544643434", 404, "Steam user not found"),
        ]
    )
    async def test_request(self,client:AsyncClient,user,status_code,expected):
        response = await client.get(f"{self.base_url}?user={user}")

        assert response.status_code == status_code
        if not expected:
            assert response.json().get("games")
            assert response.json().get("game_count")>=0
        else:
            assert response.json() == {"detail": expected}

    async def test_private_user(self,client:AsyncClient):
        response = await client.get(f"{self.base_url}?user=76561198061916691")

        assert response.status_code == 200
        assert response.json() == {}

@pytest.mark.asyncio
class TestGameAchivements:
    base_url = "/api/v1/steam/game_achivements"

    @pytest.mark.parametrize(
        "game_id,status_code,expected",
        [
            (730,200,None),
            (570,200,None),
            (9999999,404,"Steam game not found"),
            (571,404,"Steam game not found"),
        ]
    )
    async def test_request(self,client:AsyncClient,game_id,status_code,expected):
        response = await client.get(f"{self.base_url}?game_id={game_id}")

        assert response.status_code == status_code
        if not expected:
            assert response.json().get("achievementpercentages")
        else:
            assert response.json() == {"detail": expected}

@pytest.mark.asyncio
@pytest.mark.usefixtures("steamgames")
@pytest.mark.parametrize(
    "page,status_code,limit,elements,expected",[
        (1,200,10,10,None),
        (1,200,25,25,None),
        (3,404,50,0,"3 Page Not Found"),
        (4,404,100,0,"4 Page Not Found"),
    ]
)
class TestSteamGames:
    base_url = "/api/v1/steam/"

    async def test_best_games(self,client:AsyncClient,page,status_code,limit,elements,expected):
        response = await client.get(f"{self.base_url}best_sallers/?page={page}&limit={limit}")

        assert response.status_code == status_code
        if isinstance(response.json(),dict) and status_code !=200:
            assert response.json()["detail"] == expected
        else:
            assert isinstance(response.json(),list)
            assert len(response.json()) == elements



    async def test_get_top_games(self,client:AsyncClient,page,status_code,limit,elements,expected):
        response = await client.get(f"{self.base_url}get_top_games/?page={page}&limit={limit}")

        data = response.json()

        assert response.status_code == status_code
        if isinstance(response.json(),dict) and status_code !=200:
            assert response.json()["detail"] == expected
        else:
            assert isinstance(data,list)
            for i in range(0,min(limit-1,10)):
                assert data[i]["positive"] >= data[i+1]["positive"]

            assert len(data) == elements