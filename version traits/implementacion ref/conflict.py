class ConflictResolution:
    def __init__(self, attr):
        self.attr = attr

    def resolve(self): ...

class ListAll(ConflictResolution):
    def resolve(self):
        return 

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
