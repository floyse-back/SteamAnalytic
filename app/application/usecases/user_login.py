from sqlalchemy.ext.asyncio import AsyncSession

from app.application.dto.user_dto import TokenType
from app.domain.logger import ILogger
from app.domain.users.repository import IRefreshTokenRepository
from app.infrastructure.db.models.users_models import UserModel
from app.utils.auth_utils import create_access_token, create_refresh_token


class UserLoginUseCase:
    def __init__(self,refresh_token_repository: IRefreshTokenRepository,logger:ILogger):
        self.refresh_token_repository = refresh_token_repository
        self.logger = logger

    async def execute(self,session: AsyncSession,user:UserModel)->TokenType:
        self.logger.debug("Create Tokens")
        access_token = create_access_token(user)
        refresh_token = create_refresh_token(user)
        self.logger.debug("Access Token %s", access_token)
        self.logger.debug("Refresh Token %s", refresh_token)
        user_id = user.id
        await self.refresh_token_repository.create_refresh_token(
            session=session,
            user_id=user.id,
            refresh_token=refresh_token
        )
        self.logger.info(f"UserLoginUseCase: Create Tokens Successful %s",user_id)

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )