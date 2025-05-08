from app.application.dto.user_dto import UserModel
from app.application.exceptions.exception_handler import UserNotFound
from app.domain.users.repository import IUserRepository
from app.infrastructure.logger.logger import Logger

logger = Logger()

class GetUserUseCase:
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,user_id:int|None = None,email: str|None = None,username:str|None = None)->UserModel:
        if user_id != None:
            user_model = await self.user_repository.get_user_for_id(session = session,user_id=user_id)
        elif email != None:
            user_model = await self.user_repository.get_user_for_email(session = session,email=email)
        elif username != None:
            user_model = await self.user_repository.get_user(session = session,username = username)
        else:
            raise UserNotFound

        if user_model == None:
            raise UserNotFound

        logger.info(f"User {user_model.id} is getting a user")

        return user_model