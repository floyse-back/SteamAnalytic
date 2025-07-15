from app.application.exceptions.exception_handler import PasswordIncorrect
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository
from app.utils.utils import verify_password


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,user_password,user_model,session):
        if not verify_password(password=user_password, hashed_password=user_model.hashed_password):
            raise PasswordIncorrect("Password incorrect")
        self.logger.info("DeleteUserUseCaseUser %s Delete Account",user_model.username)
        await self.user_repository.delete_user(session,user_model)