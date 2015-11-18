# -*- coding: utf8 -*-
'''
Utility functions for smallshapes package
'''

class lazy(object):

    '''Lazy accessor .'''

    def __init__(self, func):
        self.func = func

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        value = self.func(obj)
        setattr(obj, self.func.__name__, value)
        return value
