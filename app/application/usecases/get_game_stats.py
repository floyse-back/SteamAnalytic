from app.domain.logger import ILogger
from app.infrastructure.steam_api.client import SteamClient


class GetGameStatsUseCase:
    def __init__(self,steam,logger:ILogger):
        self.steam:SteamClient = steam
        self.logger = logger

    async def execute(self,steam_id:int):
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements,release_date'
        self.logger.info("GetGameStatsUseCase Get User Steam Steam_id=%s",steam_id)
        result = await self.steam.save_start_pool(self.steam.apps.get_app_details,app_id=steam_id,filters=filters)

        return result