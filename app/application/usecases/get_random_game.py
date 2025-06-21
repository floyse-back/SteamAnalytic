from app.application.dto.steam_dto import transform_to_dto, GameShortModel
from app.application.exceptions.exception_handler import SteamRandomGameNotFound
from app.domain.steam.repository import IAnaliticsRepository


class GetRandomGamesUseCase:
    def __init__(self,analitic_repository:IAnaliticsRepository):
        self.analitic_repository = analitic_repository

    async def execute(self,session,limit:int=15):
        data = await self.analitic_repository.get_random_games(session=session,limit=limit)
        if len(data) == 0:
            raise SteamRandomGameNotFound()

        serilaze_result = [transform_to_dto(GameShortModel, i) for i in data]

        return serilaze_result