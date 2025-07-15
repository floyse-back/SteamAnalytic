from typing import Optional, List

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class FreeGamesNowSyncUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger) -> None:
        self.news_repository: INewsRepository = news_repository
        self.logger = logger

    def execute(self,session)->Optional[List[dict]]:
        data = self.news_repository.free_games_now(session=session)
        #Serialize_data
        if data is None:
            self.logger.info("FreeGamesNowSyncUseCase don`t Find Games")
            return None
        self.logger.info("FreeGamesNowSyncUseCase Find %s Games ",len(data))
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        return serialize_data