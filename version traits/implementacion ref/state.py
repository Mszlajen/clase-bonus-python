from trait import Trait, implements, CleanState

class Defensor(Trait):
    energia = CleanState(int)

@implements(Defensor)
class Guerrero:
    def __init__(self, vida):
        self.energia = vida


atila = Guerrero(100)
print(atila.energia)