from typing import Dict, Callable

from app.application.usecases.news_use_cases.cheep_games_use_case import CheepGamesUseCase
from app.application.usecases.news_use_cases.event_history_steam_use_case import EventHistorySteamFactsUseCase
from app.application.usecases.news_use_cases.summary_statistics_steam_use_case import SummaryStatisticsSteamUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.logger.logger import logger


class NewsService:
    def __init__(self,news_repository:INewsRepository):
        self.event_history_steam_facts_use_case = EventHistorySteamFactsUseCase(
            news_repository=news_repository,
        )
        self.free_games_now = FreeGamesNowSyncUseCase(
            news_repository=news_repository,
        )
        self.new_discounts_steam_use_case = HotDiscountUseCase(

        )
        self.new_release_use_case = NewReleaseUseCase(
            news_repository=news_repository
        )
        self.summary_statistics_steam_use_case = SummaryStatisticsSteamUseCase(

        )
        self.top_for_a_coins_use_case = CheepGamesUseCase(

        )
        self.dispatcher_command:Dict[str,Callable] = {
            "news_new_release":self.new_release,
            "news_free_games_now":self.free_games_now,
            "news_event_history":self.event_history_steam_facts,
        }

    def event_history_steam_facts(self,session):
        return self.event_history_steam_facts_use_case.execute(session=session)

    def free_games_now(self,session):
        return self.free_games_now.execute(session=session)

    def summary_statistics_steam(self,session):
        return self.summary_statistics_steam_use_case.execute()

    def news_discounts_steam(self,session):
        return self.new_discounts_steam_use_case.execute()

    def top_for_a_coins(self,session):
        return self.top_for_a_coins_use_case.execute(min_price=500)

    def random_game(self,session):
        return {"Time":"Soon"}

    def trailer_from_day(self,session):
        return {"Time":"Soon"}

    def new_release(self,session):
        return self.new_release_use_case.execute(session=session)

    #В майбутньому
    def _guess_the_game(self):
        pass

    def dispathcher(self,func_name:str,*args,**kwargs):
        try:
            return self.dispatcher_command[func_name](*args,**kwargs)
        except KeyError as e:
            raise KeyError(e)
        except Exception as e:
            logger.error(e)
            raise e