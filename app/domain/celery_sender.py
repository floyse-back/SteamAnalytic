from abc import ABC, abstractmethod


class ICelerySender(ABC):

    @abstractmethod
    async def send_email(self,receiver,token,type):
        pass
