from abc import ABC, abstractmethod
from datetime import date
from typing import Optional, List

from app.domain.steam.schemas import Game


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


class ISubscribesRepository(ABC):
    @abstractmethod
    def wishlist_game_discount(self,appids:List[int])->Optional[dict]:
        pass

