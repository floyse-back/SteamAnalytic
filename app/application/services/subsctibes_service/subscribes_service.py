from typing import List, Optional, Dict, Callable

from app.application.usecases.news_use_cases.get_calendar_event_now_use_case import GetCalendarEventNowUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.game_changed_wishlist_appids_use_case import \
    GameChangesWishlistAppidsUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.application.usecases.subscribes_use_cases.update_game_wishlist_use_case import UpdateGameWishlistUseCase
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import IGameWishlistRepository, INewsRepository, ICalendarSteamEventRepository


class SubscribesService:
    def __init__(self, wishlist_repository: IGameWishlistRepository, calendar_repository:ICalendarSteamEventRepository, news_repository: INewsRepository,logger:ILogger):
        self.free_games_now_use_case =  FreeGamesNowSyncUseCase(
            news_repository = news_repository,
            logger = logger
        )
        self.hot_discount_games_use_case = HotDiscountUseCase(
            news_repository = news_repository,
            logger=logger
        )
        self.event_new_use_case = GetCalendarEventNowUseCase(
            calendar_repository = calendar_repository,
            logger = logger
        )
        self.wishlist_game_discount_use_case = GameChangesWishlistAppidsUseCase(
            wishlist_repository = wishlist_repository,
            logger = logger
        )
        self.new_release_use_case = NewReleaseUseCase(
            news_repository=news_repository,
            logger = logger
        )
        self.update_game_wishlist_use_case = UpdateGameWishlistUseCase(
            wishlist_repository=wishlist_repository,
            logger = logger
        )
        self.dispatcher_command:Dict[str,Callable] = {

        }
        self.logger = logger

    def new_release(self,session)->List[dict]:
        return self.new_release_use_case.execute(session=session)

    def free_games_now(self,session)->List[dict]:
        return self.free_games_now_use_case.execute(session=session)

    def event_new(self,session)->List[dict]:
        return self.event_new_use_case.execute(session=session)

    def wishlist_game_discount(self,appids:List[int]):
        self.wishlist_game_discount_use_case.execute()

    def hot_discount_games(self,session)->Optional[List[dict]]:
        return self.hot_discount_games_use_case.execute(session=session)

    def update_game_wishlist(self,session,data:List[dict]):
        return self.update_game_wishlist_use_case.execute(session=session,data=data)

    def dispathcher(self,func_name:str,*args,**kwargs):
        try:
            self.logger.debug("Dispatcher Command: %s",func_name)
            return self.dispatcher_command[func_name](*args,**kwargs)
        except KeyError as e:
            raise KeyError(e)
        except Exception as e:
            self.logger.error(e)
            raise e