from typing import List, Optional

from app.domain.steam.sync_repository import IGameWishlistRepository
from app.infrastructure.db.models.steam_models import Game


class GameWishlistRepository(IGameWishlistRepository):
    def wishlist_game_discount(self,appids: List[int],session) -> Optional[dict]:
        pass

    def get_changed_games(self,appids: List[dict],session) -> Optional[List[Game]]:
        pass