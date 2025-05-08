from app.application.services.steam_service.steam_service import SteamService
from app.application.decorators.cache import cache_data
from app.application.usecases.get_free_games import GetFreeGamesUseCase
from app.application.usecases.get_friends_game_list import GetFriendsGameListUseCase
from app.application.usecases.get_games_for_you import GetGamesForYouUseCase
from app.application.usecases.get_salling_for_you import GetSallingForYouUseCase
from app.application.usecases.get_player_achievemts import GetUserAchivementsUseCase
from app.application.usecases.get_player_battle import GetUserBattleUseCase
from app.application.usecases.get_player_full_stats import GetUserFullStats
from app.application.usecases.get_player_games_play import GetUserGamesPlayUseCase
from app.application.usecases.get_players_rating import GetUserRatingUseCase
from app.domain.redis_repository import ICacheRepository
from app.domain.steam.repository import ISteamRepository, IAnaliticsRepository
from app.infrastructure.steam_api.client import SteamClient



class AnalyticService:
    def __init__(self, steam:SteamClient,cache_repository: ICacheRepository,steam_repository:ISteamRepository,analitic_repository: IAnaliticsRepository):
        self.steam = steam
        self.cache_repository = cache_repository

        self.get_user_full_stats = GetUserFullStats(
            steam = steam
        )
        self.get_user_games_play = GetUserGamesPlayUseCase(
            steam = steam
        )
        self.get_user_rating = GetUserRatingUseCase()
        self.get_free_games = GetFreeGamesUseCase(
            steam_repository=steam_repository
        )
        self.get_user_achivements = GetUserAchivementsUseCase(
            steam=steam
        )
        self.get_friends_game_list = GetFriendsGameListUseCase(
            steam = steam
        )
        self.get_games_for_you = GetGamesForYouUseCase(
            analitic_repository=analitic_repository
        )
        self.get_salling_for_you = GetSallingForYouUseCase(
            analitic_repository=analitic_repository
        )
        self.get_user_battle = GetUserBattleUseCase()

    @cache_data(expire=1200)
    async def analitic_user_rating(self,user:str):
        data = await self.get_user_full_stats.execute(user=user,friends_details=False)

        return await self.get_user_rating.execute(data=data)

    @cache_data(expire=1200)
    async def analitic_games_for_you(self,user,session):
        user_data = await self.get_user_games_play.execute(user=user)
        return await self.get_games_for_you.execute(data=user_data,session=session)

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
    async def salling_for_you_games(self,user:str,session):
        user_data = await self.get_user_games_play.execute(user=user)
        return await self.get_salling_for_you.execute(data=user_data, session=session)

    @cache_data(expire=1200)
    async def friends_game_list(self,user):
        return await self.get_friends_game_list.execute(user)

    @cache_data(expire=1200)
    async def user_achivements(self,user:str,app_id:int):
        return await self.get_user_achivements.execute(user=user,app_id=app_id)

    @cache_data(expire=1200)
    async def free_games(self,session):
        return await self.get_free_games.execute(session=session)


