from app.application.dto.steam_dto import transform_to_dto, GameShortModel
from app.application.exceptions.exception_handler import SteamRandomGameNotFound
from app.domain.logger import ILogger
from app.domain.steam.repository import IAnaliticsRepository


class GetRandomGamesUseCase:
    def __init__(self,analitic_repository:IAnaliticsRepository,logger:ILogger):
        self.analitic_repository = analitic_repository
        self.logger = logger

    async def execute(self,session,limit:int=15):
        self.logger.info("GetRandomGamesUseCase called")
        data = await self.analitic_repository.get_random_games(session=session,limit=limit)
        if len(data) == 0:
            raise SteamRandomGameNotFound()

        serilaze_result = [transform_to_dto(GameShortModel, i) for i in data]
        self.logger.info("GetRandomGamesUseCase returning len %s games",len(serilaze_result))
        return serilaze_result