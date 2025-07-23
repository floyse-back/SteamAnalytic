from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.steam_dto import SteamBase, transform_to_dto, Game
from app.application.usecases.add_blocked_games_use_case import AddBlockedGamesUseCase
from app.application.usecases.get_appid_from_name import GetAppidFromNameUseCase
from app.application.usecases.get_best_sallers import GetBestSallersUseCase
from app.application.usecases.get_game_achivements import GetGameAchievementsUseCase
from app.application.usecases.get_game_stats import GetGameStatsUseCase
from app.application.usecases.get_steam_search_games import GetSteamSearchGamesUseCase
from app.application.usecases.get_top_games import GetTopGamesUseCase
from app.application.usecases.get_player_full_stats import GetUserFullStatsUseCase
from app.application.usecases.get_player_games_play import GetPlayerGamesPlayUseCase
from app.application.usecases.get_user_badges_use_case import UserBadgesUseCase
from app.application.usecases.vanity_user_use_case import VanityUserUseCase
from app.domain.cache_repository import ICacheRepository
from app.domain.logger import ILogger
from app.domain.steam.repository import ISteamRepository
from app.application.decorators.cache import cache_data
from app.domain.steam.sync_repository import IBlockedGamesRepository


class SteamService:
    def __init__(self,steam_repository: ISteamRepository,blocked_repository:IBlockedGamesRepository,steam,cache_repository: ICacheRepository,logger:ILogger):
        self.cache_repository = cache_repository

        self.get_best_sallers_use_case = GetBestSallersUseCase(
            steam_repository = steam_repository,
            logger = logger
        )
        self.get_user_full_stats = GetUserFullStatsUseCase(
            steam = steam,
            logger = logger,
        )
        self.get_game_stats = GetGameStatsUseCase(
            steam = steam,
            logger = logger
        )
        self.get_top_games_use_case = GetTopGamesUseCase(
            steam_repository = steam_repository,
        )
        self.get_game_achievements = GetGameAchievementsUseCase(
            steam = steam,
        )
        self.get_user_games_play = GetPlayerGamesPlayUseCase(
            steam = steam,
            logger=logger
        )
        self.steam_games_use_case = GetSteamSearchGamesUseCase(
            steam_repository = steam_repository,
            logger = logger
        )
        self.get_appid_games = GetAppidFromNameUseCase(
            steam_repository = steam_repository,
            logger = logger

        )
        self.vanity_user_use_case = VanityUserUseCase(
            steam = steam,
        )
        self.user_badges_use_case = UserBadgesUseCase(
            steam = steam,
            logger = logger
        )
        self.add_blocked_games_use_case = AddBlockedGamesUseCase(
            blocked_repository=blocked_repository
        )

    @cache_data(expire=2400)
    async def best_sallers(self,session:AsyncSession,page,limit):
        result = await self.get_best_sallers_use_case.execute(session = session,page = page,limit = limit)
        new_result = [transform_to_dto(SteamBase,i) for i in result]

        return new_result

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
    async def game_achivements(self,game:str,session,page:int=1,offset:int=10):
        game_id:Optional[int] = await self.get_appid_games.execute(name = game,session=session)
        return await self.get_game_achievements.execute(game_id = game_id,page=page,offset=offset)

    async def user_games_play(self,user:str):
        return await self.get_user_games_play.execute(user = user)

    @cache_data(expire=600)
    async def search_game(self,session,page:int = 1,limit:int = 10,share:bool = True,name:Optional[str] = None,category = None,ganre = None,discount = None,publisher = None,to_price = None,out_price = None):
        result =  await self.steam_games_use_case.execute(session=session,page = page,share=share,limit=limit,name=name,category=category,discount=discount,publisher=publisher,ganre=ganre,to_price=to_price,out_price=out_price)
        return result

    async def vanity_user(self,user:str):
        return await self.vanity_user_use_case.execute(user = user)

    async def user_badges(self,user):
        return await self.user_badges_use_case.execute(user=user)

    def add_blocked_games_use_case(self,appid:int,session):
        return self.add_blocked_games_use_case.execute(appid = appid,session=session)