from app.application.exceptions.exception_handler import UserNotFound, TokenNotFound
from app.domain.logger import ILogger
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository


class EmailVerifyConfirmUseCase:
    def __init__(self,email_repository:IEmailConfirmationRepository,user_repository:IUserRepository,logger:ILogger):
        self.email_repository = email_repository
        self.user_repository = user_repository
        self.logger = logger

    async def execute(self,session,type,token):
        self.logger.debug(f"EmailVerifyConfirmUseCase: Verifying email confirmation for {type}")
        email_model = await  self.email_repository.verify_confirm_token(session=session,type=type,token=token)
        self.logger.debug(f"EmailVerifyConfirmUseCase: Email confirmation")
        if not email_model:
            raise TokenNotFound()

        self.logger.debug(f"EmailVerifyConfirmUseCase: User Model Get")
        user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)
        self.logger.debug(f"EmailVerifyConfirmUseCase: User Model Check")
        if not user_model:
            raise UserNotFound()

        await self.email_repository.delete_confirm_token(session=session,type=type,user_id=email_model.user_id)

        if type == "delete_user":
            user_model = await self.user_repository.get_user_for_id(session=session,user_id=email_model.user_id)

        return user_model