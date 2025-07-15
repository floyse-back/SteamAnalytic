from typing import List, Optional

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.db.models.steam_models import Game


class HotDiscountUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger) -> None:
        self.news_repository=news_repository
        self.logger = logger

    def execute(self,session,limit:int=5)->Optional[List[Game]]:
        self.logger.debug("HotDiscountUseCase execute")
        data = self.news_repository.news_discounts_steam(session=session,limit=limit)
        if data is None:
            self.logger.info("HotDiscountUseCase execute not found Games")
            return None
        #Серіалізація даних
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        self.logger.info("HotDiscountUseCase Count Games: %s",len(serialize_data))
        return serialize_data