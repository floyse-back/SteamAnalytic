from redis import Redis

from app.utils.config import REDIS_HOST


class RedisDB:
    def __init__(self,host=f'{REDIS_HOST}',port=6379,db=0):
        self._client = Redis(host=host,
                             port=port,
                             db=db,
                             decode_responses=True
                             )

    @property
    def client(self):
        return self._client

redis_client = RedisDB()