from typing import Callable, Concatenate, Any
from inspect import getmembers_static, ismethod
from functools import partial


class ClassMethod:
    def __init__[R](self, f: Callable[Concatenate[type, ...], R]):
        self.f = f
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self.f
        else:
            return partial(self.f, objtype)

class StaticMethod:
    def __init__[R](self, f: Callable[Concatenate[type, ...], R]):
        self.f = f
    
    def __get__(self, obj, objtype):
        return self.f


class Property[T]:
    def __init__[R](self, f: Callable[[T], R]):
        self.f = f
    
    def __set_name__(self, owner: type[T], name: str):
        self.owner = owner
        self.name = name
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self.f
        else:
            return self.f(obj)

# Mostrarlo y reiterar la comparación entre non-data descriptor y data descriptors
class CachedProperty(Property):
    def __get__(self, obj, objtype):
        res = super().__get__(obj, objtype)
        if obj is not None:
            setattr(obj, self.name, res)
        return res


class FullProperty[T]:
    def __init__[R, V](self, getter: Callable[[T], R], setter: Callable[[T, V], None] | None = None):
        self._getter = getter
        self._setter = setter
    
    def __set_name__(self, owner: type[T], name: str):
        self.owner = owner
        self.name = name
    
    def __get__(self, obj, objtype):
        if obj is None:
            return self._getter
        else:
            return self._getter(obj)
    
    def setter[V](self, f: Callable[[T, V], None]):
        self._setter = f
    
    def __set__(self, obj, value):
        if self._setter is None:
            setattr(obj, self.name, value)
        else:
            self._setter(obj, value)


# Recordar explicar la trampa del compilador
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


class AbstractMethod: 
    def __init__(self, f: 'function') -> None:
        self.f = f
    
    def __get__(self, obj, objtype):
        return self.f

class ABCMeta(type):
    def __call__(self: 'ABCMeta', *args, **kwargs):
        abstract_methods = getmembers_static(self, lambda attr_value: isinstance(attr_value, AbstractMethod))
        if abstract_methods:
            raise NotImplementedError("Abstract classes shouldn't be instanciated")
        super().__call__(*args, **kwargs)