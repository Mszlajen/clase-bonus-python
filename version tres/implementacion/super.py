from functools import partial
from inspect import ismethod
from typing import Any


class Super:
    def __init__[T](self, cur_type: type[T], obj: T):
        if not isinstance(obj, cur_type):
            raise ValueError(f"obj is not of type {cur_type}")
        self.base_type = cur_type.mro()[1]
        self.obj = obj
    
    def __getattribute__(self, name: str) -> Any:
        if name in ('base_type', 'obj'):
            return object.__getattribute__(self, name)
        else:
            attr = getattr(self.base_type, name)
            if ismethod(attr):
                return partial(attr, self.obj)
            else:
                return attr