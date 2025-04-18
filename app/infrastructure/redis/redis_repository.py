import functools

from app.infrastructure.redis.redis_db import redis_client
import json

class RedisRepository:
    REDIS_CLIENT = redis_client.client


    @classmethod
    def cache_data(cls, key: str, data, expire: int = 3600):
        cls.REDIS_CLIENT.set(key, json.dumps(data), ex=expire)

    @classmethod
    def get_data(cls,key):
        result = cls.REDIS_CLIENT.get(key)

        return json.loads(result) if result else None

    @classmethod
    def delete_data(cls,key):
        cls.REDIS_CLIENT.delete(key)

def redis_cache(expire: int = 3600):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args,**kwargs):
            key = f"{func.__name__}:{args}:{kwargs}"

            redis_result = RedisRepository.get_data(key)
            if redis_result:
                return redis_result

            result = await func(*args,**kwargs)

            RedisRepository.cache_data(key,result,expire)

            return result
        return wrapper
    return decorator