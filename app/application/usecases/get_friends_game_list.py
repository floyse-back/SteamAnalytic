from app.infrastructure.steam_api.client import SteamClient


class GetFriendsGameListUseCase:
    def __init__(self,steam):
        self.steam:SteamClient = steam

    async def execute(self,user:str):
        user_id = await self.steam.get_vanity_user_url(user)
        result = await self.steam.user_get_friends(user=user_id)
        return result