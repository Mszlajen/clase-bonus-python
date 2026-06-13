from functools import wraps, partial
from typing import Callable

def validar(*types: type):
    def decorator(f: Callable):
        def inner(self, *args):
            if any(isinstance(arg, type) for type, arg in zip(types, args)):
                raise TypeError()
        return inner
    return decorator

class Validar:
    def __init__(self, *types: type):
        self.types = types
    
    def __call__(self, f: Callable):
        return partial(self._validate, f)
    
    def _validate(self, f, *args):
        if any(isinstance(arg, type) for type, arg in zip(self.types, args)):
            raise TypeError()
        return f(*args)