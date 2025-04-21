from app.utils.config import EMAIL_PASSWORD, EMAIL_NAME



class EmailSender:
    def __init__(self):
        self.email_name = EMAIL_NAME
        self.email_password = EMAIL_PASSWORD

    def send_email(self,message:str,email):
        pass

    def forgout_password(self):
        pass

    def delete_account(self):
        pass

    def authenticate(self):
        pass
