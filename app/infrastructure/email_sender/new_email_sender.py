import smtplib
from app.domain.email_sender import IEmailSender
from app.infrastructure.celery_app.celery_app import logger
from app.utils.config import EMAIL_PASSWORD, EMAIL_SERVER, EMAIL_PORT, EMAIL_SENDER, ServicesConfig

class EmailSender(IEmailSender):
    """Відправка простих текстових email"""
    def __init__(self):
        self.email_name = EMAIL_SENDER
        self.email_password = EMAIL_PASSWORD  # App password
        self.email_server = EMAIL_SERVER
        self.email_port = EMAIL_PORT
        self.email_sender = EMAIL_SENDER
        self.service_config = ServicesConfig()

        self.type_handlers = {
            "verify_email": self.email_verify,
            "forgot_password": self.forgot_password,
            "delete_user": self.delete_account
        }

    def connect_server(self):
        logger.info(f"Connecting to {self.email_server}")
        server = smtplib.SMTP_SSL("smtp.gmail.com", self.email_port, timeout=10)
        logger.debug(f"Started SMTP connection to {self.email_server}")
        server.login(self.email_name, self.email_password)
        logger.debug(f"Logged in to {self.email_server}")
        return server

    def send_email(self, receiver, token, type):
        subject, body = self.type_handlers[type](receiver, token)
        message = f'Subject:{subject}\n{body}"'
        self.server = self.connect_server()
        message = message.encode('utf-8')
        self.server.sendmail(from_addr=self.email_sender,to_addrs= receiver, msg=message)

    def forgot_password(self, receiver, token):
        subject = "Reset your password – Steam Analytic"
        body = f"""
    Hi there,

    We received a request to reset the password for your Steam Analytic account.

    Code: {token}

    If you didn't request this change, you can safely ignore this email – no changes will be made.

    Best regards,  
    The Steam Analytic Team
    """
        return subject, body

    def delete_account(self, receiver, token):
        subject = "Confirm account deletion – Steam Analytic"
        body = f"""
    Hello,

    We noticed a request to delete your Steam Analytic account.

    Code: {token}

    If you didn't make this request, no action is required.

    Thanks,  
    Steam Analytic Support
    """
        return subject, body


    def email_verify(self, receiver, token):
        subject = "Verify your email address – Steam Analytic"
        body = f"""
    Welcome!

    Please confirm your email address to complete your registration with Steam Analytic.

    Code: {token}

    If you didn’t sign up, just ignore this message.

    Thank you,  
    The Steam Analytic Team
    """
        return subject, body

