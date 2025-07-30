from typing import Optional, List

from sqlalchemy import select, desc, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.steam.repository import ISteamRepository
from app.infrastructure.db.models.steam_models import SteamBase, Game, Category, Publisher, Ganres


class SteamRepository(ISteamRepository):
    """Репозиторій для роботи з Steam даними"""

    async def get_top_games(self,session:AsyncSession,page:int,limit:int):
        statement = select(SteamBase).order_by(desc(SteamBase.positive)).offset((page - 1) * limit).limit(limit)

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_most_discount_games(self,session:AsyncSession,page:int,limit:int):
        statement = select(SteamBase).filter(and_(SteamBase.positive >= 1000,SteamBase.positive - SteamBase.negative >=250)).order_by(desc(SteamBase.discount)).offset((page - 1) * limit).limit(limit)

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_free_discount_games(self,session:AsyncSession):
        statement = select(SteamBase).where(SteamBase.discount>=100)

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_steam_appid(self,session:AsyncSession,name:str):
        statement = select(SteamBase.appid).filter(SteamBase.name.ilike(f"%{name}%")).limit(1)

        result = await session.execute(statement)
        return result.scalars().first()

    async def search_game(self,session,page:int= 1,limit:int = 10,name:str = None,category = None,ganre = None,discount = None,publisher = None,to_price = None,out_price = None) -> Optional[List[Game]]:
        statement = (
            select(Game)
        )

        if category:
            statement = statement.filter(Category.category_name.in_(category))
        if ganre:
            statement = statement.filter(Ganres.ganres_name.in_(ganre))
        if publisher:
            statement = statement.filter(Publisher.publisher_name.in_(publisher))

        if name:
            name=name.lower()
            statement = statement.filter(Game.name.ilike(f"%{name}%")).order_by(desc(Game.recomendations))
        if discount:
            statement = statement.filter(Game.discount >= discount)
        if to_price:
            statement = statement.filter(Game.final_price >= to_price)
        if out_price:
            statement = statement.filter(Game.final_price <= out_price)

        statement = statement.offset((page - 1)*limit).limit(limit)

        result = await session.execute(statement)
        return result.unique().scalars().all()


