from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, case, and_
from sqlalchemy import func

from app.domain.steam.repository import IAnaliticsRepository
from app.infrastructure.db.models.steam_models import Game,Ganres,Category,GanreToMany,CategoryToMany
from typing import List


class AnaliticRepository(IAnaliticsRepository):
    """Репозиторій для роботи з аналітикою даних"""
    async def get_games_for_appids(self,session:AsyncSession,appid_list: List[int]):
        games_get = await session.execute(select(Game).filter(Game.steam_appid.in_(appid_list)))

        return games_get.scalars().unique().all()

    async def games_for_you(self,session:AsyncSession,ganres_data:List,category_data:List,steam_appids:List):
        ganre_cases = [ (Ganres.ganres_name == f'{ganre[0]}',ganre[1]) for ganre in ganres_data ]
        category_case = [ (Category.category_name == f'{category[0]}',category[1]) for category in category_data ]

        query = (select(
            Game.steam_appid,
            Game.name,
            Game.img_url,
            func.sum(
                case(*ganre_cases,else_=0) + case(*category_case,else_=0)
            ).label("total")
        ).join(GanreToMany,GanreToMany.game_id==Game.steam_appid) \
        .join(Ganres,Ganres.ganres_id==GanreToMany.ganre_id) \
        .join(CategoryToMany, CategoryToMany.game_id == Game.steam_appid, isouter=True) \
        .join(Category, Category.category_id == CategoryToMany.category_id, isouter=True).where(Game.steam_appid.notin_(steam_appids)) \
        .group_by(Game.name,Game.steam_appid,Game.img_url)).limit(100)

        subquery = query.subquery()

        final_query = select(subquery.c.steam_appid,subquery.c.name,subquery.c.img_url,subquery.c.total).order_by(subquery.c.total.desc())

        result = await session.execute(final_query)
        results = result.fetchall()

        return [{"appid":r[0],"name": r[1],"steam_img":r[2], "total": r[3]} for r in results]

    async def salling_for_you(self,session:AsyncSession,ganres_data:List,category_data:List,steam_appids:List):
        ganre_cases = [ (Ganres.ganres_name == f'{ganre[0]}',ganre[1]) for ganre in ganres_data ]
        category_case = [ (Category.category_name == f'{category[0]}',category[1]) for category in category_data ]

        query = (select(
            Game.steam_appid,
            Game.name,
            Game.img_url,
            Game.discount,
            func.sum(
                case(*ganre_cases,else_=0) + case(*category_case,else_=0)
            ).label("total")
        ).join(GanreToMany,GanreToMany.game_id==Game.steam_appid) \
        .join(Ganres,Ganres.ganres_id==GanreToMany.ganre_id) \
        .join(CategoryToMany, CategoryToMany.game_id == Game.steam_appid, isouter=True) \
        .join(Category, Category.category_id == CategoryToMany.category_id, isouter=True).where(and_(Game.steam_appid.notin_(steam_appids), Game.discount >= 70)) \
        .group_by(Game.name,Game.steam_appid,Game.img_url,Game.discount)).limit(100)

        subquery = query.subquery()

        final_query = select(subquery.c.steam_appid,subquery.c.name,subquery.c.img_url,subquery.c.total,subquery.c.discount).order_by(subquery.c.total.desc())

        result = await session.execute(final_query)
        results = result.fetchall()

        return [{"appid":r[0],"name": r[1],"steam_img":r[2], "total": r[3],"discount":r[4]} for r in results]