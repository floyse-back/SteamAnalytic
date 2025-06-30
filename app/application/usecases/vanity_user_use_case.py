from app.application.dto.steam_dto import SteamAppid
from app.infrastructure.steam_api.client import SteamClient


class VanityUserUseCase:
    def __init__(self,steam:SteamClient):
        self.steam = steam

    async def execute(self,user:str):
        data = await self.steam.get_vanity_user_url(user)
        return SteamAppid(
            steam_appid=data
        )