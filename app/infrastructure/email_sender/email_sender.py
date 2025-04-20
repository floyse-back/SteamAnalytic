from app.utils.config import EMAIL_PRIVATE_API,EMAIL_PUBLIC_API



class EmailSender:
    def __init__(self):
        self.email_private_api = EMAIL_PRIVATE_API
        self.email_public_api = EMAIL_PUBLIC_API

    def send_email(self,message:str,email):
        pass

    def forgout_password(self):
        pass

    def delete_account(self):
        pass

    def authenticate(self):
        pass
