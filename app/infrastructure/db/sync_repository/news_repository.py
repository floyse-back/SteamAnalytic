from datetime import date
from typing import Optional, List, Sequence

from sqlalchemy.orm import Session
from sqlalchemy import select, and_, func, cast, Integer, or_

from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.db.models.steam_models import Game, SteamBase, SteamReserveBase


class NewsRepository(INewsRepository):
    def free_games_now(self,session)->Optional[Sequence[SteamBase.appid]]:
        statement = select(SteamBase.appid).outerjoin(SteamReserveBase,SteamBase.appid==SteamReserveBase.appid)\
        .filter(and_(SteamBase.discount==100,SteamReserveBase.discount!=100))
        result=session.execute(statement)
        return result.scalars().all()

    def summary_statistics_steam(self,session)->Optional[dict]:
        return {"Sonn":"Don`t Created"}

    def news_discounts_steam(self,session,limit:int=5,final_price:int=500)->Optional[List[Game]]:
        statement = select(Game).outerjoin(SteamReserveBase,cast(SteamReserveBase.appid,Integer)==Game.steam_appid)\
        .filter(and_(Game.discount>func.coalesce(SteamReserveBase.discount,0),Game.discount>=75,Game.discount!=100)).order_by(SteamBase).limit(limit)
        result=session.execute(statement)
        return result.scalars().unique().all()

    def game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        statement = select(Game).outerjoin(SteamBase,cast(SteamBase.appid,Integer)==Game.steam_appid)\
        .filter(and_(Game.final_price>0,
                     Game.final_price<=price,
                     Game.release_data==date(year=2018,month=1,day=1),
                     or_(cast(Game.metacritic,Integer)>=85, 100*SteamBase.positive/(SteamBase.positive+SteamBase.negative)>85),
                     SteamBase.average_2weeks > 150
                     )
        )
        result = session.execute(statement)
        return result.scalars().unique().all()

    def random_game_from_price(self,session:Session,price:int,limit:int=2)->Optional[Sequence[Game]]:
        statement = select(Game).filter(Game.final_price>price,cast(Game.metacritic,Integer)>=70).order_by(func.random()).limit(limit)
        result = session.execute(statement)
        return result.scalars().unique().all()

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