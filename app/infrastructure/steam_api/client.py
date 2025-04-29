from steam_web_api import Steam

from app.infrastructure.exceptions.exception_handler import SteamGameNotFound, SteamUserNotFound, \
    SteamUserAchievementsNotFoundDetails
from app.utils.config import STEAM_API_KEY
import re
from httpx import AsyncClient


class SteamClient(Steam):
    def __init__(self,steam_key = STEAM_API_KEY):
        super().__init__(key=steam_key)

    async def get_global_achievements(self,game_id):
        async with AsyncClient() as client:
            response = await client.get(
                f"https://api.steampowered.com/ISteamUserStats/GetGlobalAchievementPercentagesForApp/v2/?gameid={game_id}")

        if response.status_code == 200:
            return response.json()
        else:
            raise SteamGameNotFound("Steam game not found")

    async def get_user_info(self, user: str) -> tuple[dict, str]:
        if re.fullmatch(r"7656119\d{10}", user):
            steam_id = user
            user_data = self.users.get_user_details(steam_id)
            if user_data is not None and user_data.get('player') is not None:
                return user_data, steam_id

        user_data = self.users.search_user(user)

        if user_data is None or isinstance(user_data,str) or user_data.get('player') is None:
            raise SteamUserNotFound(f"User {user} not found")

        steam_id = user_data["player"]["steamid"]
        return user_data, steam_id

    async def users_get_owned_games(self,users):
        try:
            result = self.users.get_owned_games(f"{users}")
            return result
        except Exception:
            raise SteamGameNotFound(f"User {users} not found")

    async def users_get_achievements(self,user_id,app_id):
        try:
            data = self.apps.get_user_achievements(user_id,app_id)
            return data
        except Exception:
            raise SteamUserAchievementsNotFoundDetails("User or app not found")