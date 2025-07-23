from typing import List, Optional

from sqlalchemy import select

from app.domain.steam.sync_repository import IGameWishlistRepository
from app.infrastructure.db.models.steam_models import Game
from app.infrastructure.logger.logger import Logger


class GameWishlistRepository(IGameWishlistRepository):
    def wishlist_game_discount(self,appids: List[int],session) -> Optional[dict]:
        pass

    def get_changed_games(self,appids: List[dict],session) -> Optional[List]:
        logger = Logger(name="infrastructure.wishlist_repository",file_path="infrastructure")
        logger.info("Get changed games %s",appids)
        only_appids = [appid['steam_appid'] for appid in appids]
        statement = select(
            Game.steam_appid,
            Game.name,
            Game.short_description,
            Game.initial_price,
            Game.final_price,
            Game.discount,
            Game.initial_price,
            Game.final_formatted_price,
        ).where(Game.steam_appid.in_(only_appids))

        result = session.execute(statement)
        return result.all()

