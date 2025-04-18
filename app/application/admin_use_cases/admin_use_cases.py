from app.application.exceptions.exception_handler import UserNotFound
from app.domain.users.repository import IUserRepository
from app.domain.users.schemas import UserModel


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

        return user_model

    async def delete_user(self,session,user_id:int,username:str):
        user_model =await self.get_user(session,user_id,username)

        await self.user_repository.delete_user(session,user_model)

    async def get_user_info(self,session,username:str,user_id:int):
        return await self.get_user(session,user_id,username)