from trait import *


class RPGCharacter(Trait):    
    level: int

    @keep_recursion
    def required_exp(self, start_level = None):
        if not start_level: start_level = self.level
        if start_level == 1: return 10
        return 2 * self.required_exp(start_level - 1)


@implements(RPGCharacter << ("required_exp", "basic_calculation"))
class Pokemon:
    def __init__(self, level = 10):
        self.level = level

    def required_exp_v1(self):
        return self.basic_calculation() * 10
    
    def required_exp_v2(self):
        return RPGCharacter.required_exp(self) * 10

print(Pokemon(1).required_exp_v1())
print(Pokemon(1).required_exp_v2())