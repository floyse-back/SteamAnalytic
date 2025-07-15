from app.application.usecases.send_email import SendEmailUseCase
from app.domain.logger import ILogger
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.domain.celery_sender import ICelerySender



class NotificationService:
    def __init__(self,user_repository:IUserRepository,email_confirmation_repository: IEmailConfirmationRepository,celery_sender:ICelerySender,logger:ILogger):
        self.send_email_use_case = SendEmailUseCase(
            email_repository=email_confirmation_repository,
            celery_sender=celery_sender,
            user_repository=user_repository,
            logger = logger
        )
        self.logger = logger

    async def send_email(self,session,email,type:str):
        self.logger.info(f"NotificationService: Create task sending %s email to %s",type,email)
        return await self.send_email_use_case.execute(session,email,type)