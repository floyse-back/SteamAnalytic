from typing import List, Optional

from app.domain.steam.sync_repository import ISubscribesRepository


class SubscribesRepository(ISubscribesRepository):
    def wishlist_game_discount(self,appids: List[int]) -> Optional[dict]:
        pass