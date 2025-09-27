from trait import *


class Atacante(Trait):
    vida = 100

    def atacar(self): ...

    def descansar(self): ...

class Defensor(Trait):
    def descansar(self): ...

    def recibir_danio(self, danio): ...

GuerreroTrait = Atacante & Defensor - "descansar"

@implements(GuerreroTrait)
class Guerrero():
    ...
    
Guerrero().atacar()