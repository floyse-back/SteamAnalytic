from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.steam_dto import SteamUser,SteamBase,transform_to_dto
from app.application.exceptions.exception_handler import ProfilePrivate, PageNotFound
from app.domain.steam.repository import ISteamRepository
from app.infrastructure.steam_api.client import SteamClient
from app.infrastructure.redis.redis_repository import redis_cache




class SteamService:
    def __init__(self,steam_repository: ISteamRepository,steam: SteamClient):
        self.steam_repository = steam_repository
        self.steam = steam

    @redis_cache(expire=2400)
    async def best_sallers(self,session:AsyncSession,page,limit):
        result = await self.steam_repository.get_most_discount_games(session = session,page = page,limit = limit)
        if result == []:
            raise PageNotFound(page)

        new_result = [transform_to_dto(SteamBase,i) for i in result]

        return new_result

    @redis_cache(expire=2400)
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
            ).model_dump()

        raise ProfilePrivate(user_profile=user_data["player"].get("personaname"))

    @redis_cache(expire=2400)
    async def game_stats(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        result = self.steam.apps.get_app_details(steam_id, filters=filters)

        return result

    @redis_cache(expire=1200)
    async def get_top_games(self,session:AsyncSession,limit:int,page:int):
        result = await self.steam_repository.get_top_games(session,page,limit)

        if result == []:
            raise PageNotFound(page)

        serialize_result = [ transform_to_dto(SteamBase,i) for i in result]

        return serialize_result

    @redis_cache(expire=600)
    async def game_achivements(self,game_id):
        response = await self.steam.get_global_achievements(game_id)

        return response

    @redis_cache(expire=1200)
    async def user_games_play(self,user:str):
        user_data,user = await self.steam.get_user_info(user)

        response = await self.steam.users_get_owned_games(f"{user}")

        return response

    @redis_cache(expire=600)
    async def games_filter(self,session:AsyncSession):
        pass