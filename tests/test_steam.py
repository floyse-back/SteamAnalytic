import pytest
from httpx import AsyncClient

from app.application.dto.steam_dto import AchievementsModel, GameAchievementsModel
from app.infrastructure.logger.logger import logger
from app.utils.config import ServicesConfig
from tests.utils import transform_to_dto

service_config = ServicesConfig()

@pytest.mark.asyncio
class TestUsersFullStats:
    PATH = f"{service_config.steam_service.path}/users_full_stats"
    @pytest.mark.parametrize(
        "user, status_code,expected",[
            ("floysefake",200,None),
            ("76561199054741771", 200,None),
            ("ytgfdbltootpphrhtrhltfbflgf",404,"Steam user not found"),
            ("765611990544643434",404,"Steam user not found"),
        ]
    )
    async def test_default_request(self,client:AsyncClient,user,status_code,expected):
        response = await client.get(f"{self.PATH}/{user}")
        logger.info(f"response: {response.status_code}")
        assert (response.status_code == status_code or response.status_code == 429 or response.status_code == 502)

        if not expected and not (response.status_code == 502 or response.status_code == 429):
            data:dict = response.json()
            logger.info(data)
            assert data.get("user_data")["player"]
            assert data.get("user_friends_list")
            assert data.get("user_badges")
            assert data.get("user_games")
        elif expected:
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
        response = await client.get(f"{self.PATH}/{user}?user_badges={user_badges}&friends_details={friends_details}&user_games={user_games}")

        assert response.status_code == status_code or response.status_code == 502
        if response.status_code == 200:
            if user_badges == "false":
                assert response.json()["user_badges"] == None

            if friends_details == "false":
                user_list = response.json()["user_friends_list"].get("friends")
                assert isinstance(user_list,list)

            if user_games == "false":
                assert response.json()["user_games"] == None

    async def test_private_user(self,client:AsyncClient):
        response_1 = await client.get(f"{self.PATH}/76561198061916691")

        assert response_1.status_code == 403 or response_1.status_code == 502
        assert response_1.json().get("detail")

@pytest.mark.asyncio
class TestUserGamesPlay:
    PATH = f"{service_config.steam_service.path}/user_games_played"

    @pytest.mark.parametrize(
        "user, status_code,expected",[
            ("floysefake",200,None),
            ("76561199054741771",200,None),
            ("ytgfdbltootpphrhtrhltfbflgf", 404, "Steam user not found"),
            ("765611990544643434", 404, "Steam user not found"),
        ]
    )
    async def test_request(self,client:AsyncClient,user,status_code,expected):
        response = await client.get(f"{self.PATH}?user={user}")

        assert response.status_code == status_code or response.status_code == 502
        if response.status_code == status_code:
            if not expected:
                assert response.json().get("games")
                assert response.json().get("game_count")>=0
            else:
                assert response.json() == {"detail": expected}

    async def test_private_user(self,client:AsyncClient):
        response = await client.get(f"{self.PATH}?user=76561198061916691")

        assert response.status_code == 200
        assert response.json() == {}

@pytest.mark.asyncio
class TestGameAchivements:
    base_url = f"{service_config.steam_service.path}/game_achivements"

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
        response = await client.get(f"{self.base_url}",params={
            "game": game_id,
            "page":1,
            "offset":5,
        })

        assert response.status_code == status_code or response.status_code == 502
        if not expected:
            transform_to_dto(GameAchievementsModel,response.json())
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
    PATH = f"{service_config.steam_service.path}"

    async def test_best_games(self,client:AsyncClient,page,status_code,limit,elements,expected):
        response = await client.get(f"{self.PATH}/best_sallers/?page={page}&limit={limit}")

        assert response.status_code == status_code
        if isinstance(response.json(),dict) and status_code !=200:
            assert response.json()["detail"] == expected
        else:
            assert isinstance(response.json(),list)
            assert len(response.json()) == elements



    async def test_get_top_games(self,client:AsyncClient,page,status_code,limit,elements,expected):
        response = await client.get(f"{self.PATH}/get_top_games/?page={page}&limit={limit}")

        data = response.json()

        assert response.status_code == status_code
        if isinstance(response.json(),dict) and status_code !=200:
            assert response.json()["detail"] == expected
        else:
            assert isinstance(data,list)

            assert len(data) == elements

class TestSearchGames:
    path = f"{service_config.steam_service.path}"


    @pytest.mark.parametrize(
        "params,status_code",[
            (
                {
                    "name":"Item 55"
                },200
            ),
            (
                    {
                        "name": "Item"
                    }, 200
            ),
            (
                    {
                        "category":["Random Category 5","Random Category 2"],
                    }, 200
            ),
            (
                    {
                        "publisher": ["Random Publisher 5", "Random Publisher 2"],
                    }, 200
            ),
            (
                    {
                        "ganre": ["Random Ganre 5", "Random Ganre 2"],
                    }, 200
            ),
            (
                    {
                        "name": "Item 25",
                        "discount": 30,
                        "to_price": 1599
                    }, 200
            ),
            (
                    {
                        "ganre": ["Random Ganre 3"],
                        "publisher": ["Random Publisher 2"],
                        "discount": 50
                    }, 200
            ),
            (
                    {
                        "name": "Item 17",
                        "out_price": 349,
                        "publisher": ["Random Publisher 4"]
                    }, 200
            ),
            (
                    {
                        "ganre": ["Random Ganre 2", "Random Ganre 5"],
                        "discount": 20,
                        "out_price": 799
                    }, 200
            ),
            (
                    {
                        "name": "Item 66",
                        "ganre": ["Random Ganre 4"],
                        "to_price": 1250,
                        "discount": 0
                    }, 200
            ),
            (
                    {
                        "publisher": ["Random Publisher 1"],
                        "to_price": 999,
                        "out_price": 499
                    }, 200
            ),
            (
                    {
                        "name": "Item 90",
                        "ganre": ["Random Ganre 1"],
                        "publisher": ["Random Publisher 3"],
                        "discount": 75,
                        "to_price": 1400,
                        "out_price": 250
                    }, 200
            ),

        ]
    )
    async def test_search_games(self,games,client:AsyncClient,params,status_code):
        response = await client.get(f"{self.path}/search_game/",params=params)

        assert response.status_code == status_code
        logger.debug("%s",response.json())
        assert isinstance(response.json(),list)
        assert len(response.json())<=20