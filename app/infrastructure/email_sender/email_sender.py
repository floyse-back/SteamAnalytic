from app.domain.email_sender import IEmailSender
from app.utils.config import EMAIL_PASSWORD, EMAIL_NAME



class EmailSender(IEmailSender):
    def __init__(self):
        self.email_name = EMAIL_NAME
        self.email_password = EMAIL_PASSWORD

    def send_email(self,email:str,message:str):
        pass

    def forgout_password(self):
        pass

    def delete_account(self):
        pass

    def authenticate(self):
        pass
