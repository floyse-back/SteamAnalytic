from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user_dto import TokenType
from app.domain.users.repository import IRefreshTokenRepository
from app.utils.auth_utils import create_access_token, create_refresh_token


class UserLoginUseCase:
    def __init__(self,refresh_token_repository: IRefreshTokenRepository):
        self.refresh_token_repository = refresh_token_repository

    async def execute(self,session: AsyncSession,user)->TokenType:
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)

        await self.refresh_token_repository.create_refresh_token(
            session=session,
            user_id=user.id,
            refresh_token=refresh_token
        )

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )