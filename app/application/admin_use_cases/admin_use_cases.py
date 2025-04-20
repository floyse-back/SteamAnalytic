from app.application.exceptions.exception_handler import UserNotFound, TokenNotFound
from app.domain.users.repository import IUserRepository
from app.domain.users.schemas import UserModel
from app.utils.utils import decode_jwt


class AdminService:
    """Service для реалізації Адмінки"""
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def get_user(self,session,user_id,username:str)->UserModel:
        if user_id != None:
            user_model = await self.user_repository.get_user_for_id(session = session,user_id=user_id)
        elif username != None:
            user_model = await self.user_repository.get_user(session = session,username = username)
        else:
            raise UserNotFound

        if user_model == None:
            raise UserNotFound

        return user_model

    async def delete_user(self,session,user_id:int,username:str):
        user_model =await self.get_user(session,user_id,username)

        await self.user_repository.delete_user(session,user_model)

    async def role_check_user(self,session,token):
        if token == None:
            raise TokenNotFound("Token not found")

        token_decoded = decode_jwt(token)
        user_id = token_decoded["user_id"]

        user_model =await self.get_user(session=session,user_id=user_id,username="")
        if user_model.role == "admin":
            return True
        return False

    async def get_user_info(self,session,username:str,user_id:int):
        data =  await self.get_user(session,user_id,username)
        return data