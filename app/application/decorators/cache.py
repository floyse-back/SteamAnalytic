import functools


def cache_data(expire: int = 3600):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(self,*args,**kwargs):
            if not hasattr(self, "cache_repository"):
                raise AttributeError("cache_repository не знайдено в self")

            key = f"{func.__name__}:{args}:{kwargs}"

            redis_result = self.cache_repository.get_data(key)
            if redis_result:
                return redis_result

            result = await func(self,*args,**kwargs)

            self.cache_repository.cache_data(key,result,expire)

            return result
        return wrapper
    return decorator
