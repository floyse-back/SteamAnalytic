from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.steam.repository import ISteamRepository
from app.infrastructure.db.models.steam_models import SteamBase


class SteamRepository(ISteamRepository):
    """Репозиторій для роботи з Steam даними"""

    async def get_top_games(self,session:AsyncSession,page:int,limit:int):
        statement = select(SteamBase).order_by(desc(SteamBase.positive)).offset((page - 1) * limit).limit(limit)

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_most_discount_games(self,session:AsyncSession,page:int,limit:int):
        statement = select(SteamBase).order_by(desc(SteamBase.discount)).offset((page - 1) * limit).order_by(desc(SteamBase.discount),desc(SteamBase.positive),desc(SteamBase.price)).limit(limit)

        result = await session.execute(statement)
        return result.scalars().all()

    async def get_free_discount_games(self,session:AsyncSession):
        statement = select(SteamBase).where(SteamBase.discount>=100)

        result = await session.execute(statement)
        return result.scalars().all()
