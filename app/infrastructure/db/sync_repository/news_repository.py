from datetime import date, timedelta
from typing import Optional, List, Sequence

from sqlalchemy.orm import Session, aliased
from sqlalchemy import select, and_, func, cast, Integer, or_, desc

from app.domain.steam.sync_repository import INewsRepository
from app.infrastructure.db.models.steam_models import Game, SteamBase, SteamReserveBase, Ganres, Category


class NewsRepository(INewsRepository):
    BLOCK_CATEGORIES = ["Демоверсія гри"]
    BLOCK_GANRES = ["Сексуальний вміст","Оголення"]

    def free_games_now(self,session)->Optional[Sequence[SteamBase.appid]]:
        statement = (
            select(SteamBase.appid)
            .outerjoin(SteamReserveBase, SteamBase.appid == SteamReserveBase.appid)
            .outerjoin(Game, cast(SteamBase.appid, Integer) == Game.steam_appid)
            .filter(
                or_(
                    and_(
                        SteamBase.discount == 100,
                        SteamReserveBase.discount != 100
                    ),
                    and_(
                        Game.discount == 100,
                        SteamBase.discount != 100,
                        Game.last_updated == date.today()
                    )
                )
            )
        )
        result=session.execute(statement)
        return result.scalars().all()

    def summary_statistics_steam(self,session)->Optional[dict]:
        return {"Sonn":"Don`t Created"}

    def news_discounts_steam(self,session:Session,limit:int=5)->Optional[List[Game]]:
        final_price: int = 10000

        statement = (select(Game)
        .join(SteamReserveBase,cast(SteamReserveBase.appid,Integer)==Game.steam_appid)
        .join(SteamBase,cast(SteamBase.appid,Integer)==Game.steam_appid)
        .filter(and_(
            SteamBase.discount > SteamReserveBase.discount,
            Game.recomendations >= 6000,
            Game.release_data >= date(year=2018,month=1,day=1),
            Game.discount>=60,Game.discount!=100,
            Game.initial_price >= final_price
        )
        )
        .order_by(desc(Game.discount))
        .limit(5))
        result=session.execute(statement)
        return result.scalars().unique().all()

    def game_from_price(self,session,price:int,limit:int=5)->Optional[List[Game]]:
        Ganre = aliased(Ganres)
        CategoryAlias = aliased(Category)

        statement = (select(Game)
        .outerjoin(SteamBase,cast(SteamBase.appid,Integer)==Game.steam_appid)
        .join(Game.game_categories.of_type(CategoryAlias))
        .join(Game.game_ganre.of_type(Ganre))
        .filter(and_(
                     ~CategoryAlias.category_name.in_(self.BLOCK_CATEGORIES),
                     ~Ganre.ganres_name.in_(self.BLOCK_GANRES),
                     Game.final_price>0,
                     Game.initial_price >= 15000,
                     Game.final_price<=price,
                     Game.release_data>=date(year=2020,month=1,day=1),
                     or_(cast(Game.metacritic,Integer)>=85, 100*SteamBase.positive/(SteamBase.positive+SteamBase.negative)>85),
                     SteamBase.average_2weeks > 150
                    )
        ).order_by(func.random()).limit(5))
        result = session.execute(statement)
        return result.scalars().unique().all()

    def random_game_from_price(self,session:Session,price:int,limit:int=2)->Optional[Sequence[Game]]:
        Ganre = aliased(Ganres)
        CategoryAlias = aliased(Category)

        statement = (select(Game)
        .join(Game.game_ganre.of_type(Ganre))
        .join(Game.game_categories.of_type(CategoryAlias))
        .filter(and_(~CategoryAlias.category_name.in_(self.BLOCK_CATEGORIES),
                ~Ganre.ganres_name.in_(self.BLOCK_GANRES),
                or_(Game.recomendations >= 7000,
                Game.final_price>price,cast(Game.metacritic,Integer)>=70))).order_by(func.random()).limit(limit))
        result = session.execute(statement)
        return result.scalars().unique().all()

    def new_release(self,session:Session,now_date:date=date.today())-> Sequence[Game]:
        CategoryAlias = aliased(Category)
        yestarday = now_date-timedelta(days=1)
        statement = (select(Game).join(Game.game_categories.of_type(CategoryAlias))
        .filter(and_(
            ~CategoryAlias.category_name.in_(self.BLOCK_CATEGORIES),
            Game.release_data == yestarday,
        )).order_by(desc(Game.recomendations)))
        result = session.execute(statement)
        return result.scalars().unique().all()

    def new_release_from_this_month(self,session,now_date:date=date.today())->Optional[List[Game]]:
        pass

    def event_history_steam_facts(self,session,now_date_list:List[date]=date.today())->Optional[List[Game]]:
        CategoryAlias = aliased(Category)
        Ganre = aliased(Ganres)
        statement = (select(Game)
                     .join(Game.game_ganre.of_type(Ganre))
                     .join(Game.game_categories.of_type(CategoryAlias))
                     .filter(and_(
                     Game.release_data.in_(now_date_list),
                     ),
                     Game.recomendations >= 100
        )
                     .order_by(Game.recomendations).limit(5))
        result = session.execute(statement).unique()
        return result.scalars().unique().all()

    def get_game_from_ganre_name(self, ganre_name:str, session)->Optional[Game]:
        Ganre = aliased(Ganres)
        CategoryAlias = aliased(Category)

        statement = (
            select(Game)
            .join(SteamBase, cast(SteamBase.appid, Integer) == Game.steam_appid)
            .join(Game.game_ganre.of_type(Ganre))
            .join(Game.game_categories.of_type(CategoryAlias))
            .filter(
                ~CategoryAlias.category_name.in_(self.BLOCK_CATEGORIES),
                ~Ganre.ganres_name.in_(self.BLOCK_GANRES),
                Ganre.ganres_name.in_([ganre_name]),
                (SteamBase.positive - SteamBase.negative) >= 6000,
                Game.release_data >= date(year=2020, month=1, day=1),
            )
            .order_by(func.random())
            .limit(1)
        )

        result = session.execute(statement)
        return result.scalars().first()

    def get_game_from_categorie_name(self, category_name:str, session)->Optional[Game]:
        Ganre = aliased(Ganres)
        CategoryAlias = aliased(Category)

        statement = (
            select(Game)
            .join(SteamBase, cast(SteamBase.appid, Integer) == Game.steam_appid)
            .join(Game.game_ganre.of_type(Ganre))
            .join(Game.game_categories.of_type(CategoryAlias))
            .filter(
                ~CategoryAlias.category_name.in_(self.BLOCK_CATEGORIES),
                ~Ganre.ganres_name.in_(self.BLOCK_GANRES),
                CategoryAlias.category_name.in_([category_name]),
                (SteamBase.positive - SteamBase.negative) >= 6000,
                Game.release_data >= date(year=2019, month=1, day=1),
            )
            .order_by(func.random())
            .limit(1)
        )

        result = session.execute(statement)
        return result.scalars().first()