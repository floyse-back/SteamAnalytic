from app.application.dto.user_dto import UserModel
from app.application.exceptions.exception_handler import UserNotPermitions
from app.domain.users.repository import IUserRepository


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,user:UserModel):
        if user.role == "admin":
            raise UserNotPermitions

        await self.user_repository.delete_user(session,user)
