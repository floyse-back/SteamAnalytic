from .models import SteamBase
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from sqlalchemy import select


class CRUD:
    async def get_most_played_page(self,async_session:async_sessionmaker[AsyncSession],page:int,limit:int):
        statement = select(SteamBase).order_by(SteamBase.positive).offset((page - 1) * limit).limit(limit)

        async with async_session() as session:
            result = await session.execute(statement)
            return result.scalars().all()

    async def get_most_discount_games(self,async_session:async_sessionmaker[AsyncSession],page:int,limit:int):
        statement = select(SteamBase).order_by(SteamBase.discount).filter(SteamBase.discount > 80).offset((page - 1) * limit).limit(limit)

        async with async_session() as session:
            result = await session.execute(statement)
            return result.scalars().all()