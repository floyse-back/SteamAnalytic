from app.application.exceptions.exception_handler import TokenNotFound, UserNotPermitions
from app.application.usecases.delete_admin_user import DeleteUserUseCase
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository
from app.domain.users.schemas import UserModel
from app.utils.utils import decode_jwt
from app.application.usecases.get_user import GetUserUseCase

class AdminService:
    """Service для реалізації Адмінки"""
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.logger = logger
        self.get_user_usecase = GetUserUseCase(
            user_repository = user_repository,
            logger = logger
        )
        self.delete_user_usecase = DeleteUserUseCase(
            user_repository = user_repository,
            logger = logger
        )

    async def get_user_info(self,session,user_id:int|None,username:str|None,email:str|None=None)->UserModel:
        self.logger.debug(f"get_user_info %s,%s,%s",user_id,username,email)
        return await self.get_user_usecase.execute(session=session,user_id=user_id,username=username,email=email)

    async def delete_user(self,session,user_id:int,username:str,email:str|None):
        user_model = await self.get_user_usecase.execute(session=session,user_id=user_id,username=username,email=email)

        return await self.delete_user_usecase.execute(session,user_model)


    async def role_check_user(self,session,token):
        self.logger.debug(f"role_check_user {token}")
        if token == None:
            raise TokenNotFound("Token not found")

        token_decoded = decode_jwt(token)
        user_id = token_decoded["user_id"]

        user_model = await self.get_user_usecase.execute(session=session,user_id=user_id)

        self.logger.debug(f"role_check User: %s Role %s",user_model.role,user_model.username)
        if user_model.role == "admin":
            return True

        raise UserNotPermitions("Not Permitted")
