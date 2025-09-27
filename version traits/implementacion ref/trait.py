from types import MethodType
from typing import Any, Callable
from inspect import getmembers

def implements(trait):
    if not isinstance(trait, TraitMeta):
        raise TypeError("Expected a Trait")

    def decorator[T: type](cls: T) -> T:
        for key, value in getmembers(trait):
            if not hasattr(cls, key):
                if isinstance(value, Conflict):
                    raise NotImplementedError("Method is conflicting between traits")
                setattr(cls, key, value)
        return cls
    return decorator

class Proxy:
    def __init__(self, obj, attr, func) -> None:
        self.obj = obj
        self.attr = attr
        self.func = MethodType(func, self)

    def __getattribute__(self, name: str) -> Any:
        if name == super().__getattribute__('attr'):
            return super().__getattribute__('func')
        else:
            return getattr(super().__getattribute__('obj'), name)

class FrozenRecursion:
    def __init__(self, func):
        self.func = func
    
    def __set_name__(self, owner, attr):
        self.owner = owner
        self.attr = attr

    def __get__(self, obj = None, cls = None):
        if obj is None:
            return self
        else:
            return MethodType(self.func, Proxy(obj, self.attr, self.func))
    
    def __call__(self, obj, *args, **kwargs):
        return self.func(Proxy(obj, self.attr, self.func), *args, **kwargs)

def keep_recursion(func: Callable) -> Callable:
    return FrozenRecursion(func)

class Conflict:
    def __init__(self, *methods):
        self.methods = []
        for method in methods:
            if isinstance(method, Conflict):
                self.methods.extend(method.methods)
            elif callable(method):
                self.methods.append(method)
            else:
                raise TypeError()

class TraitMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any):
        return super().__new__(cls, name, bases, dict | {'__new__': cls.__instance_new__}, **kwds)
    
    def __instance_new__(cls, *args, **kwargs):
        raise NotImplementedError("Traits shouldn't be instanced")

    def __and__(self, other) -> 'TraitMeta':
        if isinstance(other, TraitMeta):
            conflicts = {attr: Conflict(getattr(self, attr), getattr(other, attr)) for attr in self.__dict__.keys() if attr in other.__dict__.keys()}
            return TraitMeta(f"{self.__name__} + {other.__name__}", (type,), {**self.__dict__, **other.__dict__, **conflicts})
        else:
            return NotImplemented

    def __sub__(self, other) -> 'TraitMeta':
        if isinstance(other, str):
            new_dict = self.__dict__.copy()
            new_dict.pop(other, None)
            return TraitMeta(self.__qualname__, (type,), new_dict)
        else:
            return NotImplemented
    
    def __lshift__(self, other) -> 'TraitMeta':
        try:
            old, new = other
        except TypeError:
            return NotImplemented
        new_trait = TraitMeta(self.__qualname__, (type, ), self.__dict__.copy())
        setattr(new_trait, new, getattr(self, old))
        delattr(new_trait, old)
        return new_trait
            

class Trait(metaclass=TraitMeta):
    # Mostrar primero implementación del algebra usando @classmethod y explicar por qué no funciona
    ...




# Implementación alternativa con hooks
class Impl:
    def __init_subclass__(cls, trait, **kwargs) -> None:
        implements(trait)(cls)
        super().__init_subclass__(**kwargs)