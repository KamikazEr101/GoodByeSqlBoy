import redis
from functools import lru_cache
from config import settings

host = settings.REDIS_HOST
port = settings.REDIS_PORT

pool = redis.ConnectionPool(host=host, port=port, db=0, decode_responses=True)

@lru_cache
def get_redis_template():
    return redis.Redis(connection_pool=pool)

