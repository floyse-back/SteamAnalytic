from app.application.exceptions.exception_handler import UserNotFound, TokenNotFound
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.infrastructure.logger.logger import logger


class EmailVerifyConfirmUseCase:
    def __init__(self,email_repository:IEmailConfirmationRepository,user_repository:IUserRepository):
        self.email_repository = email_repository
        self.user_repository = user_repository

    async def execute(self,session,type,token):
        logger.debug(f"Verifying email confirmation for {type}")
        email_model = await  self.email_repository.verify_confirm_token(session=session,type=type,token=token)
        logger.debug(f"Email confirmation")
        if not email_model:
            raise TokenNotFound()

        logger.debug(f"User Model Get")
        user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)
        logger.debug(f"User Model Check")
        if not user_model:
            raise UserNotFound()

        logger.debug(f"User Model transform to dto")
        await self.email_repository.delete_confirm_token(session=session,type=type,user_id=email_model.user_id)

        if type == "delete_user":
            user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)

        return user_model