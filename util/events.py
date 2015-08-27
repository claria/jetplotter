class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class EventHandler(object):
    """ Very simple callback system."""
    __metaclass__ = Singleton

    def __init__(self):
        self._callbacks = {}

    def add(self, callback, func):
        if not callable(func):
            raise TypeError('The Callback function is not callable.')
        self._callbacks.setdefault(callback, []).append(func)

    def remove(self, callback, func):
        self._callbacks[callback].remove(func)

    def trigger(self, callback, *args, **kwargs):

        for func in self._callbacks.setdefault(callback, []):
            func(*args, **kwargs)

