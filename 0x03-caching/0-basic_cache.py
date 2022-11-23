#!/usr/bin/python3
"""  Basic dictionary """
from base_caching import BaseCaching


class BasicCache(BaseCaching):
    """ Class that inherits from BaseCaching and is a caching system
        This caching system doesn’t have limit """
    def put(self, key, item):
        """ Assign to the dictionary """
        if key and item:
            self.cache_data[key] = item

    def get(self, key):
        """ Return the value linked """
        if key is not None or self.cache_data.get(key) is not None:
            return self.cache_data.get(key)
        else:
            return None
