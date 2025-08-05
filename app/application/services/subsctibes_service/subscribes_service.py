from typing import List, Optional, Dict, Callable

from app.application.usecases.get_free_transform import GetFreeTransformUseCase
from app.application.usecases.get_game_stats import GetGameStatsUseCase
from app.application.usecases.news_use_cases.get_calendar_event_now_use_case import GetCalendarEventNowUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.game_changed_wishlist_appids_use_case import \
    GameChangesWishlistAppidsUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.application.usecases.subscribes_use_cases.update_game_wishlist_use_case import UpdateGameWishlistUseCase
from app.domain.logger import ILogger
from app.domain.steam.sync_repository import IGameWishlistRepository, INewsRepository, ICalendarSteamEventRepository
from app.infrastructure.messages.producer import EventProducer
from app.infrastructure.steam_api.client import SteamClient


class SubscribesService:
    def __init__(self, wishlist_repository: IGameWishlistRepository, calendar_repository:ICalendarSteamEventRepository, news_repository: INewsRepository,logger:ILogger,steam:SteamClient,event_producer:EventProducer):
        self.event_provider =event_producer
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
            "subscribe_new_release":self.new_release,
            "subscribe_free_games_now":self.free_games_now,
            "subscribe_hot_discount_notificate":self.hot_discount_games,
            "subscribe_wishlist_notificate":self.wishlist_game_discount,
            "subscribe_steam_news":self.event_new,
        }
        self.get_game_stats_use_case = GetGameStatsUseCase(
            logger=logger,
            steam=steam
        )
        self.get_game_correct_data = GetFreeTransformUseCase(logger=logger)
        self.logger = logger

    def new_release(self,session)->List[dict]:
        return self.new_release_use_case.execute(session=session)

    def free_games_now(self,session)->List[dict]:
        data:List[int] = self.free_games_now_use_case.execute(session=session)
        if data is None or len(data) == 0:
            return None
        else:
            full_data = [
                self.get_game_correct_data.execute(data = self.get_game_stats_use_case.execute_sync(steam_id=i),game_id=i,full=True)
                for i in data
            ]
        return full_data

    def event_new(self,session)->List[dict]:
        return self.event_new_use_case.execute(session=session)

    def wishlist_game_discount(self,appids:List[dict],session):
        self.wishlist_game_discount_use_case.execute(appids=appids,session=session)

    def hot_discount_games(self,session)->Optional[List[dict]]:
        return self.hot_discount_games_use_case.execute(session=session,limit=5)

    def update_game_wishlist(self,session,data:List[dict]):
        data =  self.update_game_wishlist_use_case.execute(session=session,data=data)
        self.logger.info(f"Data Update Game Wishlist {data}")
        self.event_provider.send_message(body = {"type":"send_and_update_wishlist_games","status":True,"data":data},queue="subscribe_queue")

    def dispathcher(self,func_name:str,*args,**kwargs):
        try:
            self.logger.debug("Dispatcher Command: %s",func_name)
            return self.dispatcher_command[func_name](*args,**kwargs)
        except KeyError as e:
            self.logger.warning(f"Dispatcher Command {func_name} not defined: {e}")
            raise KeyError(e)
        except Exception as e:
            self.logger.error(e)
            raise e