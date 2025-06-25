from typing import Optional, List

from app.api.middleware.middleware import logger
from app.application.dto.steam_dto import transform_to_dto, GamePriceModel
from app.infrastructure.steam_api.client import SteamClient


class GetGamePriceNowUseCase:
    def __init__(self,steam:SteamClient):
        self.steam = steam

    async def execute(self,app_id:int)->Optional[GamePriceModel]:
        data = await self.steam.get_price_game_now(app_id)
        serialize_data = transform_to_dto(GamePriceModel,data)
        return serialize_data
