



class GetPlayerGamesPlayUseCase:
    def __init__(self,steam):
        self.steam = steam

    async def execute(self,user):
        user_data,user = await self.steam.get_user_info(user)
        response = await self.steam.users_get_owned_games(f"{user}")

        return response