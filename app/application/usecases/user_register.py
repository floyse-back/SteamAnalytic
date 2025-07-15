from app.application.exceptions.exception_handler import UserRegisterError
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository
from app.infrastructure.exceptions.exception_handler import InfrastructureUserRegister
from app.utils.utils import hashed_password


class UserRegisterUseCase:
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,session,user):
        user.hashed_password = hashed_password(user.hashed_password)

        try:
            await self.user_repository.create_user(session, user)
            self.logger.info(f"UserRegisterUseCase: Create User Successful %s",user.username)
        except InfrastructureUserRegister as e:
            self.logger.error(f"UserRegisterUseCase: Create User Successful Error {e}",exc_info=True)
            raise UserRegisterError("User not registered")

        return {"message":"Register successful"}