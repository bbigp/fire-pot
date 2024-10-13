from cachetools import TTLCache
import redis

redis_client = redis.Redis(host='118.31.9.234', port=63796, db=0, password='123456')

def put_cache(key, value, ttl):
    redis_client.set(key, value, ex=ttl)

def get_cache(key):
    return redis_client.get(key)

def exists_cache(key):
    return redis_client.exists(key)

# channel_cache = TTLCache(maxsize=100, ttl=60*10)
# item_cache = TTLCache(maxsize=100, ttl=60*60*24*5)
#
# def put_cahce(key: str, value: str, cache: TTLCache=channel_cache):
#     cache[key] = value
#
# def get_cahce(key: str, cache:TTLCache=channel_cache):
#     return cache.get(key)
#
# def exists_cahce(key: str, cache:TTLCache=channel_cache):
#     return key in cache