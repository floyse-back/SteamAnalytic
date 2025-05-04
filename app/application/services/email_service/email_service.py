from app.domain.users.repository import IEmailConfirmationRepository, IUserRepository
from app.domain.celery_sender import ICelerySender
import uuid

from app.utils.config import HOST


class EmailService:
    def __init__(self,user_repository:IUserRepository,email_confirmation_repository: IEmailConfirmationRepository,celery_sender:ICelerySender):
        self.email_repository = email_confirmation_repository
        self.celery_sender = celery_sender
        self.user_repository = user_repository

        self.handlers_confirm = {
            "verify_email":self.confirm_email,
            "forgot_password":self.confirm_forgot_password,
            "delete_user":self.confirm_delete_user,
        }
        self.base_url = f"{HOST}/api/v1/"
        self.url = {
            "verify_email":'verify_url/verify_email/',
            "forgot_password":'verify_url/forgot_password/',
            "delete_user":'verify_url/delete_user/'
        }

    async def send_email(self,session,email,type:str):
        if self.url[type] != None:
            raise IncorrectType()

        verify_token = await self.create_email_code()
        user_model = await self.user_repository.get_user_for_email(email,session)
        receiver = user_model.email
        url = self.base_url+self.url[f"{type}"]+f"?token={verify_token}"
        if user_model is None:
            raise Exception

        await self.email_repository.delete_confirm_token(session,type,user_model.id)
        await self.email_repository.create_confirm_token(session=session,token=verify_token,type=type,user_model=user_model)
        await self.celery_sender.send_email(receiver=receiver,type=type,url=url)

    async def confirm_forgot_password(self):
        print("Hello World")

    async def confirm_email(self,session,user_model):
        await self.user_repository.user_verify_update(session=session,status=True,user_model=user_model)

    async def confirm_delete_user(self,session,user_model):
        await self.user_repository.delete_user(session,user_model)

    async def create_email_code(self):
        return str(uuid.uuid4())
