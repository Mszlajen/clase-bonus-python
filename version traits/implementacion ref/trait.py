from typing import Any
from inspect import getmembers


def implements(trait):
    if not isinstance(trait, TraitMeta):
        raise TypeError("Expected a Trait")
    def decorator(cls):
        for key, value in getmembers(trait):
            if not hasattr(cls, key):
                setattr(cls, key, value)
        return cls
    return decorator

class TraitMeta(type):
    def __new__(cls, name: str, bases: tuple[type, ...], dict: dict[str, Any], /, **kwds: Any):
        return super().__new__(cls, name, bases, dict | {'__new__': cls.__instance_new__}, **kwds)
    
    def __instance_new__(cls, *args, **kwargs):
        raise NotImplementedError("Traits shouldn't be instanced")

    def __add__(self, other):
        if isinstance(other, TraitMeta):
            return TraitMeta(f"{self.__name__} + {other.__name__}", (type,), {**self.__dict__, **other.__dict__})
        else:
            return NotImplemented
    
    def __lshift__(self, other):
        if isinstance(other, str):
            new_dict = self.__dict__.copy()
            new_dict.pop(other, None)
            return TraitMeta(self.__qualname__, (type,), new_dict)
        else:
            return NotImplemented

class Trait(metaclass=TraitMeta):
    # Mostrar primero implementación del algebra usando @classmethod y explicar por qué no funciona
    ...