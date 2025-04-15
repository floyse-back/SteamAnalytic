import hashlib

from app.infrastructure.redis.redis_db import redis_client
import json

class RedisRepository:
    def __init__(self,client = None):
        self.redis_client = client or redis_client.client

    def cache_data(self, key: str, data, expire: int = 3600):
        if isinstance(data, list):
            data = [item.dict() for item in data]
        else:
            data = data.dict()

        self.redis_client.set(key, json.dumps(data), ex=expire)

    def get_data(self,key):
        result = self.redis_client.get(key)

        return json.loads(result) if result else None

    def delete_data(self,key):
        self.redis_client.delete(key)