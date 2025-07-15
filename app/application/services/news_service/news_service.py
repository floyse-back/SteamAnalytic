from typing import Dict, Callable, Optional, List

from app.application.usecases.news_use_cases.cheep_games_use_case import CheepGamesUseCase
from app.application.usecases.news_use_cases.event_history_steam_use_case import EventHistorySteamFactsUseCase
from app.application.usecases.news_use_cases.get_calendar_event_now_use_case import GetCalendarEventNowUseCase
from app.application.usecases.news_use_cases.get_sync_random_game import GetSyncRandomGameUseCase
from app.application.usecases.news_use_cases.summary_statistics_steam_use_case import SummaryStatisticsSteamUseCase
from app.application.usecases.news_use_cases.update_calendar_events_use_case import UpdateCalendarEventsUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository, ICalendarSteamEventRepository


class NewsService:
    def __init__(self,news_repository:INewsRepository,calendar_repository:ICalendarSteamEventRepository,logger:ILogger):
        self.logger = logger
        self.event_history_steam_facts_use_case = EventHistorySteamFactsUseCase(
            news_repository=news_repository,
            logger = logger
        )
        self.free_games_now_use_case = FreeGamesNowSyncUseCase(
            news_repository=news_repository,
            logger = logger
        )
        self.new_discounts_steam_use_case = HotDiscountUseCase(
            news_repository=news_repository,
            logger=logger
        )
        self.new_release_use_case = NewReleaseUseCase(
            news_repository=news_repository,
            logger=logger
        )
        self.summary_statistics_steam_use_case = SummaryStatisticsSteamUseCase(
            news_repository=news_repository,
            logger=logger
        )
        self.top_for_a_coins_use_case = CheepGamesUseCase(
            news_repository=news_repository,
            logger=logger
        )
        self.random_game_sync_use_case = GetSyncRandomGameUseCase(
            news_repository=news_repository,
            logger=logger
        )
        self.update_calendar_events_use_case = UpdateCalendarEventsUseCase(
            calendar_repository=calendar_repository,
        )
        self.calendar_event_now_use_case = GetCalendarEventNowUseCase(
            calendar_repository=calendar_repository,
            logger=logger
        )
        self.dispatcher_command:Dict[str,Callable] = {
            "news_new_release":self.new_release,
            "news_free_games_now":self.free_games_now,
            "news_event_history":self.event_history_steam_facts,
            "news_discounts_steam_now":self.news_discounts_steam,
            "news_top_for_a_coins":self.top_for_a_coins,
            "news_random_game":self.random_game,
            "news_trailer_from_day":self.trailer_from_day,
            "news_calendar_event_now":self.get_calendar_event_now
        }

    def event_history_steam_facts(self,session)->Optional[List[dict]]:
        return self.event_history_steam_facts_use_case.execute(session=session)

    def free_games_now(self,session)->Optional[List[dict]]:
        return self.free_games_now_use_case.execute(session=session)

    def summary_statistics_steam(self,session)->Optional[List[dict]]:
        return self.summary_statistics_steam_use_case.execute(session=session)

    def news_discounts_steam(self,session)->Optional[List[dict]]:
        return self.new_discounts_steam_use_case.execute(session=session,limit=5)

    def top_for_a_coins(self,session)->Optional[List[dict]]:
        return self.top_for_a_coins_use_case.execute(min_price=500,session=session)

    def random_game(self,session)->Optional[List[dict]]:
        return self.random_game_sync_use_case.execute(session=session)

    def trailer_from_day(self,session):
        return {"Time":"Soon"}

    def new_release(self,session)->Optional[List[dict]]:
        return self.new_release_use_case.execute(session=session)

    #В майбутньому
    def _guess_the_game(self):
        pass

    def get_calendar_event_now(self,session):
        return self.calendar_event_now_use_case.execute(session=session)

    def update_calendar_events(self,session):
        return self.update_calendar_events_use_case.execute(session=session)

    def dispathcher(self,func_name:str,*args,**kwargs):
        try:
            return self.dispatcher_command[func_name](*args,**kwargs)
        except KeyError as e:
            raise KeyError(e)
        except Exception as e:
            self.logger.error("",e,exc_info=True)
            raise e