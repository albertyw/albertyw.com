# Various utility functions
import os


SHOULD_CACHE = os.environ['ENV'] == 'production'


def cached_function(func):
    data = {}

    def wrapper(*args):
        if not SHOULD_CACHE:
            return func(*args)
        cache_key = ' '.join([str(x) for x in args])
        if cache_key not in data:
            data[cache_key] = func(*args)
        return data[cache_key]

    return wrapper
