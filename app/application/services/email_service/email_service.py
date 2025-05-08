from app.application.usecases.send_email import SendEmailUseCase
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.domain.celery_sender import ICelerySender



class EmailService:
    def __init__(self,user_repository:IUserRepository,email_confirmation_repository: IEmailConfirmationRepository,celery_sender:ICelerySender):
        self.send_email_use_case = SendEmailUseCase(
            email_repository=email_confirmation_repository,
            celery_sender=celery_sender,
            user_repository=user_repository,
        )

    async def send_email(self,session,email,type:str):
        return await self.send_email_use_case.execute(session,email,type)