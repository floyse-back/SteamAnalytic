from app.application.exceptions.exception_handler import UserRegisterError
from app.domain.users.repository import IUserRepository
from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister
from app.utils.utils import hashed_password


class UserRegisterUseCase:
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,user):
        user.hashed_password = hashed_password(user.hashed_password)

        try:
            await self.user_repository.create_user(session, user)
        except InfrastructureUserRegister:
            raise UserRegisterError("User not registered")

        return {"message":"Register successful"}