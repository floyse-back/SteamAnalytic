from typing import Optional

from app.domain.logger import ILogger
from app.domain.steam.repository import ISteamRepository


class GetAppidFromNameUseCase:
    def __init__(self,steam_repository:ISteamRepository,logger:ILogger):
        self.steam_repository = steam_repository
        self.logger = logger

    async def execute(self,name,session)->Optional[int]:
        try:
            answer = int(name)
            return answer
        except ValueError:
            pass

        result = await self.steam_repository.get_steam_appid(session=session,name=name)
        self.logger.info("GetAppidFromNameUseCase: Steam Get Steam Appid name=%s result:%s",name,result)
        return result
