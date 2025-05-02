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
            <!DOCTYPE html>
            <html lang="en">
            <body style="background-color: rgb(245, 237, 237);width: 100%;margin: 0;padding: 0;align-items: center;">
                <header style="background-color: rgb(35, 93, 179);;margin: 0;padding: 5px;">
                    <h1 style="text-align: center;color: white;">Steam Analitic</h1>
                </header>
                <div style="text-align: center;">
                    <h3>Hello User you need verify account</h3>
                </div>
                <div style= "display: flex;justify-content: center;margin-top:50px;">
                    <div style="">
                        <a style="background-color: rgb(35, 93, 179); border-radius: 0.75em;border: solid 0px;padding:10px 60px;text-align: center;color: white; font-size: 2em;font-family: Arial, Helvetica, sans-serif;">Get Started</a>
                    </div>
                </div>
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
