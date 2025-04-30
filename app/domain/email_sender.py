from abc import ABC,abstractmethod


class IEmailSender(ABC):

    @abstractmethod
    def send_email(self,email:str,message:str):
        pass

    @abstractmethod
    def forgout_password(self):
        pass

    @abstractmethod
    def delete_account(self):
        pass

    @abstractmethod
    def authenticate(self):
        pass