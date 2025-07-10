from typing import List

from app.application.dto.steam_dto import GameShortModel
from app.application.usecases.subscribes_use_cases.event_new_use_case import EventNewUseCase
from app.application.usecases.subscribes_use_cases.free_games_now_use_case import FreeGamesNowSyncUseCase
from app.application.usecases.subscribes_use_cases.game_changed_wishlist_appids_use_case import \
    GameChangesWishlistAppidsUseCase
from app.application.usecases.subscribes_use_cases.hot_discount_games_use_case import HotDiscountUseCase
from app.application.usecases.subscribes_use_cases.new_release_use_case import NewReleaseUseCase
from app.domain.steam.sync_repository import ISubscribesRepository, INewsRepository


class SubscribesService:
    def __init__(self,subscribes_repository: ISubscribesRepository,news_repository: INewsRepository):
        self.free_games_now_use_case =  FreeGamesNowSyncUseCase(
        )
        self.hot_discount_games_use_case = HotDiscountUseCase(

        )
        self.event_new_use_case = EventNewUseCase(

        )
        self.wishlist_game_discount_use_case = GameChangesWishlistAppidsUseCase(

        )
        self.new_release_use_case = NewReleaseUseCase(

        )

    def new_release(self)->GameShortModel:
        return self.new_release_use_case.execute()

    def free_games_now(self)->GameShortModel:
        return self.free_games_now_use_case.execute()

    def event_new(self):
        self.event_new_use_case.execute()

    def wishlist_game_discount(self,appids:List[int]):
        self.wishlist_game_discount_use_case.execute()

    def hot_discount_games(self)->GameShortModel:
        self.hot_discount_games_use_case.execute()