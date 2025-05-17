from app.infrastructure.steam_api.client import SteamClient


class GetFriendsGameListUseCase:
    def __init__(self,steam):
        self.steam:SteamClient = steam

    async def execute(self,user:str):
        user_data,user_id = await self.steam.get_user_info(user)
        result = self.steam.save_start_pool(self.steam.users.get_user_friends_list,steam_id=user_id)
        return result