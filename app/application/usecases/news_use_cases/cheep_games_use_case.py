from app.application.dto.steam_dto import transform_to_dto, GameShortModel, GameFullModel
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository


class CheepGamesUseCase:
    def __init__(self,news_repository:INewsRepository,logger:ILogger):
        self.news_repository = news_repository
        self.logger = logger

    def execute(self,session,min_price:int,limit=5):
        data = self.news_repository.game_from_price(session,price=min_price,limit=limit)
        self.logger.debug("CheepGamesUseCase Get Cheep Game Details: %s",data)
        #Serialize Data
        if data is None:
            self.logger.info("CheepGamesUseCase Get Cheep Game Details: None")
            return None
        self.logger.info("CheepGamesUseCase Get Cheep Game Details len: %s",len(data))
        serialize_data = [transform_to_dto(GameFullModel, i) for i in data]

        return serialize_data