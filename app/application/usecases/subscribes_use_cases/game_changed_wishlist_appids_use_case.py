from typing import List

from app.domain.steam.sync_repository import IGameWishlistRepository


class GameChangesWishlistAppidsUseCase:
    def __init__(self,wishlist_repository:IGameWishlistRepository) -> None:
        self.wishlist_repository = wishlist_repository

    def execute(self, appids:List[dict],session):
        return self.wishlist_repository.wishlist_game_discount(appids=appids,session=session)