from app.application.dto.steam_dto import SteamUser
from app.application.exceptions.exception_handler import ProfilePrivate
from app.infrastructure.steam_api.client import SteamClient


class GetUserFullStatsUseCase:
    def __init__(self,steam):
        self.steam:SteamClient = steam

    async def execute(self,user,user_badges:bool = True,friends_details:bool = True,user_games:bool = True):
        user_data,user = await self.steam.get_user_info(user)

        if user_data["player"].get("communityvisibilitystate") == 3:
            user_friends_list = self.steam.save_start_pool(self.steam.users.get_user_friends_list,steam_id=f"{user}",enriched=friends_details)
            user_badges = self.steam.save_start_pool(self.steam.users.get_user_badges,steam_id=f"{user}") if user_badges else None
            user_games = self.steam.save_start_pool(self.steam.users.get_owned_games,steam_id=f"{user}")  if user_games else None

            return SteamUser(
                user_data = user_data,
                user_friends_list = user_friends_list,
                user_badges = user_badges,
                user_games = user_games,
            ).model_dump()

        raise ProfilePrivate(user_profile=user_data["player"].get("personaname"))
