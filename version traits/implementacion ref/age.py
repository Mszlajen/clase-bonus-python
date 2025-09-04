from trait import *


class Atacante(Trait):
    vida = 100

    def atacar(self): ...

    def descansar(self): ...

class Defensor(Trait):
    def descansar(self): ...

    def recibir_danio(self, danio): ...


@implements(Atacante & Defensor - "descansar")
class Guerrero():
    ...