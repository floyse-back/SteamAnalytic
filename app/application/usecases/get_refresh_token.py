from app.application.dto.user_dto import TokenType
from app.domain.users.repository import IUserRepository
from app.utils.auth_utils import create_access_token


class GetRefreshTokenUseCase:
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,refresh_token:str,user:str,session):
        user_model = await self.user_repository.get_user_for_id(user_id=int(user), session=session)

        access_token = create_access_token(user=user_model)

        return TokenType(
            access_token=access_token,
            refresh_token=refresh_token
        )