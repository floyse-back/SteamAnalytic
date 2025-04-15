from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.steam_dto import SteamUser,SteamBase
from app.application.exceptions.exception_handler import ProfilePrivate
from app.infrastructure.db.repository.steam_repository import SteamRepository
from app.infrastructure.steam_api.client import SteamClient
from app.utils.config import STEAM_API_KEY
from app.infrastructure.redis.redis_repository import RedisRepository




class SteamService:
    def __init__(self):
        self.steam_repository = SteamRepository()
        self.steam = SteamClient(STEAM_API_KEY)
        self.redis_repository = RedisRepository()

    async def best_sallers(self,session:AsyncSession,page,limit):
        redis_result  = self.redis_repository.get_data(f"best_sallers{page}_{limit}")
        if redis_result:
            return redis_result

        result = await self.steam_repository.get_most_discount_games(session = session,page = page,limit = limit)

        redis_result = self.redis_repository.cache_data(f"best_sallers{page}_{limit}",result,1200)
        
        return result

    async def user_full_stats(self, user,user_badges:bool = True,friends_details:bool = True,user_games:bool = True):
        user_data,user = await self.steam.get_user_info(user)

        if user_data["player"].get("communityvisibilitystate") == 3:
            user_friends_list = self.steam.users.get_user_friends_list(f"{user}", enriched=friends_details)
            user_badges = self.steam.users.get_user_badges(f"{user}") if user_badges else None
            user_games = self.steam.users.get_owned_games(f"{user}") if user_games else None


            return SteamUser(
                user_data = user_data,
                user_friends_list = user_friends_list,
                user_badges = user_badges,
                user_games = user_games,
            )
        raise ProfilePrivate(user_profile=user_data["player"].get("personaname"))

    async def game_stats(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        result = self.steam.apps.get_app_details(steam_id, filters=filters)

        return result

    async def get_top_games(self,session:AsyncSession,limit:int,page:int):
        result = await self.steam_repository.get_top_games(session,page,limit)

        return result

    async def game_achivements(self,game_id):
        response = await self.steam.get_global_achievements(game_id)

        return response.json()

    async def user_games_play(self,user:str):
        user_data,user = await self.steam.get_user_info(user)

        response = self.steam.users.get_owned_games(f"{user}")

        return response