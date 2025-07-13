from app.application.dto.steam_dto import transform_to_dto, GameShortModel, GameFullModel
from app.domain.steam.sync_repository import INewsRepository


class CheepGamesUseCase:
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,session,min_price:int,limit=5):
        data = self.news_repository.game_from_price(session,price=min_price,limit=limit)

        #Serialize Data
        if data is None:
            return None
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]

        return serialize_data