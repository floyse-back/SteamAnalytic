from sqlalchemy.ext.asyncio import AsyncSession

from .games_for_you import GamesForYou, SallingForYou
from .user_rating import UserRating
from ..steam_use_cases.steam_use_cases import SteamService
from ...infrastructure.steam_api.client import SteamClient





class AnaliticService:
    def __init__(self):
        self.steam = SteamClient()

        self.user_rating = UserRating()
        self.games_for_you = GamesForYou()
        self.salling_for_you = SallingForYou()
        self.steam_service = SteamService()

    async def analitic_user_rating(self,user:str):
        data = await self.steam_service.user_full_stats(user=user,friends_details=False)

        return await self.user_rating.create_user_rating(data=data)

    async def analitic_games_for_you(self,user,session:AsyncSession):
        user = await self.steam_service.user_games_play(user)
        data = user.json()

        return await self.games_for_you.find_games_for_you(data=data,session = session)

    async def analitic_user_battle(self,user1:str,user2:str):
        if user1 == user2:
            raise ValueError("Users don't match")

        user_1 = await self.steam_service.user_full_stats(user=user1,friends_details=False)
        user_2 = await self.steam_service.user_full_stats(user=user2,friends_details=False)

        return {
            "message":user_1,
            "message2":user_2
        }



    async def salling_for_you_games(self,user:str,session:AsyncSession):
        user_data = await self.steam_service.user_games_play(user=user)
        return await self.salling_for_you.find_games_for_you(data=user_data,session=session)

    async def friends_game_list(self,user_id):
        user_data,correct_user_id = await self.steam.get_user_info(user_id)
        result = self.steam.users.get_user_friends_list(correct_user_id)
        return result

    async def user_achivements(self,user:str,app_id:int):
        user_data,correct_user_id = await self.steam.get_user_info(user)
        return self.steam.apps.get_user_achievements(int(correct_user_id),app_id)

