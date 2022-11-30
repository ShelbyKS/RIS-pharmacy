from functools import wraps
from cache.connection import RedisCache


def fetch_from_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) #Подсключились к Редис
    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            cached_value = cache_conn.get_value(cache_name)#Извлекаем из кэша
            print('cached_value=', cached_value)
            if cached_value:
                return cached_value #Возвращаем извлеченное из кэша
            response = f(*args, **kwargs) #Если в кэше ничего нет, запускаем селект из БД
            print('response=', response)
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response #Возвращаем р-т из БД
        return wrapper
    return wrapper_func


def update_cache(cache_name: str, cache_config: dict):
    cache_conn = RedisCache(cache_config['redis']) #Подсключились к Редис
    ttl = cache_config['ttl']

    def wrapper_func(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs) #Если в кэше ничего нет, запускаем селект из БД
            print('response=', response)
            cache_conn.set_value(cache_name, response, ttl=ttl)
            return response #Возвращаем р-т из БД
        return wrapper
    return wrapper_func


