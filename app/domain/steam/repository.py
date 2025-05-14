from abc import ABC, abstractmethod
from typing import List, Optional
from app.domain.steam.schemas import SteamBase,Game

class ISteamRepository(ABC):
    @abstractmethod
    async def get_top_games(self,session,page:int,limit:int)->tuple[SteamBase]:
        pass

    @abstractmethod
    async def get_most_discount_games(self,session,page:int,limit:int)->tuple[SteamBase]:
        pass

    @abstractmethod
    async def get_free_discount_games(self, session: object) -> None:
        pass

    @abstractmethod
    async def search_game(self,*args,**kwargs) -> Optional[List[Game]]:
        pass

class IAnaliticsRepository(ABC):
    @abstractmethod
    async def get_games_for_appids(self,session,appid_list) ->List[Game]:
        pass

    @abstractmethod
    async def games_for_you(self,session,ganre_data,category_data,steam_appids) ->List:
        pass

    @abstractmethod
    async def salling_for_you(self,session,ganre_data,category_data,steam_appids) ->List:
        pass


