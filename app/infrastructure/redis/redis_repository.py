from pydantic import BaseModel

from app.domain.cache_repository import ICacheRepository
from app.infrastructure.logger.logger import logger
from app.infrastructure.redis.redis_db import redis_client
import json

class RedisRepository(ICacheRepository):

    def __init__(self,client = None):
        self.redis_client = redis_client.client if client is None else client

    def cache_data(self, key: str, data, expire: int = 3600):
        if isinstance(data, list) and all(isinstance(item, BaseModel) for item in data):
            serialized_data = [item.model_dump() for item in data]
        elif isinstance(data, BaseModel):
            serialized_data = data.model_dump()
        else:
            serialized_data = data
        logger.critical(f"key:{key}")
        self.redis_client.set(key, json.dumps(serialized_data), ex=expire)

    def get_data(self,key):
        result = self.redis_client.get(key)

        return json.loads(result) if result else None

    def delete_data(self,key):
        self.redis_client.delete(key)

