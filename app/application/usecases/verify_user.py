from app.application.exceptions.exception_handler import PasswordIncorrect, UserNotFound
from app.domain.users.repository import IUserRepository
from app.utils.utils import verify_password


class VerifyUserUseCase:
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,username,password):
        user = await self.user_repository.get_user(session, username)

        if not user:
            raise UserNotFound("User not found")

        if not verify_password(password, user.hashed_password):
            raise PasswordIncorrect("Password incorrect")

        return user
