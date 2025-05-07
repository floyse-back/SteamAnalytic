from abc import ABC, abstractmethod

class ILogger(ABC):
    @abstractmethod
    def logger_config(self,level):
        pass

    @abstractmethod
    def info(self,msg,*args,**kwargs):
        pass

    @abstractmethod
    def error(self,msg,*args,**kwargs):
        pass

    @abstractmethod
    def warning(self,msg,*args,**kwargs):
        pass

    @abstractmethod
    def critical(self,msg,*args,**kwargs):
        pass

    @abstractmethod
    def debug(self,msg,*args,**kwargs):
        pass

    @abstractmethod
    def exception(self,msg,*args,**kwargs):
        pass

