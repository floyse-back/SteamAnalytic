




class GetFriendsGameListUseCase:
    def __init__(self,steam):
        self.steam = steam

    async def execute(self,user:str):
        user_data,user_id = await self.steam.get_user_info(user)
        result = self.steam.users.get_user_friends_list(user_id)
        return result