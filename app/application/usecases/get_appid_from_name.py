from typing import Optional

from app.domain.steam.repository import ISteamRepository
from app.infrastructure.logger.logger import logger


class GetAppidFromNameUseCase:
    def __init__(self,steam_repository:ISteamRepository):
        self.steam_repository = steam_repository

    async def execute(self,name,session)->Optional[int]:
        try:
            answer = int(name)
            return answer
        except ValueError:
            pass

        result = await self.steam_repository.get_steam_appid(session=session,name=name)
        logger.info("Steam Get Steam Appid name=%s result:%s",name,result)
        return result
