from app.application.exceptions.exception_handler import UserNotFound, TokenNotFound, UserNotPermitions
from app.application.usecases.delete_user import DeleteUserUseCase
from app.domain.users.repository import IUserRepository
from app.domain.users.schemas import UserModel
from app.utils.utils import decode_jwt
from app.application.usecases.get_user import GetUserUseCase

class AdminService:
    """Service для реалізації Адмінки"""
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository
        self.get_user_usecase = GetUserUseCase(
            user_repository = self.user_repository
        )
        self.delete_user_usecase = DeleteUserUseCase(
            user_repository = self.user_repository
        )

    async def get_user_info(self,session,user_id:int|None,username:str|None,email:str|None=None)->UserModel:
        return await self.get_user_usecase.execute(session=session,user_id=user_id,username=username,email=email)

    async def delete_user(self,session,user_id:int,username:str,email:str|None):
        user_model = await self.get_user_usecase.execute(session=session,user_id=user_id,username=username,email=email)

        return await self.delete_user_usecase.execute(session,user_model)


    async def role_check_user(self,session,token):
        if token == None:
            raise TokenNotFound("Token not found")

        token_decoded = decode_jwt(token)
        user_id = token_decoded["user_id"]

        user_model =await self.get_user_usecase.execute(session=session,user_id=user_id)

        if user_model.role == "admin":
            return True
        raise UserNotPermitions("Not Permitted")
