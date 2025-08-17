# Intervenir en method lookup

## ¿Qué es un objeto?

Para darle una definición simple y generica podriamos decir que un objeto es algo que puede tener atributos y recibir mensajes.  
En ruby un objeto es una construcción en la que se basa el lenguaje para construir el resto de su metamodelo \(salvo un par de excepciones\) y los atributos y metodos son dos construcciones separadas una de la otra.   
Pero eso no es necesariamente una obligación.  
[Ver codigo](<1a - Qué es un objeto.ipynb>)  
Definimos una clase y dos instancias, les podemos pedir sus atributos y llamar sus metodos.  
Pero, ¿qué es un metodo? Una función asignada a un atributo de la clase.
¿Qué pasa ahora si quiero modificar en runtime un objeto?  
[Ver codigo](<1b - Qué es un objeto.ipynb>)  
Y volvemos a la pregunta original, ¿qué es un objeto \(en python\)?  
[Ver codigo](<1c - Qué es un objeto.ipynb>)  
La respuesta simple es un diccionario. Entonces, ¿si quiere hacer reflection uso ese diccionario? NO.
Como vimos en el ejemplo, el diccionario solo incluye los atributos definidos directamente en el objeto y python tiene una opción para optimizar objetos que no vamos a querer modificar dinamicamente que saltea la creación del diccionario con lo cual en una aplicación tendriamos un manejo más complejo.  

## Intervenir el lookup

[Ver codigo](<2a - Intervenir el lookup.ipynb>)  
Vamos plantear un problema. Tenemos un framework que tiene una clase usuario y en ciertos contextos queremos tratar un usuario como anonimo que modifica algunos de sus comportamientos.  
[Ver codigo](<2b - Intervenir el lookup.ipynb>)  
En la primera opción tenemos lo mismo que Ruby. Python nos ofrece un hook que podemos definir para ejecutar cuando un atributo no existe.  
Sin embargo esto tiene dos problemas, uno solucionable y otro no.  
El solucionable es que si el objeto decorado se envia un mensaje a si mismo no va pasar por nuestro decorator.  
El no solucionable es que los atributos heredados de object siguen tomando prioridad sobre los de usuario.  
[Ver codigo](<2c - Intervenir el lookup.ipynb>)  
Para solucionar el segundo problema Python nos ofrece otro hook \(y un punto donde tira su forma de nombrar a la mierda\).  

## Decorators

Supongamos que tenemos una secuencia de metodos donde varios de ellos repiten el inicio y final, ¿cómo podemos reducir la repetición de codigo usando objetos tradicional? Una opción seria usar orden superior.  
[Ver codigo](<3a - Decorators.ipynb>)  
Pero en python los metodos no son más que atributos en la clase con lo cual lo podemos pisar el contenido del atributo con una version decorada del metodo.
y como esto es un patron lo suficientemente comun, python nos da una sintaxis especial para realizarlo.  
[Ver codigo](<3b - Decorators.ipynb>)  
Pero acá hay una trampa, algo que funcionaba antes ahora no funciona.  
m3 imprime el texto equivocado.  
Para solucionar esto podemos aprovechar que el arroba no recibe el decorator sino una linea de python cuyo resultado es el decorator.  
[Ver codigo](<3c - Decorators.ipynb>)  
Pero escribir las funciones anidadas puede ser dificil de manejar si necesitamos una logica compleja para esto podemos aprovechar el hecho de python es un lenguaje de tipado estructural y definir nuestro propio objeto en lugar de utilizar funciones.  
[Ver codigo](<3d - Decorators.ipynb>)  

---
Pero la magia de los decorators no termina ahí.  
Para empezar no es necesario que el decorator realmente cambie el contenido del atributo.   
Supongamos que queremos definir un framework de test, una forma de definir nuestro test podria ser.  
[Ver codigo](<3e - Decorators.ipynb>)  
Al escribir test tambien seguramente queramos definir un test suite y estamos en objetos así que una clase suena bastante razonable pero ¿cómo lo registramos?  
**Decorators al rescate.**  

Si bien ese es un ejemplo simple un decorator puede hacer cualquier cosa, un ejemplo de esto es la implementación de dataclasses.  
[Ver codigo](<3g - Decorators.ipynb>)  

## Descriptors

Para ver este ultimo metodo vamos a ver otro decorador de Python, property, que nos permite definir getter y setters para nuestros objetos.  
[Ver codigo](<4a - Descriptors.ipynb>)  
¿Cómo podemos definir algo así?   
Si nos fijamos en lo que contienen los atributos en la clase, tenemos un objeto Property, con eso sabemos que vamos a necesitar al menos una clase que reciba el getter al instanciar y un metodo setter que reciba la función del setter.  
[Ver codigo](<4b - Descriptors.ipynb>)  
Pero solo con eso nos quedamos cortos, acá es donde entran los descriptores. Un descriptor es cualquier objeto que implemente al menos el metodo magico \_\_get\_\_ y opcionalmente los metodos \_\_set\_\_ y \_\_del\_\_
[Ver codigo](<4c - Descriptors.ipynb>)  
\_\_get\_\_ recibe el objeto sobre el que se está haciendo la llamada y su clase si se está pidiendo el atributo de una instancia o None y la clase si se está pidiendo directamente a la clase.
En cambio \_\_set\_\_ recibe solo el objeto y el valor a settear porque si no quitar el descriptor seria recursivo.  
Pero esto no termina acá, si se combina con otras herramientas de python podemos extender la capacidad. Por ejemplo que nos de más información del error.  
[Ver codigo](<4d - Descriptors.ipynb>)  
O que modifique directamente el objeto sobre el que está aplicado.  
[Ver codigo](<4e - Descriptors.ipynb>)  
