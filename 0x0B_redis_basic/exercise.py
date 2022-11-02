#!/usr/bin/env python3
""" Writing strings to Redis, Reading from Redis and recovering original type,
    Incrementing values, Storing lists, Retrieving lists """

import redis
import uuid
from typing import Union, Callable, Optional, Any, List
from functools import wraps

r = redis.Redis()

def count_calls(method: Callable) -> Callable:
    """ Counts how many times methods of the Cache class are called. """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function """
        self._redis.incr(method.__qualname__)
        return method(self, *args, **kwds)
    return wrapper

def call_history(method: Callable) -> Callable:
    """ Stores the history of inputs and outputs for a particular function. """
    @wraps(method)
    def wrapper(self, *args, **kwds):
        """ Wrapper function """
        self._redis.rpush(method.__qualname__ + ":inputs", str(args))
        output = method(self, *args, **kwds)
        self._redis.rpush(method.__qualname__ + ":outputs", str(output))
        return output
    return wrapper

def replay(method: Callable):
    """ Display the history of calls of a particular function. """
    r = redis.Redis()
    method_name = method.__qualname__
    inputs = r.lrange(method_name + ":inputs", 0, -1)
    outputs = r.lrange(method_name + ":outputs", 0, -1)
    print("{} was called {} times:".format(method_name, r.get(method_name).decode("utf-8")))
    for i, j in zip(inputs, outputs):
        print("{}(*{}) -> {}".format(method_name, i.decode("utf-8"), j.decode("utf-8")))
    print()

class Cache:
    """ Cache class """
    def __init__(self):
        """ Constructor """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """ Generate a random key, store the input data in Redis using the
            random key and return the key. """
        key = str(uuid.uuid4())
        self._redis.mset({key: data})
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Any:
        """ Take a key string and an optional conversion function
            as arguments. Return the data stored in Redis as a string
            or converted by the conversion function. """
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    @count_calls
    @call_history
    def get_str(self, key: str) -> str:
        """ Take a key string, and return the string stored in Redis
            as a decoded string. """
        data = self._redis.get(key)
        return data.decode("utf-8")

    @count_calls
    @call_history
    def get_int(self, key: str) -> int:
        """ Take a key string, and return the string stored in Redis
            as a converted integer. """
        data = self._redis.get(key)
        return int(data)
