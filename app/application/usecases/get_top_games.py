from app.application.exceptions.exception_handler import PageNotFound
from app.domain.steam.repository import ISteamRepository


class GetTopGamesUseCase:
    def __init__(self,steam_repository:ISteamRepository):
        self.steam_repository = steam_repository

    async def execute(self,session,page,limit):
        result = await self.steam_repository.get_top_games(session = session,page = page,limit = limit)
        if result == []:
            raise PageNotFound(page)

        return result






