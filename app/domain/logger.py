from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def trace(self, msg:str,*args, **kwargs):
        pass

    @abstractmethod
    def debug(self,msg:str, *args, **kwargs):
        pass

    @abstractmethod
    def info(self,msg:str,*args, **kwargs):
        pass

    @abstractmethod
    def warning(self,msg:str,*args, **kwargs):
        pass

    @abstractmethod
    def error(self,msg:str,*args, **kwargs):
        pass

    @abstractmethod
    def critical(self,msg:str,*args, **kwargs):
        pass