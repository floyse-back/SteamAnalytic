from typing import List

from app.domain.logger import ILogger
from app.domain.steam.sync_repository import IGameWishlistRepository


class UpdateGameWishlistUseCase:
    def __init__(self, wishlist_repository:IGameWishlistRepository,logger:ILogger):
        self.wishlist_repository = wishlist_repository
        self.logger = logger

    async def execute(self,session,data:List[dict]):
        self.logger.info("UpdateGameWishlistUseCase EXECUTE ")
        return self.wishlist_repository.get_changed_games(appids=data,session=session)