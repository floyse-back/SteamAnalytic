from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.steam_dto import SteamBase, transform_to_dto, Game
from app.application.usecases.get_best_sallers import GetBestSallersUseCase
from app.application.usecases.get_game_achivements import GetGameAchievementsUseCase
from app.application.usecases.get_game_stats import GetGameStatsUseCase
from app.application.usecases.get_steam_search_games import GetSteamSearchGamesUseCase
from app.application.usecases.get_top_games import GetTopGamesUseCase
from app.application.usecases.get_player_full_stats import GetUserFullStatsUseCase
from app.application.usecases.get_player_games_play import GetPlayerGamesPlayUseCase
from app.domain.cache_repository import ICacheRepository
from app.domain.steam.repository import ISteamRepository
from app.application.decorators.cache import cache_data


class SteamService:
    def __init__(self,steam_repository: ISteamRepository,steam,cache_repository: ICacheRepository):
        self.cache_repository = cache_repository

        self.get_best_sallers_use_case = GetBestSallersUseCase(
            steam_repository = steam_repository
        )
        self.get_user_full_stats = GetUserFullStatsUseCase(
            steam = steam
        )
        self.get_game_stats = GetGameStatsUseCase(
            steam = steam
        )
        self.get_top_games_use_case = GetTopGamesUseCase(
            steam_repository = steam_repository
        )
        self.get_game_achievements = GetGameAchievementsUseCase(
            steam = steam
        )
        self.get_user_games_play = GetPlayerGamesPlayUseCase(
            steam = steam
        )
        self.steam_games_use_case = GetSteamSearchGamesUseCase(
            steam_repository = steam_repository
        )

    @cache_data(expire=2400)
    async def best_sallers(self,session:AsyncSession,page,limit):
        result = await self.get_best_sallers_use_case.execute(session = session,page = page,limit = limit)
        new_result = [transform_to_dto(SteamBase,i) for i in result]

        return new_result

    @cache_data(expire=2400)
    async def user_full_stats(self, user,user_badges:bool = True,friends_details:bool = True,user_games:bool = True):
        return await self.get_user_full_stats.execute(user = user, user_badges=user_badges,friends_details=friends_details,user_games=user_games)

    @cache_data(expire=2400)
    async def game_stats(self,steam_id:int):
        return await self.get_game_stats.execute(steam_id = steam_id)

    @cache_data(expire=2400)
    async def get_top_games(self,session:AsyncSession,limit:int,page:int):
        result = await self.get_top_games_use_case.execute(session = session,limit = limit,page = page)
        if len(result)==0 or result[0] is None:
            return None
        new_result = [transform_to_dto(SteamBase,i) for i in result]
        return new_result

    @cache_data(expire=2400)
    async def game_achivements(self,game_id):
        return await self.get_game_achievements.execute(game_id = game_id)

    @cache_data(expire=2400)
    async def user_games_play(self,user:str):
        return await self.get_user_games_play.execute(user = user)

    @cache_data(expire=600)
    async def search_game(self,session,name = None,category = None,ganre = None,discount = None,publisher = None,to_price = None,out_price = None):
        result =  await self.steam_games_use_case.execute(session=session,name=name,category=category,discount=discount,publisher=publisher,ganre=ganre,to_price=to_price,out_price=out_price)

        serilaze_result = [transform_to_dto(Game, i) for i in result]

        return serilaze_result