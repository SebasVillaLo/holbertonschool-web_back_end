#!/usr/bin/env python3
"""Writing strings to Redis """

import redis
from typing import Union, Callable
from uuid import uuid4
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Incrementing values """
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Incrementing values"""
        self._redis.incr(key)
        return method(self, *args, **kwds)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Storing lists """
    inp = method.__qualname__ + ':inputs'
    out = method.__qualname__ + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwds):
        """Storing lists"""
        self._redis.rpush(inp, str(args))
        rtn_method = method(self, *args, **kwds)
        return self._redis.rpush(out, str(rtn_method))
    return wrapper


class Cache():
    """Writing strings to Redis """

    def __init__(self) -> None:
        """init method"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """generate a random key"""
        key = str(uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None) -> Union[
            str, bytes, int, float]:
        """convert the data back to the desired format"""
        if fn:
            return fn(self._redis.get(key))
        return self._redis.get(key)

    def get_str(self, data: str) -> str:
        """ parametrize Cache.get with
        the correct conversion function"""
        return str(data.encode('utf-8'))

    def get_int(self, number: str) -> int:
        """ parametrize Cache.get with
        the correct conversion function"""
        return int(number)
