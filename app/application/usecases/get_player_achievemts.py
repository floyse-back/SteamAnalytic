



class GetPlayerAchivementsUseCase:
    def __init__(self,steam):
        self.steam = steam

    async def execute(self,user:str,app_id:int):
        user_data, correct_user_id = await self.steam.get_user_info(user)
        return await self.steam.users_get_achievements(int(correct_user_id), app_id)
