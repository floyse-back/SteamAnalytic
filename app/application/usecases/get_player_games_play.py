from app.infrastructure.steam_api.client import SteamClient


class GetPlayerGamesPlayUseCase:
    def __init__(self,steam):
        self.steam:SteamClient = steam

    async def execute(self,user):
        user = await self.steam.get_vanity_user_url(user)
        response = await self.steam.users_get_owned_games(f"{user}")

        return response