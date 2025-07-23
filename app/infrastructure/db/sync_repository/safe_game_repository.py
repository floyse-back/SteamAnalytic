from typing import List

from sqlalchemy import select, Sequence
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.domain.steam.sync_repository import ISafegameRepository
from app.infrastructure.db.models.steam_models import SafeGames


class SafeGameRepository(ISafegameRepository):
    def add_safe_games(self,appid:int,session:Session):
        statement = insert(SafeGames).values(
            appid=appid
        ).on_conflict_do_nothing(index_elements=["appid"])
        session.execute(statement)
        session.commit()

    def get_safe_games_from_appids(self, appids:List, session:Session)->Sequence[SafeGames]:
        statement = select(
            SafeGames
        ).where(SafeGames.appid.in_(appids))
        result = session.execute(statement)
        return result.scalars().all()