---
marp: true
---

# Metaprogramación en Python

## Implementando Traits

---

## ¿Qué es un objeto?

```python
class C:
    def m(self):
        ...

c = C()
```
<!--
Hablar de los objectos como diccionarios y metodos como funciones vinculadas.
Mostrar metamodelo.
-->

---

## Sintaxis (P1)

```python
class Atacante(Trait):
    def atacar(self): ...

    def descansar(self): ...

class Defensor(Trait):
    def descansar(self): ...

    def recibir_danio(self, danio): ...

GuerreroTrait = Atacante & Defensor - "descansar"
```

<!--
Plantear que dada la sintaxis deseada se necesita una clase Trait y luego explicar como python maneja los operadores (aka. metodos magicos).
Una vez hecho eso, notar que la implementación aplica sobre las instancias, mostrar @classmethod y porque en este caso no sirve y luego introducir metaclass
-->

---

## Sintaxis (P2)

```python
GuerreroTrait = Atacante & Defensor - "descansar"

@implements(GuerreroTrait)
class Guerrero:
    ...
```

<!--
Profundizar más en decorators e introducir el monkey patching en python.
-->

---

## Recursividad (P1)

```python
class RPGCharacter(Trait):    
    level: int

    def required_exp(self):
        ...

@implements(RPGCharacter << ("required_exp", "basic_calculation"))
class Pokemon:
    def __init__(self, level = 10):
        self.level = level

    def required_exp(self):
        return self.basic_calculation() * 10
    
    def required_exp_v2(self):
        return RPGCharacter.required_exp(self) * 10
```

<!--
Explicar como el alias method es redundante en python porque puedo referenciar la funcion original a traves del Trait directamente pero lo vamos a hacer para demostrar que lo siguiente doble funciona.
-->

---

## Recursividad (P2)

```python
class RPGCharacter(Trait):
    level: int

    def required_exp(self, start_level = None):
        if not start_level: start_level = self.level
        if start_level == 1: return 10
        return 2 * self.required_exp(start_level - 1)
```

---

## Recursividad (P3)

```python
class RPGCharacter(Trait):    
    level: int

    @keep_recursion
    def required_exp(self, start_level = None):
        if not start_level: start_level = self.level
        if start_level == 1: return 10
        return 2 * self.required_exp(start_level - 1)
```

<!--
Definir keep_recursion -> Definir FrozenRecursion -> Explicar descriptors -> Separar comportamiento entre clase e instancia -> Introducir clase MethodType ->
Introducir Proxy -> Mostrar __getattribute__
-->

---

## ¿Estado?

<!-- Hablar de como el estado se resuelve automaticamente porque todo se maneja con atributos -->

---

## Implementación alternativa

```python
class Guerrero(Impl, trait=GuerreroTrait):
    ...
```

<!-- Comparar Metaclass.__new__vs Type.__init_subclass__ -->

---

## Chequeo de Tipos

<!-- -->