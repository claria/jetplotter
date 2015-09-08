
_callbacks = {}

def add(callback, func):
    if not callable(func):
        raise TypeError('The Callback function is not callable.')
    _callbacks.setdefault(callback, []).append(func)

def register(callback):
    def func_wrapper(func):
        _callbacks.setdefault(callback, []).append(func)
        return func
    return func_wrapper

def remove(callback, func):
    _callbacks[callback].remove(func)

def trigger(callback, *args, **kwargs):

    for func in _callbacks.setdefault(callback, []):
        func(*args, **kwargs)
