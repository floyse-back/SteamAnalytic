from typing import Optional

from app.application.dto.steam_dto import transform_to_dto, GameFullModel
from app.domain.steam.sync_repository import INewsRepository


class GetGameFromGanreNameUseCase:
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,ganre_name:str,session)->Optional[dict]:
        data = self.news_repository.get_game_from_ganre_name(ganre_name=ganre_name,session=session)
        if data is None:
            return None

        serialize_data = transform_to_dto(GameFullModel,data)

        return serialize_data