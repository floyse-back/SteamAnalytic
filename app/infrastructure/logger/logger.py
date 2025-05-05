import logging



class Logger:
    def __init__(self,name=__name__,level=logging.INFO):
        self.logger = logging.getLogger(name)

    def logger_config(self,level):
        logging.basicConfig(level=level,
                            datefmt="%Y:%m:%d %H:%M:%S",
                            format="%(asctime)s - %(module)s:(lineno)%s - %(levelname)s - %(message)s)"
                            )

    async def info(self,msg,args,**kwargs):
        self.logger.info(msg,args **kwargs)

    async def error(self,msg,args,**kwargs):
        self.logger.error(msg,args,**kwargs)

    async def warning(self,msg,args,**kwargs):
        self.logger.warning(msg,args,**kwargs)

    async def critical(self,msg,args,**kwargs):
        self.logger.critical(msg,args,**kwargs)

    async def debug(self,msg,args,**kwargs):
        self.logger.debug(msg,args,**kwargs)

    async def exception(self,msg,args,**kwargs):
        self.logger.exception(msg,args,**kwargs)