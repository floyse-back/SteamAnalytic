import uuid

from app.application.exceptions.exception_handler import IncorrectType, UserNotFound
from app.domain.celery_sender import ICelerySender
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.infrastructure.celery_app.senders.celery_sender import CelerySender
from app.utils.config import HOST


class SendEmailUseCase:
    def __init__(self,email_repository:IEmailConfirmationRepository,user_repository:IUserRepository,celery_sender:ICelerySender):
        self.email_repository = email_repository
        self.user_repository = user_repository
        self.celery_sender = celery_sender

        self.base_url = f"{HOST}/api/v1/"
        self.url = {
            "verify_email":'verify_url/verify_email/',
            "forgot_password":'verify_url/forgot_password/',
            "delete_user":'verify_url/delete_user/'
        }

    async def execute(self,session,email,type:str):
        if self.url[f"{type}"]==None:
            raise IncorrectType()

        verify_token = self.__create_email_code()
        user_model = await self.user_repository.get_user_for_email(email,session)

        if not user_model:
            raise UserNotFound()

        receiver = user_model.email
        url =f"?token={verify_token}"
        if user_model is None:
            raise Exception

        await self.email_repository.delete_confirm_token(session,type,user_model.id)
        await self.email_repository.create_confirm_token(session=session,token=verify_token,type=type,user_model=user_model)
        await self.celery_sender.send_email(receiver=receiver,type=type,url=url)


    def __create_email_code(self):
        return str(uuid.uuid4())