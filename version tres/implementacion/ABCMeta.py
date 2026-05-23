from inspect import getmembers_static
from typing import Any, Iterable, overload

def abstractmethod(f):
    f.__abstract__ = True
    return f

class ABCMeta(type):
    def __call__(self: 'ABCMeta', name: str, superclasses: Iterable[type], body: dict[str, Any], **kwargs: Any):
        abstract_methods = getmembers_static(self, lambda attr_value: getattr(attr_value, '__abstract__', False))
        if abstract_methods:
            raise NotImplementedError("Abstract classes shouldn't be instanciated")
        return super().__call__(name, superclasses, body, **kwargs)