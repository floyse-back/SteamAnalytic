from app.application.dto.user_dto import UserModelDTO, transform_to_dto, UserShortDTO
from app.application.exceptions.exception_handler import UserNotPermitions
from app.domain.users.repository import IUserRepository


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository):
        self.user_repository = user_repository

    async def execute(self,session,user:UserModelDTO):
        if user.role == "admin":
            raise UserNotPermitions

        await self.user_repository.delete_user(session,user)
