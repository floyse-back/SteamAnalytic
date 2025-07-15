from app.application.dto.steam_dto import transform_to_dto, SteamBase
from app.domain.logger import ILogger
from app.domain.steam.repository import ISteamRepository


class GetFreeGamesUseCase:
    def __init__(self,steam_repository:ISteamRepository,logger:ILogger):
        self.steam_repository = steam_repository
        self.logger = logger

    async def execute(self,session):
        self.logger.debug("GetFreeGamesUseCase: called %s")
        result = await self.steam_repository.get_free_discount_games(session=session)
        new_result = [transform_to_dto(SteamBase,game) for game in result]
        self.logger.debug("GetFreeGamesUseCase: Successfully fetched free games count: %s", len(new_result))
        return new_result