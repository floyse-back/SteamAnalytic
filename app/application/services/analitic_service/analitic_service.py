from typing import List, Optional

from app.application.decorators.cache import cache_data
from app.application.dto.steam_dto import GameShortModel
from app.application.usecases.get_appid_from_name import GetAppidFromNameUseCase
from app.application.usecases.get_free_games import GetFreeGamesUseCase
from app.application.usecases.get_free_transform import GetFreeTransformUseCase
from app.application.usecases.get_friends_game_list import GetFriendsGameListUseCase
from app.application.usecases.get_game_stats import GetGameStatsUseCase
from app.application.usecases.get_games_for_you import GetGamesForYouUseCase
from app.application.usecases.get_price_game_now import GetGamePriceNowUseCase
from app.application.usecases.get_random_game import GetRandomGamesUseCase
from app.application.usecases.get_salling_for_you import GetSallingForYouUseCase
from app.application.usecases.get_player_achievemts import GetPlayerAchivementsUseCase
from app.application.usecases.get_player_battle import GetPlayerBattleUseCase
from app.application.usecases.get_player_full_stats import GetUserFullStatsUseCase
from app.application.usecases.get_player_games_play import GetPlayerGamesPlayUseCase
from app.application.usecases.get_players_rating import GetUserRatingUseCase
from app.domain.cache_repository import ICacheRepository
from app.domain.logger import ILogger
from app.domain.steam.repository import ISteamRepository, IAnaliticsRepository



class AnalyticService:
    def __init__(self,steam,cache_repository: ICacheRepository,steam_repository:ISteamRepository,analitic_repository: IAnaliticsRepository,logger:ILogger):
        self.steam = steam
        self.cache_repository = cache_repository

        self.get_user_full_stats = GetUserFullStatsUseCase(
            steam = steam,
            logger=logger
        )
        self.get_user_games_play = GetPlayerGamesPlayUseCase(
            steam = steam,
            logger = logger
        )
        self.get_user_rating = GetUserRatingUseCase(
            logger = logger
        )
        self.get_free_games = GetFreeGamesUseCase(
            steam_repository=steam_repository,
            logger = logger
        )
        self.get_free_transform = GetFreeTransformUseCase(logger=logger)
        self.get_user_achivements = GetPlayerAchivementsUseCase(
            steam=steam,
        )
        self.get_friends_game_list = GetFriendsGameListUseCase(
            steam = steam,
        )
        self.get_games_for_you = GetGamesForYouUseCase(
            analitic_repository=analitic_repository,
            logger = logger
        )
        self.get_salling_for_you = GetSallingForYouUseCase(
            analitic_repository=analitic_repository,
            logger = logger
        )
        self.get_game_details = GetGameStatsUseCase(
            steam = steam,
            logger = logger
        )
        self.get_user_battle = GetPlayerBattleUseCase(
            logger = logger
        )
        self.get_random_games = GetRandomGamesUseCase(
            analitic_repository=analitic_repository,
            logger = logger
        )
        self.get_steam_appid = GetAppidFromNameUseCase(
            steam_repository = steam_repository,
            logger = logger
        )
        self.get_price_now = GetGamePriceNowUseCase(
            steam = self.steam,
            logger = logger
        )
        self.logger = logger

    @cache_data(expire=1200)
    async def analitic_user_rating(self,user:str):
        data = await self.get_user_full_stats.execute(user=user,friends_details=False)

        return await self.get_user_rating.execute(data=data,enriched=True)

    @cache_data(expire=1200)
    async def analitic_games_for_you(self,user,session,page:int = 1,limit:int = 15):
        user_data = await self.get_user_games_play.execute(user=user)
        return await self.get_games_for_you.execute(data=user_data,session=session,page=page,limit=limit)

    @cache_data(expire=1200)
    async def analitic_user_battle(self,user1:str,user2:str):
        if user1 == user2:
            raise ValueError("Users don't match")

        user_1 = await self.get_user_full_stats.execute(user=user1,friends_details=False)
        user_2 = await self.get_user_full_stats.execute(user=user2,friends_details=False)

        user1_rating = await self.get_user_rating.execute(data=user_1)
        user2_rating = await self.get_user_rating.execute(data=user_2)

        data = await self.get_user_battle.execute(user_1,user_2,user1_rating,user2_rating)

        return data

    @cache_data(expire=1200)
    async def salling_for_you_games(self,user:str,session,page:int = 1,limit:int = 15):
        user_data = await self.get_user_games_play.execute(user=user)
        return await self.get_salling_for_you.execute(data=user_data, session=session,page=page,limit=limit)

    async def friends_game_list(self,user):
        return await self.get_friends_game_list.execute(user,enriched=False)

    @cache_data(expire=1200)
    async def user_achivements(self,user:str,app:str,session):
        app_id = await self.get_steam_appid.execute(app,session)
        return await self.get_user_achivements.execute(user=user,app_id=app_id)

    @cache_data(expire=1200)
    async def free_games(self,session)->Optional[List[GameShortModel]]:
        data = await self.get_free_games.execute(session=session)
        answer = []
        if not data:
            return False

        for value in data:
            game = await self.get_game_details.execute(steam_id=int(value['appid']))
            self.logger.info(f"FreeGames: game {game}")
            if int(game.get("price_overview",{"discount_percent":0}).get("discount_percent",0))==100:
                self.logger.info(f"FreeGames: {int(game.get("price_overview",{"discount_percent":0}).get("discount_percent",0))}")
                answer.append(self.get_free_transform.execute(game,game_id=int(value['appid'])))
        self.logger.info(f"FreeGames: {len(answer)}")
        if len(answer) == 0:
            return False

        return answer

    async def random_games(self,session,limit:int=15):
        return await self.get_random_games.execute(session=session,limit=limit)

    async def game_price_now(self,app,session):
        app_id = await self.get_steam_appid.execute(app, session)
        data = await self.get_price_now.execute(app_id=app_id)
        return data







