import logging

from app.domain.logger import ILogger


class Logger(ILogger):
    def __init__(self,name=__name__,level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger_config(level)

    def logger_config(self,level):
        logging.basicConfig(level=level,
                            datefmt="%Y:%m:%d %H:%M:%S",
                            format="%(asctime)s - %(module)s:(lineno)%d  - %(levelname)s - %(message)s)"
                            )

    def info(self,msg,*args,**kwargs):
        self.logger.info(msg,*args, **kwargs)

    def error(self,msg,*args,**kwargs):
        self.logger.error(msg,*args,**kwargs)

    def warning(self,msg,*args,**kwargs):
        self.logger.warning(msg,*args,**kwargs)

    def critical(self,msg,*args,**kwargs):
        self.logger.critical(msg,*args,**kwargs)

    def debug(self,msg,*args,**kwargs):
        self.logger.debug(msg,*args,**kwargs)

    def exception(self,msg,*args,**kwargs):
        self.logger.exception(msg,*args,**kwargs)