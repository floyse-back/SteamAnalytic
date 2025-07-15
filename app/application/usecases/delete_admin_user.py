from app.application.dto.user_dto import UserModelDTO, transform_to_dto, UserShortDTO
from app.application.exceptions.exception_handler import UserNotPermitions
from app.domain.logger import ILogger
from app.domain.users.repository import IUserRepository


class DeleteUserUseCase:
    """Клас для видалення користувача"""
    def __init__(self,user_repository:IUserRepository,logger:ILogger):
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,session,user:UserModelDTO):
        if user.role == "admin":
            self.logger.debug(f"%s is not admin",user.username)
            raise UserNotPermitions
        await self.user_repository.delete_user(session,user)
        self.logger.info(f"User %s:%s is deleted",user.id,user.username)