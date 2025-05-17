from app.infrastructure.steam_api.client import SteamClient


class GetGameStatsUseCase:
    def __init__(self,steam):
        self.steam:SteamClient = steam

    async def execute(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements'
        result = self.steam.save_start_pool(self.steam.apps.get_app_details,steam_id=steam_id,filters=filters)

        return result