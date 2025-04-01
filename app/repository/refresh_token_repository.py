from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import TokenBase


class RefreshTokenRepository:
    """Репозиторій для роботи з RefreshToken"""
    @staticmethod
    async def verify_refresh_token(session,refresh_token):
        token_get = await session.execute(select(TokenBase).filter(TokenBase.refresh_token == refresh_token))
        result = token_get.scalars().first()

        if not result:
            return False

        return True

    @staticmethod
    async def delete_refresh_token(session:AsyncSession,refresh_token):
        stmt = delete(TokenBase).where(TokenBase.refresh_token == refresh_token)

        await session.execute(stmt)
        await session.commit()

    @staticmethod
    async def create_refresh_token(session:AsyncSession,user_id,refresh_token):
        token_model  =TokenBase(
            user_id = user_id,
            refresh_token=refresh_token
        )

        session.add(token_model)
        await session.commit()
