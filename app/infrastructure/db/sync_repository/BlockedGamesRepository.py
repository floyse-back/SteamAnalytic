from typing import List

from sqlalchemy import select, Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.domain.steam.sync_repository import IBlockedGamesRepository
from app.infrastructure.db.models.steam_models import BlockedGames


class BlockedGamesRepository(IBlockedGamesRepository):
    def add_blocked_games(self,appid,session):
        statement = insert(BlockedGames).values(
            appid=appid
        ).on_conflict_do_nothing(index_elements=["appid"])
        session.execute(statement)
        session.commit()

    def get_blocked_games_from_appids(self, appids:List, session:Session)->Sequence[BlockedGames]:
        statement = select(
            BlockedGames
        ).where(BlockedGames.appid.in_(appids))
        result = session.execute(statement)
        return result.scalars().all()
