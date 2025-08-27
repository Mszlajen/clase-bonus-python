from trait import *


class RPGCharacter(Trait):    
    exp: int

    @keep_recursion
    def level(self, finish=False):
        if finish: return 1

        return self.level(True)


@implements(RPGCharacter << ("level", "basic_level"))
class Pokemon:
    def __init__(self, exp = 100):
        self.exp = exp

    def level_v1(self):
        return self.basic_level() * 10
    
    def level_v2(self):
        return RPGCharacter.level(self) * 10

print(Pokemon().level_v1())
print(Pokemon().level_v2())