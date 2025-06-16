from app.application.dto.steam_dto import transform_to_dto, SteamBase
from app.domain.steam.repository import ISteamRepository


class GetFreeGamesUseCase():
    def __init__(self,steam_repository:ISteamRepository):
        self.steam_repository = steam_repository

    async def execute(self,session):
        result = await self.steam_repository.get_free_discount_games(session=session)
        new_result = [transform_to_dto(SteamBase,game) for game in result]

        return new_result