import logging

from app.domain.logger import ILogger


class Logger(ILogger):
    def __init__(self,name=__name__,level=logging.INFO):
        self.logger = logging.getLogger(name)
        self.logger_config(level)

    def logger_config(self,level):
        logging.basicConfig(level=level,
                            datefmt="%Y:%m:%d %H:%M:%S",
                            format="%(asctime)s - %(module)s:(%(lineno)d) - %(levelname)s - %(message)s"
                            )

    def info(self,msg,*args):
        self.logger.info(msg,*args)

    def error(self,msg,*args):
        self.logger.error(msg,*args)

    def warning(self,msg,*args):
        self.logger.warning(msg,*args)

    def critical(self,msg,*args):
        self.logger.critical(msg,*args)

    def debug(self,msg,*args):
        self.logger.debug(msg,*args)

    def exception(self,msg,*args):
        self.logger.exception(msg,*args)