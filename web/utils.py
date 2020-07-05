# coding: utf-8

from threading import local as threadlocal
from .py3helpers import (
    iteritems,
    itervalues,
    iterkeys
)


class Storage(dict):
    """
    A Storage object is like a dictionary except `obj.foo` can be used
    in addition to `obj['foo']`.
        >>> o = storage(a=1)
        >>> o.a
        1
        >>> o['a']
        1
        >>> o.a = 2
        >>> o['a']
        2
        >>> del o.a
        >>> o.a
        Traceback (most recent call last):
            ...
        AttributeError: 'a'
    """

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError as k:
            raise AttributeError(k)

    def __repr__(self):
        return "<Storage " + dict.__repr__(self) + ">"


storage = Storage


def group(seq, size):
    """
    Returns an iterator over a series of lists of length size from iterable.

        >>> list(group([1,2,3,4], 2))
        [[1, 2], [3, 4]]
        >>> list(group([1,2,3,4,5], 2))
        [[1, 2], [3, 4], [5]]
    """
    return (seq[i: i+size] for i in range(0, len(seq), size))


class ThreadedDict(threadlocal):
    """
    Thread local storage.

        >>> d = ThreadedDict()
        >>> d.x = 1
        >>> d.x
        1
        >>> import threading
        >>> def f(): d.x = 2
        ...
        >>> t = threading.Thread(target=f)
        >>> t.start()
        >>> t.join()
        >>> d.x
    """
    _instances = set()

    def __init__(self):
        ThreadedDict._instances.add(self)

    def __del__(self):
        ThreadedDict._instances.remove(self)

    def __hash__(self):
        return id(self)

    def clear_all():
        for t in list(ThreadedDict._instances):
            t.clear()

    clear_all = staticmethod(clear_all)

    def __getitem__(self, key):
        return self.__dict__[key]

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __delitem__(self, key):
        del self.__dict__[key]

    def __contains__(self, key):
        return key in self.__dict__

    has_key = __contains__

    def clear(self):
        self.__dict__.clear()

    def copy(self):
        return self.__dict__.copy()

    def get(self, key, default=None):
        return self.__dict__.get(key, default)

    def items(self):
        return self.__dict__.items()

    def iteritems(self):
        return iteritems(self.__dict__)

    def keys(self):
        return self.__dict__.keys()

    def iterkeys(self):
        try:
            return iterkeys(self.__dict__)
        except NameError:
            return self.__dict__.keys()

    iter = iterkeys

    def values(self):
        return self.__dict__.values()

    def itervalues(self):
        return itervalues(self.__dict__)

    def pop(self, key, *args):
        return self.__dict__.pop(key, *args)

    def popitem(self):
        return self.__dict__.popitem()

    def setdefault(self, key, default=None):
        return self.__dict__.setdefault(key, default)

    def update(self, *args, **kwargs):
        self.__dict__.update(*args, **kwargs)

    def __repr__(self):
        return "<ThreadedDict %r>" % self.__dict__

    __str__ = __repr__

threadeddict = ThreadedDict