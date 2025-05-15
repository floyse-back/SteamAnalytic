from app.domain.steam.repository import ISteamRepository


class GetSteamSearchGamesUseCase:
    def __init__(self,steam_repository:ISteamRepository):
        self.steam_repository = steam_repository

    async def execute(self,session,name,category,ganre,discount,publisher,to_price,out_price):
        return await self.steam_repository.search_game(session=session,name=name,category=category,discount=discount,publisher=publisher,ganre=ganre,to_price=to_price,out_price=out_price)