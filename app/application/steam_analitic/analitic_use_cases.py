from .games_for_you import GamesForYou, SallingForYou
from .user_rating import UserRating
from .users_battle import UsersBattle
from ..dto.steam_dto import transform_to_dto
from ..steam_use_cases.steam_use_cases import SteamService
from ...infrastructure.redis.redis_repository import redis_cache
from ...infrastructure.steam_api.client import SteamClient




class AnaliticService:
    def __init__(self):
        self.steam = SteamClient()

        self.user_rating = UserRating()
        self.games_for_you = GamesForYou()
        self.salling_for_you = SallingForYou()
        self.user_battle = UsersBattle()
        self.steam_service = SteamService()

    @redis_cache(expire=1200)
    async def analitic_user_rating(self,user:str):
        data = await self.steam_service.user_full_stats(user=user,friends_details=False)

        return await self.user_rating.create_user_rating(data=data)

    @redis_cache(expire=1200)
    async def analitic_games_for_you(self,user,session):
        user = await self.steam_service.user_games_play(user)
        data = user.json()

        result =  await self.games_for_you.find_games_for_you(data=data,session = session)

        return result

    @redis_cache(expire=1200)
    async def analitic_user_battle(self,user1:str,user2:str):
        if user1 == user2:
            raise ValueError("Users don't match")

        user_1 = await self.steam_service.user_full_stats(user=user1,friends_details=False)
        user_2 = await self.steam_service.user_full_stats(user=user2,friends_details=False)


        data = await self.user_battle.users_battle(user_1,user_2)

        return data

    @redis_cache(expire=1200)
    async def salling_for_you_games(self,user:str,session):
        user_data = await self.steam_service.user_games_play(user=user)
        return await self.salling_for_you.find_games_for_you(data=user_data,session=session)

    @redis_cache(expire=1200)
    async def friends_game_list(self,user_id):
        user_data,correct_user_id = await self.steam.get_user_info(user_id)
        result = self.steam.users.get_user_friends_list(correct_user_id)
        return result

    @redis_cache(expire=1200)
    async def user_achivements(self,user:str,app_id:int):
        user_data,correct_user_id = await self.steam.get_user_info(user)
        return self.steam.apps.get_user_achievements(int(correct_user_id),app_id)

