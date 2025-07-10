from datetime import date
from typing import Optional, List, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func, cast,Integer

from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.db.models.steam_models import Game, SteamBase, SteamReserveBase


class NewsRepository(INewsRepository):
    def free_games_now(self,session)->Optional[Sequence[SteamBase.appid]]:
        statement = select(SteamBase.appid).outerjoin(SteamReserveBase,SteamBase.appid==SteamReserveBase.appid)\
        .filter(and_(SteamBase.discount==100,SteamReserveBase.discount!=100))
        result=session.execute(statement)
        return result.scalars().all()

    def summary_statistics_steam(self,session)->Optional[dict]:
        pass

    def news_discounts_steam(self,session,limit:int=5)->Optional[List[Game]]:
        statement = select(Game).outerjoin(SteamReserveBase,cast(SteamReserveBase.appid,Integer)==Game.steam_appid)\
        .filter(and_(Game.discount>func.coalesce(SteamReserveBase.discount,0),Game.discount>=60,Game.discount!=100)).order_by(Game.discount,Game.final_price).limit(limit)
        result=session.execute(statement)
        return result.scalars().all()

    def game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        pass

    def random_game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        pass

    def new_release(self,session:Session,now_date:date=date.today())-> Sequence[Game]:
        statement = select(Game).where(Game.release_data==now_date)
        result = session.execute(statement).unique()
        return result.scalars().unique().all()

    def new_release_from_this_month(self,session,now_date:date=date.today())->Optional[List[Game]]:
        pass

    def event_history_steam_facts(self,session,now_date_list:List[date]=date.today())->Optional[List[Game]]:
        statement = select(Game).where(Game.release_data.in_(now_date_list)).limit(25)
        result = session.execute(statement).unique()
        return result.scalars().unique().all()