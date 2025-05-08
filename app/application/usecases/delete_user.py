from app.application.dto.user_dto import UserModel
from app.application.exceptions.exception_handler import UserNotPermitions, TokenNotFound, UserNotFound, \
    PasswordIncorrect
from app.domain.users.repository import IUserRepository, IEmailConfirmationRepository
from app.utils.utils import verify_password


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository,email_repository:IEmailConfirmationRepository):
        self.user_repository = user_repository
        self.email_repository = email_repository

    async def execute(self,token,user_password,session):
        email_model = await self.email_repository.verify_confirm_token(token=token,session=session,type="delete_user")
        if not email_model:
            raise TokenNotFound("Token not found")

        user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)

        if not user_model:
            raise UserNotFound("User not found")

        if not verify_password(user_password, user_model.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        await self.user_repository.delete_user(session,user_model)