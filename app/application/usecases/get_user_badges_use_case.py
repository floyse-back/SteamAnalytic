from app.application.dto.steam_dto import transform_to_dto, SteamBadgesListModel
from app.infrastructure.steam_api.client import SteamClient


class UserBadgesUseCase:
    def __init__(self,steam:SteamClient):
        self.steam = steam

    async def execute(self,user):
        user_id = await self.steam.get_vanity_user_url(vanity_url=user)
        data = await self.steam.save_start_pool(self.steam.users.get_user_badges,func_name="user_badges",steam_id=user_id)
        serialize_data = transform_to_dto(SteamBadgesListModel,data)

        return serialize_data