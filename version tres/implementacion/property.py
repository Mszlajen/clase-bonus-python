from typing import Callable


class Property[T, R]:
    def __init__(self, getter: Callable[[T], R], setter: Callable[[T, R], None] | None = None):
        self._getter = getter
        self._setter = setter
    
    def __set_name__(self, owner: type[T], name: str):
        self.owner = owner
        self.name = name
    
    def __get__(self, obj: T, objtype: type[T]):
        if obj is None:
            return self._getter
        else:
            return self._getter(obj)
    
    def setter(self, f: Callable[[T, R], None]):
        self._setter = f
    
    def __set__(self, obj: T, value: R):
        if self._setter is None:
            setattr(obj, self.name, value)
        else:
            self._setter(obj, value)