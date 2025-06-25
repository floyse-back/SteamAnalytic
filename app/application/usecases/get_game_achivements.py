from typing import Optional

from app.api.middleware.middleware import logger
from app.application.dto.steam_dto import transform_to_dto, GameAchievementsModel
from app.infrastructure.steam_api.client import SteamClient


class GetGameAchievementsUseCase:
    def __init__(self,steam:SteamClient):
        self.steam = steam

    async def execute(self,game_id:int,page:Optional[int]=1,offset:Optional[int]=10):
        response = await self.steam.get_global_achievements(game_id)
        logger.info("Data_XD))()():%s",response)
        data =  self.__offset_cords(response=response,page=page,offset=offset)
        if data:
            return transform_to_dto(
                model=GameAchievementsModel,
                orm=data
            )

    @staticmethod
    def __offset_cords(response:dict,page:int=1,offset:int=10):
        offset_cords = (int((page-1)*offset),int(page*offset))
        if not response.get("achievements") is None:
            response["achievements"]["highlighted"] = response["achievements"]["highlighted"][offset_cords[0]:offset_cords[1]]

        return response