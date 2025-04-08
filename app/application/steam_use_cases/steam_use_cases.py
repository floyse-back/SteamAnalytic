from fastapi import HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from steam_web_api import Steam

from app.application.dto.steam_dto import SteamUser
from app.infrastructure.db.repository.steam_repository import SteamRepository
from app.utils.config import STEAM_API_KEY


class SteamService:
    def __init__(self):
        self.steam_repository = SteamRepository()
        self.steam = Steam(STEAM_API_KEY)

    async def get_user(self, user):
        try:
            my_int = int(user)
            user_data = self.steam.users.get_user_details(f"{my_int}")
        except Exception:
            user_data = self.steam.users.search_user(f"{user}")
            if user_data is None:
                raise HTTPException(
                    status_code=404,
                    detail=f"User {user} not found",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            user = user_data["player"]["steamid"]

        return user_data,user

    async def best_sallers(self,session:AsyncSession,page,limit):
        result = await self.steam_repository.get_most_discount_games(session = session,page = page,limit = limit)
        return result

    async def user_full_stats(self, user,user_badges:bool,friends_details:bool,user_games:bool):
        user_data,user = await self.get_user(user)

        user_friends_list = self.steam.users.get_user_friends_list(f"{user}", enriched=friends_details)
        user_badges = self.steam.users.get_user_badges(f"{user}") if user_badges else None
        user_games = self.steam.users.get_owned_games(f"{user}") if user_games else None

        return SteamUser(
            user_data = user_data,
            user_friends = user_friends_list,
            user_badges = user_badges,
            user_games = user_games,
        )

    async def game_stats(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        result = self.steam.apps.get_app_details(steam_id, filters=filters)

        return result

    async def get_top_games(self,session:AsyncSession,limit:int,page:int):
        result = await self.steam_repository.get_top_games(session,page,limit)

        return result

    async def game_achivements(self,game_id):
        async with AsyncClient() as client:
            response = await client.get(
                f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={game_id}")

        if response.status_code != 200:
            raise HTTPException(status_code=404, detail=f"Game {game_id} not found")

        return response.json()

    async def user_games_play(self,user:str):
        user_data,user = await self.get_user(user)

        response = self.steam.users.get_owned_games(f"{user}")

        return response