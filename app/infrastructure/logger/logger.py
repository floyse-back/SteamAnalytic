from app.domain.logger import ILogger
from app.infrastructure.logger.logger_conf import get_logger


class Logger(ILogger):
    def __init__(self,name,file_path:str=None)->None:
        self.__logger = get_logger(name,file_path)

    def trace(self, msg :str ,*args, **kwargs):
        self.__logger.debug(msg,*args, **kwargs)

    def debug(self ,msg :str, *args, **kwargs):
        self.__logger.debug(msg,*args, **kwargs)

    def info(self ,msg :str ,*args, **kwargs):
        self.__logger.info(msg,*args, **kwargs)

    def warning(self ,msg :str ,*args, **kwargs):
        self.__logger.warning(msg,*args, **kwargs)

    def error(self ,msg :str ,*args, **kwargs):
        self.__logger.error(msg,*args, **kwargs)

    def critical(self ,msg :str ,*args, **kwargs):
        self.__logger.critical(msg,*args, **kwargs)