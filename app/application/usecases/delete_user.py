from app.application.dto.user_dto import UserModel
from app.application.exceptions.exception_handler import UserNotPermitions, TokenNotFound, UserNotFound, \
    PasswordIncorrect
from app.domain.users.repository import IUserRepository, IEmailConfirmationRepository
from app.utils.utils import verify_password


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,user_password,user_model,session):
        if not verify_password(user_password, user_model.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        await self.user_repository.delete_user(session,user_model)