from typing import Optional, List

from app.domain.steam.sync_repository import INewsRepository


class FreeGamesNowSyncUseCase:
    def __init__(self,news_repository:INewsRepository) -> None:
        self.news_repository: INewsRepository = news_repository

    def execute(self,session)->Optional[List]:
        data = self.news_repository.free_games_now(session=session)
        #Serialize_data
        return data