from steam_web_api import Steam
from app.utils.config import STEAM_API_KEY
from httpx import AsyncClient


class SteamGameNotFound(Exception):
    pass

class SteamUserNotFound(Exception):
    pass


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
        try:
            steam_id = str(int(user))
            user_data = self.users.get_user_details(steam_id)
        except ValueError:
            user_data = self.users.search_user(user)
            if user_data is None:
                raise SteamUserNotFound(f"User {user} not found")
            steam_id = user_data["player"]["steamid"]

        return user_data, steam_id