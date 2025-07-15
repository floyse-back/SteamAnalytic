from app.application.dto.user_dto import TokenType
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository
from app.utils.auth_utils import create_access_token


class GetRefreshTokenUseCase:
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,refresh_token:str,user:str,session):
        user_model = await self.user_repository.get_user_for_id(user_id=int(user), session=session)

        access_token = create_access_token(user=user_model)
        self.logger.debug(f"GetRefreshTokenUseCase: Get Refresh Token Successful ",access_token)
        self.logger.info("GetRefreshTokenUseCase: Get Refresh Token Successful %s",user)
        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )