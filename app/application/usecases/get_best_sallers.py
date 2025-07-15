from app.application.exceptions.exception_handler import PageNotFound
from app.domain.logger import ILogger
from app.domain.steam.repository import ISteamRepository


class GetBestSallersUseCase:
    def __init__(self,steam_repository:ISteamRepository,logger:ILogger):
        self.steam_repository = steam_repository
        self.logger = logger

    async def execute(self,session,page,limit):
        self.logger.debug("GetBestSallersUseCase EXECUTING, page=%s,limit=%s",page,limit)
        result = await self.steam_repository.get_most_discount_games(session = session,page = page,limit = limit)
        if result == []:
            raise PageNotFound(page)

        return result