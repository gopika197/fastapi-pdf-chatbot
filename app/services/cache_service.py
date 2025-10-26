import time
from cachetools import TTLCache

cache = TTLCache(maxsize=1024, ttl=300)

def cache_get_or_set(key, compute_fn, ttl_seconds=300):
    try:
        if key in cache:
            return cache[key]
        val = compute_fn()
        cache[key] = val
        return val
    except Exception:
        return compute_fn()
