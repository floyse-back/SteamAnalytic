from typing import Optional

from app.application.dto.steam_dto import transform_to_dto, GamePriceModel
from app.domain.logger import ILogger
from app.infrastructure.steam_api.client import SteamClient


class GetGamePriceNowUseCase:
    def __init__(self,steam:SteamClient,logger:ILogger):
        self.steam = steam
        self.logger = logger

    async def execute(self,app_id:int)->Optional[GamePriceModel]:
        self.logger.info("GetGamePriceNowUseCase executing with app_id: %s",app_id)
        data = await self.steam.get_price_game_now(app_id)
        serialize_data = transform_to_dto(GamePriceModel,data)
        return serialize_data
