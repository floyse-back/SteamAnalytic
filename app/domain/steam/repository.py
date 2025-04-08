from abc import ABC, abstractmethod
from typing import List
from app.infrastructure.db.models.steam_models import Game, SteamBase


class ISteamRepository(ABC):
    @abstractmethod
    async def get_top_games(self,session,page:int,limit:int)->tuple[SteamBase]:
        pass

    @abstractmethod
    async def get_most_discount_games(self,session,page:int,limit:int)->tuple[SteamBase]:
        pass

class IAnaliticsRepository(ABC):
    @abstractmethod
    async def get_games_for_appids(self,session,appid_list) ->Game:
        pass

    @abstractmethod
    async def games_for_you(self,session,ganre_data,category_data,steam_appids) ->List:
        pass


