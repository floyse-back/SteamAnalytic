from typing import Optional

from app.domain.logger import ILogger
from app.infrastructure.steam_api.client import SteamClient


class GetGameStatsUseCase:
    def __init__(self,steam,logger:ILogger):
        self.steam:SteamClient = steam
        self.logger = logger

    async def execute(self,steam_id:int)->Optional[dict]:
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements,release_date,movies,legal_notice'
        self.logger.info("GetGameStatsUseCase Get User Steam Steam_id=%s",steam_id)
        result = await self.steam.save_start_pool(self.steam.get_game_stats,appid=steam_id,filters=filters,cc="UA")

        return result

    def execute_sync(self,steam_id:int)->Optional[dict]:
        filters = 'basic,controller_support,dlc,fullgame,developers,demos,price_overview,metacritic,categories,genres,recommendations,achievements,release_date,legal_notice,movies'
        self.logger.info("GetGameStatsUseCase Get User Steam Steam_id=%s",steam_id)
        result = self.steam.get_game_stats(appid = steam_id, filters = filters, cc = "UA")
        return result