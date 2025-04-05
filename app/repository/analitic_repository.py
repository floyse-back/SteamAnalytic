from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select,text
from app.models.steam import Game



class AnaliticRepository:
    """Репозиторій для роботи з аналітикою даних"""
    async def get_games_for_appids(self,session:AsyncSession,appid_list: list[int]):
        games_get = await session.execute(select(Game).filter(Game.steam_appid.in_(appid_list)))

        return games_get.scalars().unique().all()
