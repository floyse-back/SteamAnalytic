from redis import Redis


class RedisDB:
    def __init__(self,host='localhost',port=6379,db=0):
        self._client = Redis(host=host,
                             port=port,
                             db=db,
                             decode_responses=True
                             )

    @property
    def client(self):
        return self._client

redis_client = RedisDB()