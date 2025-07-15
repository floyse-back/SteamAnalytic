from app.domain.logger import ILogger
from app.infrastructure.steam_api.client import SteamClient


class GetPlayerGamesPlayUseCase:
    def __init__(self,steam,logger:ILogger):
        self.steam:SteamClient = steam
        self.logger =  logger

    async def execute(self,user):
        self.logger.info("GetPlayerGamesPlayUseCase: called %s",user)
        user = await self.steam.get_vanity_user_url(user)
        self.logger.debug("GetPlayerGamesPlayUseCase: Successfully fetched user: %s",user)
        response = await self.steam.users_get_owned_games(f"{user}")
        self.logger.debug("GetPlayerGamesPlayUseCase: Successfully fetched get_owned_games: %s",response)

        return response