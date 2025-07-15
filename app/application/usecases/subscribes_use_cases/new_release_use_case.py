from typing import List

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class NewReleaseUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger) -> None:
        self.news_repository = news_repository
        self.logger = logger

    def execute(self,session)->List[dict]:
        data = self.news_repository.new_release(session=session)

        if data is None:
            return None
        self.logger.debug(f"New release data: {data}")
        serialize_data = [transform_to_dto(GameFullModel,i) for i in data]

        return serialize_data