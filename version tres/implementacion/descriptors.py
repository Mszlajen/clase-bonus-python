from functools import partial
from typing import Callable, Concatenate


class ClassMethod[T, R]:
    def __init__(self, f: Callable[Concatenate[type[T], ...], R]):
        self.f = f
    
    def __get__(self, obj: T, objtype: type[T]):
        if obj is None:
            return self.f
        else:
            return partial(self.f, objtype)

class StaticMethod[R]:
    def __init__(self, f: Callable[..., R]):
        self.f = f
    
    def __get__(self, obj, objtype):
        return self.f

class CachedProperty[T, R]:
    def __init__(self, f: Callable[[T], R]):
        self.f = f

    def __set_name__(self, owner: type[T], name: str):
        self.owner = owner
        self.name = name

    def __get__(self, obj: T, objtype: type[T]):
        if obj is not None:
            res = self.f(obj)
            setattr(obj, self.name, res)
            return res
        else:
            return self.f