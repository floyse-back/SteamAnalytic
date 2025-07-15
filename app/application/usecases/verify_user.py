from app.application.exceptions.exception_handler import PasswordIncorrect, UserNotFound
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository
from app.utils.utils import verify_password


class VerifyUserUseCase:
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,session,username,password):
        user = await self.user_repository.get_user(session, username)

        if not user:
            self.logger.info(f"VerifyUserUseCase: User not found {username}")
            raise UserNotFound("User not found")

        if not verify_password(password, user.hashed_password):
            self.logger.info(f"VerifyUserUseCase: Password incorrect {username}")
            raise PasswordIncorrect("Password incorrect")

        return user
