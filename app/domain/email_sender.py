from abc import ABC,abstractmethod


class IEmailSender(ABC):

    @abstractmethod
    def send_email(self,email:str,url,type):
        pass

    @abstractmethod
    def forgot_password(self,receiver,url):
        pass

    @abstractmethod
    def delete_account(self,receiver,url):
        pass

    @abstractmethod
    def email_verify(self,receiver,url):
        pass