from typing import Dict, Callable, Optional, List

from app.application.usecases.get_free_transform import GetFreeTransformUseCase
from app.application.usecases.get_game_stats import GetGameStatsUseCase
from app.application.usecases.news_use_cases.cheep_games_use_case import CheepGamesUseCase
from app.application.usecases.news_use_cases.event_history_steam_use_case import EventHistorySteamFactsUseCase
from app.application.usecases.news_use_cases.get_calendar_event_now_use_case import GetCalendarEventNowUseCase
from app.application.usecases.news_use_cases.get_game_from_categories_name_use_case import \
    GetGameFromCategoriesNameUseCase
from app.application.usecases.news_use_cases.get_game_from_ganre_name_use_case import GetGameFromGanreNameUseCase
from app.application.usecases.news_use_cases.get_sync_random_game import GetSyncRandomGameUseCase
from app.application.usecases.news_use_cases.summary_statistics_steam_use_case import SummaryStatisticsSteamUseCase
from app.application.usecases.news_use_cases.update_calendar_events_use_case import UpdateCalendarEventsUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import INewsRepository, ICalendarSteamEventRepository


class NewsService:
    def __init__(self,news_repository:INewsRepository,calendar_repository:ICalendarSteamEventRepository,logger:ILogger,steam):
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
        self.get_game_stats_use_case = GetGameStatsUseCase(
            logger=logger,
            steam=steam
        )
        self.get_game_from_category_name_use_case = GetGameFromCategoriesNameUseCase(
            news_repository=news_repository
                                                                                     )
        self.get_game_correct_data = GetFreeTransformUseCase(logger=logger)
        self.dispatcher_command:Dict[str,Callable] = {
            "news_new_release":self.new_release,
            "news_free_games_now":self.free_games_now,
            "news_event_history":self.event_history_steam_facts,
            "news_discounts_steam_now":self.news_discounts_steam,
            "news_top_for_a_coins":self.top_for_a_coins,
            "news_random_game":self.random_game,
            "news_calendar_event_now":self.get_calendar_event_now,
            "news_game_from_ganre":self.game_from_ganre,
            "news_game_from_categorie":self.game_from_categories
        }
        self.get_game_from_ganre_name_use_case = GetGameFromGanreNameUseCase(
            news_repository=news_repository
        )

    def event_history_steam_facts(self,session)->Optional[List[dict]]:
        return self.event_history_steam_facts_use_case.execute(session=session)

    def free_games_now(self,session)->Optional[List[dict]]:
        data:List[int] = self.free_games_now_use_case.execute(session=session)
        if data is None or len(data) == 0:
            return None
        else:
            full_data = [
                self.get_game_correct_data.execute(data = self.get_game_stats_use_case.execute_sync(steam_id=i),game_id=i,full=True)
                for i in data
            ]
        return full_data

    def summary_statistics_steam(self,session)->Optional[List[dict]]:
        return self.summary_statistics_steam_use_case.execute(session=session)

    def news_discounts_steam(self,session)->Optional[List[dict]]:
        return self.new_discounts_steam_use_case.execute(session=session,limit=5)

    def top_for_a_coins(self,session)->Optional[List[dict]]:
        return self.top_for_a_coins_use_case.execute(min_price=20000,session=session)

    def random_game(self,session)->Optional[List[dict]]:
        return self.random_game_sync_use_case.execute(session=session)

    def new_release(self,session)->Optional[List[dict]]:
        return self.new_release_use_case.execute(session=session)

    #В майбутньому
    def _guess_the_game(self):
        pass

    def get_calendar_event_now(self,session):
        return self.calendar_event_now_use_case.execute(session=session)

    def update_calendar_events(self,session):
        return self.update_calendar_events_use_case.execute(session=session)

    def game_from_ganre(self,ganre_name:str,session)->Optional[dict]:
        return self.get_game_from_ganre_name_use_case.execute(ganre_name=ganre_name,session=session)

    def game_from_categories(self,categories:str,session)->Optional[dict]:
        return self.get_game_from_category_name_use_case.execute(category = categories,session=session)

    def dispathcher(self,func_name:str,*args,**kwargs):
        try:
            return self.dispatcher_command[func_name](*args,**kwargs)
        except KeyError as e:
            raise KeyError(e)
        except Exception as e:
            self.logger.error(f"Error {e}",exc_info=True)
            raise e