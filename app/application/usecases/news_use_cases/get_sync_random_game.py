from app.application.dto.steam_dto import GameShortModel, transform_to_dto, Game, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class GetSyncRandomGameUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger):
        self.news_repository = news_repository
        self.logger = logger

    def execute(self,session):
        data = self.news_repository.random_game_from_price(session=session,limit=1,price=200)
        #Seriailze Data
        if data is None:
            self.logger.error("GetSyncRandomGameUseCase execute don`t found games")
            return None
        self.logger.info("GetSyncRandomGameUseCase execute len: %s",len(data))
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]
        return serialize_data