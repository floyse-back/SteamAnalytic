from typing import List

from app.domain.steam.sync_repository import IGameWishlistRepository


class UpdateGameWishlistUseCase:
    def __init__(self, wishlist_repository:IGameWishlistRepository):
        self.wishlist_repository = wishlist_repository

    async def execute(self,session,data:List[dict]):
        return self.wishlist_repository.get_changed_games(appids=data,session=session)