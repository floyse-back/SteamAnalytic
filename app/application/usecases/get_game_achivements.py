

class GetGameAchievementsUseCase:
    def __init__(self,steam):
        self.steam = steam

    async def execute(self,game_id:int):
        response = await self.steam.get_global_achievements(game_id)

        return response