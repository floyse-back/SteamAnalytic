from email.mime.text import MIMEText

from app.domain.email_sender import IEmailSender
from app.utils.config import EMAIL_PASSWORD, EMAIL_NAME,EMAIL_SERVER,EMAIL_PORT,EMAIL_SENDER
import smtplib
from email.mime.multipart import MIMEMultipart

class EmailSender(IEmailSender):
    """Відправка EMAIL"""
    def __init__(self):
        self.email_name = EMAIL_NAME
        self.email_password = EMAIL_PASSWORD
        self.email_server = EMAIL_SERVER
        self.email_port = EMAIL_PORT
        self.email_sender = EMAIL_SENDER
        self.server = self.connect_server()

    def connect_server(self):
        server = smtplib.SMTP(self.email_server,self.email_port)
        server.esmtp_features['auth'] = "LOGIN PLAIN"
        server.login(self.email_name,self.email_password)

        return server

    def send_email(self,receiver,part):
        message = MIMEMultipart()
        message['From'] = self.email_sender
        message['To'] = receiver
        message['Subject'] = "Steam Analitics"

        message.attach(part)

        self.server.sendmail(self.email_sender,receiver,message.as_string())

    def health_live(self,receiver):
        html ="""
        <html>
        <body>
            <p>Hi,<br></p>
            Server Start.</p>
        </body>
        </html>
        """
        part = MIMEText(html,'html')

        self.send_email(receiver,part)



    def forgout_password(self):
        pass

    def delete_account(self):
        pass

    def authenticate(self):
        pass
