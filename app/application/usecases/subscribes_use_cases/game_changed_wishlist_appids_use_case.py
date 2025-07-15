from typing import List

from app.domain.logger import ILogger
from app.domain.steam.sync_repository import IGameWishlistRepository


class GameChangesWishlistAppidsUseCase:
    def __init__(self,wishlist_repository:IGameWishlistRepository,logger:ILogger) -> None:
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    def execute(self, appids:List[dict],session):
        self.logger.info("GameChangesWishlistAppidsUseCase EXECUTE")
        return self.wishlist_repository.wishlist_game_discount(appids=appids,session=session)