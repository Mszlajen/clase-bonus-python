from types import MethodType

class classmethod:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, obj = None, cls = None):
        return MethodType(self.func, cls)