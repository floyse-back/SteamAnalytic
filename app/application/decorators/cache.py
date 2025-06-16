import functools

from app.infrastructure.logger.logger import logger
from app.utils.generators import key_generator_args_and_kwargs


def cache_data(expire: int = 3600):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self,*args,**kwargs):
            if not hasattr(self, "cache_repository"):
                raise AttributeError("cache_repository не знайдено в self")

            new_args,new_kwargs = key_generator_args_and_kwargs(args_list=args,kwargs_list=kwargs)
            key = f"{func.__name__}:{new_args}:{new_kwargs}"

            redis_result = self.cache_repository.get_data(key)
            logger.critical("%s",key)
            if redis_result:
                return redis_result

            result = await func(self,*args,**kwargs)

            self.cache_repository.cache_data(key=key,data=result,expire=expire)

            return result
        return wrapper
    return decorator
