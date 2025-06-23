from app.infrastructure.steam_api.client import SteamClient


class GetPlayerAchivementsUseCase:
    def __init__(self,steam:SteamClient):
        self.steam = steam

    async def execute(self,user:str,app_id:int):
        correct_user_id = await self.steam.get_vanity_user_url(user)
        print(correct_user_id)
        print(app_id)
        return await self.steam.users_get_achievements(int(correct_user_id), app_id)
