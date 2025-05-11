from email.mime.text import MIMEText

from app.domain.email_sender import IEmailSender
from app.utils.config import EMAIL_PASSWORD, TEST_EMAIL_NAME,TEST_EMAIL_SERVER,TEST_EMAIL_PASSWORD,TEST_EMAIL_PORT,TEST_EMAIL_SENDER
import smtplib
from email.mime.multipart import MIMEMultipart

class EmailSenderTest(IEmailSender):
    """Відправка EMAIL"""
    def __init__(self):
        self.email_name = TEST_EMAIL_NAME
        self.email_password = EMAIL_PASSWORD
        self.email_server = TEST_EMAIL_SERVER
        self.email_port = TEST_EMAIL_PORT
        self.email_sender = TEST_EMAIL_SENDER
        self.server = self.connect_server()

        self.type_handlers = {
            "verify_email": self.email_verify,
            "forgot_password": self.forgot_password,
            "delete_user": self.delete_account
        }

    def connect_server(self):
        server = smtplib.SMTP(self.email_server,self.email_port)
        server.esmtp_features['auth'] = "LOGIN PLAIN"
        server.login(self.email_name,self.email_password)

        return server

    def send_email(self,receiver,url,type):
        part = self.type_handlers[type](receiver,url)

        message = MIMEMultipart()
        message['From'] = self.email_sender
        message['To'] = receiver
        message['Subject'] = "Steam Analitics"

        message.attach(part)

        self.server.sendmail(self.email_sender,receiver,message.as_string())

    def forgot_password(self,receiver,url):
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <body style="background-color: rgb(245, 237, 237);width: 100%;margin: 0;padding: 0;align-items: center;">
                <header style="background-color: rgb(35, 93, 179);;margin: 0;padding: 5px;">
                    <h1 style="text-align: center;color: white;">Steam Analitic</h1>
                </header>
                <div style="text-align: center;">
                    <h1>You Forgot Password</h1>
                    <h3>Hello User you forgot password</h3>
                </div>
                <div style= "display: flex;justify-content: center;margin-top:50px;">
                    <div style="">
                        <a href="{url}" style="background-color: rgb(35, 93, 179); border-radius: 0.75em;border: solid 0px;padding:10px 60px;text-align: center;color: white; font-size: 2em;font-family: Arial, Helvetica, sans-serif;">Get Started</a>
                    </div>
                </div>
            </body>
            </html>
        """
        part = MIMEText(html, 'html')

        return part

    def delete_account(self,receiver,url):
        html = f"""
            <!DOCTYPE html>
            <html lang="en">
            <body style="background-color: rgb(245, 237, 237);width: 100%;margin: 0;padding: 0;align-items: center;">
                <header style="background-color: rgb(35, 93, 179);;margin: 0;padding: 5px;">
                    <h1 style="text-align: center;color: white;">Steam Analitic</h1>
                </header>
                <div style="text-align: center;">
                    <h3>Hello User you delete user account???</h3>
                </div>
                <div style= "display: flex;justify-content: center;margin-top:50px;">
                    <div style="">
                        <a href="{url}" style="background-color: red; border-radius: 0.75em;border: solid 0px;padding:10px 60px;text-align: center;color: white; font-size: 2em;font-family: Arial, Helvetica, sans-serif;">Get Started</a>
                    </div>
                </div>
            </body>
            </html>
        """
        part = MIMEText(html, 'html')

        return part

    def email_verify(self,receiver,url):
        html = f"""
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
                        <a href="{url}" style="background-color: rgb(35, 93, 179); border-radius: 0.75em;border: solid 0px;padding:10px 60px;text-align: center;color: white; font-size: 2em;font-family: Arial, Helvetica, sans-serif;">Get Started</a>
                    </div>
                </div>
            </body>
            </html>
        """
        part = MIMEText(html, 'html')

        return part
