from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.users.repository import IRefreshTokenRepository
from app.infrastructure.db.models.users_models import RefreshToken


class RefreshTokenRepository(IRefreshTokenRepository):
    """Репозиторій для роботи з RefreshToken"""
    async def verify_refresh_token(self,session,refresh_token):
        token_get = await session.execute(select(RefreshToken).filter(RefreshToken.refresh_token == refresh_token))
        result = token_get.scalars().first()

        if not result:
            return False

        return True

    async def delete_refresh_token(self,session:AsyncSession,refresh_token):
        stmt = delete(RefreshToken).where(RefreshToken.refresh_token == refresh_token)

        await session.execute(stmt)
        await session.commit()

    async def delete_refresh_from_id(self,session:AsyncSession,user_id):
        stmt = delete(RefreshToken).where(RefreshToken.user_id == user_id)

        await session.execute(stmt)

        await session.commit()

    async def create_refresh_token(self,session:AsyncSession,user_id,refresh_token):
        token_model  =RefreshToken(
            user_id = user_id,
            refresh_token=refresh_token
        )

        session.add(token_model)
        await session.commit()
