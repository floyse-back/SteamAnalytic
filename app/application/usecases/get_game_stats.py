





class GetGameStatsUseCase:
    def __init__(self,steam):
        self.steam = steam

    async def execute(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        result = self.steam.apps.get_app_details(steam_id, filters=filters)

        return result