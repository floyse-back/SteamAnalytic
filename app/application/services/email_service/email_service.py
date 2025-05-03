from app.application.exceptions.exception_handler import TokenNotFound
from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.domain.celery_sender import ICelerySender
import uuid

from app.utils.config import BASE_DIR


class EmailService:
    def __init__(self,user_repository:IUserRepository,email_confirmation_repository: IEmailConfirmationRepository,celery_sender:ICelerySender):
        self.email_repository = email_confirmation_repository
        self.celery_sender = celery_sender
        self.user_repository = user_repository

        self.handlers_confirm = {
            "verify_email":self.confirm_email,
            "forgot_password":self.confirm_forgout_password,
            "delete_user":self.confirm_delete_user,
        }
        self.base_url = F"{BASE_DIR}/api/v1/"
        self.url = {
            "verify_email":'verify_url/?type=verify_email',
            "forgot_password":'verify_url/?type=forgot_password',
            "delete_user":'verify_url/?type=delete_user'
        }

    async def send_email(self,session,receiver:str,type:str):
        verify_token = await self.create_email_code()
        url = self.base_url+self.url[f"{type}"]+f"&token={verify_token}"
        user_model = await self.user_repository.get_user_for_email(receiver,session)
        if user_model is None:
            raise Exception

        await self.email_repository.create_confirm_token(session=session,token=verify_token,type=type,user_model=user_model)
        await self.celery_sender.send_email(receiver=receiver,type=type,url=url)

    async def verify_url(self,session,token,type:str):
        email_model = self.email_repository.verify_confirm_token(session=session,type=type,token=token)
        if not email_model:
            raise TokenNotFound()

        try:
            await self.handlers_confirm[type]()
        except KeyError:
            raise KeyError()

    async def confirm_forgout_password(self):
        print("Hello World")

    async def confirm_email(self):
        print("Hello World 2")

    async def confirm_delete_user(self):
        print("Hello World 3")

    async def create_email_code(self):
        return str(uuid.uuid4())
