from typing import Optional, List

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.steam.sync_repository import INewsRepository


class FreeGamesNowSyncUseCase:
    def __init__(self,news_repository:INewsRepository) -> None:
        self.news_repository: INewsRepository = news_repository

    def execute(self,session)->Optional[List[dict]]:
        data = self.news_repository.free_games_now(session=session)
        #Serialize_data
        if data is None:
            return None

        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        return serialize_data