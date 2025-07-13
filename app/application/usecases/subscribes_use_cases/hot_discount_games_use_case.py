from typing import List, Optional

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.db.models.steam_models import Game


class HotDiscountUseCase:
    def __init__(self,news_repository:INewsRepository) -> None:
        self.news_repository=news_repository

    def execute(self,session,limit:int=5)->Optional[List[Game]]:
        data = self.news_repository.news_discounts_steam(session=session,limit=limit)
        #Серіалізація даних
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        return serialize_data