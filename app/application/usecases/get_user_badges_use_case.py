from app.application.dto.steam_dto import transform_to_dto, SteamBadgesListModel
from app.domain.logger import ILogger
from app.infrastructure.steam_api.client import SteamClient


class UserBadgesUseCase:
    def __init__(self,steam:SteamClient,logger:ILogger):
        self.steam = steam
        self.logger = logger

    async def execute(self,user):
        user_id = await self.steam.get_vanity_user_url(vanity_url=user)
        data = await self.steam.save_start_pool(self.steam.users.get_user_badges,func_name="user_badges",steam_id=user_id)
        self.logger.debug("UserBadgesUseCase execute success, user=%s",user)
        serialize_data = transform_to_dto(SteamBadgesListModel,data)

        return serialize_data