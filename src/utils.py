import time

_cache = {}

def get_cache(key: str):
    item = _cache.get(key)
    if not item:
        return None

    data, expires_at = item
    if time.time() > expires_at:
        del _cache[key]
        return None

    return data


def set_cache(key: str, value, ttl: int = 300):
    expires_at = time.time() + ttl
    _cache[key] = (value, expires_at)
