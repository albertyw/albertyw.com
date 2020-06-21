# Various utility functions
import os

from typing import Any, Callable


SHOULD_CACHE = os.environ.get('ENV', 'development') == 'production'


def cached_function(func: Callable[..., Any]) -> Callable[..., Any]:
    data = {}

    def wrapper(*args: Any) -> Any:
        if not SHOULD_CACHE:
            return func(*args)
        cache_key = ' '.join([str(x) for x in args])
        if cache_key not in data:
            data[cache_key] = func(*args)
        return data[cache_key]

    wrapper.__qualname__ = func.__qualname__
    return wrapper
