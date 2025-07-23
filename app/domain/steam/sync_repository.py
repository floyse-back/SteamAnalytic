from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List, Tuple, Sequence

from app.domain.steam.schemas import Game, BlockedGames


class INewsRepository(ABC):
    @abstractmethod
    def free_games_now(self,session)->Optional[List[Game]]:
        pass

    @abstractmethod
    def summary_statistics_steam(self,session)->Optional[dict]:
        pass

    @abstractmethod
    def news_discounts_steam(self,session,limit:int=5)->Optional[List[Game]]:
        pass

    @abstractmethod
    def game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        pass

    @abstractmethod
    def random_game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        pass

    @abstractmethod
    def new_release(self,session,now_date:date=date.today())->Optional[List[Game]]:
        pass

    @abstractmethod
    def new_release_from_this_month(self,session,now_date_list:List[date])->Optional[List[Game]]:
        pass

    @abstractmethod
    def event_history_steam_facts(self,session,now_date_list:List[date]=date.today())->Optional[List[Game]]:
        pass

    @abstractmethod
    def get_game_from_ganre_name(self, ganre_name, session):
        pass


class IGameWishlistRepository(ABC):
    @abstractmethod
    def wishlist_game_discount(self,appids:List[int],session)->Optional[dict]:
        pass

    @abstractmethod
    def get_changed_games(self,appids:List[dict],session)->Optional[List[Game]]:
        pass

class ICalendarSteamEventRepository(ABC):
    @abstractmethod
    def update_calendar_data(self,session,data:List[Tuple[str,date,date,str]]):
        pass

    @abstractmethod
    def get_calendar_events(self,session):
        pass

    @abstractmethod
    def get_now_events(self,session,datenow:date):
        pass


class IBlockedGamesRepository(ABC):
    @abstractmethod
    def add_blocked_games(self,appid:int,session):
        pass

    @abstractmethod
    def get_blocked_games_from_appids(self, appids, session)->Sequence[BlockedGames]:
        pass


class ISafegameRepository(ABC):
    @abstractmethod
    def add_safe_games(self,appid:int,session):
        pass

    @abstractmethod
    def get_safe_games_from_appids(self, appids, session):
        pass
