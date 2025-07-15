from pydantic import BaseModel

from app.domain.cache_repository import ICacheRepository
from app.domain.logger import ILogger
from app.infrastructure.redis.redis_db import redis_client
import json

class CacheRepository(ICacheRepository):
    def __init__(self,logger:ILogger,client = None):
        self.redis_client = redis_client.client if client is None else client
        self.logger = logger

    def cache_data(self, key: str, data, expire: int = 3600):
        if isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
            serialized_data = [item.model_dump() for item in data]
        elif isinstance(data, BaseModel):
            serialized_data = data.model_dump()
        else:
            serialized_data = data
        self.logger.info(f"key:{key}")
        try:
            self.redis_client.set(key, json.dumps(serialized_data), ex=expire)
        except Exception as e:
            self.logger.error("RedisRepository Error %s",e, exc_info=True)

    def get_data(self,key):
        result = self.redis_client.get(key)

        return json.loads(result) if result else None

    def delete_data(self,key):
        self.redis_client.delete(key)

