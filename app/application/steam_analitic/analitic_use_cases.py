from sqlalchemy.ext.asyncio import AsyncSession

from .games_for_you import GamesForYou, SallingForYou
from .user_rating import UserRating
from ..steam_use_cases.steam_use_cases import SteamService
from ...infrastructure.steam_api.client import SteamClient
from httpx import AsyncClient


class AnaliticService:
    def __init__(self):
        self.steam = SteamClient()

        self.user_rating = UserRating()
        self.games_for_you = GamesForYou()
        self.salling_for_you = SallingForYou()
        self.steam_service = SteamService()

    async def analitic_user_rating(self,data:dict):
        return await self.user_rating.create_user_rating(data=data)

    async def analitic_games_for_you(self,user,session:AsyncSession):
        user = await self.steam_service.user_games_play(user)

        data = user.json()
        return await self.games_for_you.find_games_for_you(data=data,session = session)

    async def analitic_user_battle(self,user1_data:dict,user2_data:dict):
        return {}

    async def salling_for_you_games(self,data:dict,session:AsyncSession):
        return await self.salling_for_you.find_games_for_you(data=data,session=session)

    async def friends_game_list(self,user_id):
        user_data,correct_user_id = await self.steam.get_user_info(user_id)

        result = self.steam.users.get_user_friends_list(correct_user_id)

        return result

