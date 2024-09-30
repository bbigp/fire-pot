from cachetools import TTLCache

channel_cache = TTLCache(maxsize=100, ttl=60*10)


item_cache = TTLCache(maxsize=100, ttl=60*60*24*5)

def put_cahce(key: str, value: str, cache: TTLCache=channel_cache):
    cache[key] = value

def get_cahce(key: str, cache:TTLCache=channel_cache):
    return cache.get(key)

def exists_cahce(key: str, cache:TTLCache=channel_cache):
    return key in cache