from app.application.dto.steam_dto import GameShortModel, transform_to_dto, Game, GameFullModel
from app.domain.steam.sync_repository import INewsRepository


class GetSyncRandomGameUseCase:
    def __init__(self,news_repository:INewsRepository):
        self.news_repository = news_repository

    def execute(self,session):
        data = self.news_repository.random_game_from_price(session=session,limit=1,price=200)
        #Seriailze Data
        if data is None:
            return None
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        return serialize_data