from typing import List

from app.application.dto.steam_dto import transform_to_dto, GameShortModel, GameFullModel
from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.logger.logger import logger


class NewReleaseUseCase:
    def __init__(self,news_repository:INewsRepository) -> None:
        self.news_repository = news_repository

    def execute(self,session)->List[dict]:
        data = self.news_repository.new_release(session=session)

        if data is None:
            return None
        logger.debug(f"New release data: {data}")
        serialize_data = [transform_to_dto(GameFullModel,i) for i in data]

        return serialize_data