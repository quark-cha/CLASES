RAMANUJAN, π Y LA ESTRUCTURA QUE RELACIONA LAS CONSTANTES

CLASES · Artículo 01
Una propuesta de investigación desde las clases de UNIHOLOG

Víctor Estrada Díaz

Hay fórmulas que permiten calcular. Otras, además, nos obligan a preguntar.

La de Ramanujan para el inverso de π pertenece a ambas categorías:

1/π = (2√2/9801) ∑ₖ₌₀∞ [(4k)!/(k!)⁴] · (1103 + 26390k)/396⁴ᵏ

La suma comienza en k = 0 y continúa indefinidamente.

No es una coincidencia decimal ni una aproximación convertida en igualdad. La serie converge exactamente a 1/π. Lo aproximado es el resultado cuando detenemos la suma después de un número finito de términos.

Su rapidez es extraordinaria: cada término aporta aproximadamente ocho cifras decimales correctas adicionales. Invirtiendo la suma parcial obtenemos una aproximación a π con esa misma rapidez asintótica.

Conviene expresarlo con precisión: no existe una garantía general de que cada iteración fije exactamente ocho cifras nuevas. La ganancia asintótica es de unas 7,98 cifras por término. La exactitud pertenece a la identidad infinita.

Pero mi interés no termina en calcular π.

La pregunta es: ¿por qué aparecen precisamente esas constantes?

CUATRO CONSTANTES BAJO UNA MISMA SUMA

Podemos escribir la estructura general así:

F(a, b, c, d) = a ∑ₖ₌₀∞ [(4k)!/(k!)⁴] · (b + ck)/d⁴ᵏ

En la fórmula de Ramanujan:

a = 2√2/9801
b = 1103
c = 26390
d = 396

Su factorización es:

9801 = 99² = 3⁴ · 11²

a = 2√2/(3⁴ · 11²)

b = 1103, número primo

c = 26390 = 2 · 5 · 7 · 13 · 29

d = 396 = 2² · 3² · 11 = 4 · 99

Y, por tanto:

d⁴ = 2⁸ · 3⁸ · 11⁴ = 256 · 99⁴

Esta escritura ya muestra algo: 9801 y 396 comparten la estructura de 99. No son números desligados.

También hay una redundancia en nuestra parametrización. La serie depende de los productos ab y ac. Multiplicar a por un número λ distinto de cero y dividir b y c por ese mismo λ deja cada término inalterado.

Podemos elegir cuatro parámetros para definir una familia de series, pero eso no convierte los valores de Ramanujan en cuatro grados de libertad independientes dentro de la identidad.

¿POR QUÉ ESAS CUATRO CONSTANTES?

Factorizar permite reconocer componentes, pero todavía no explica su procedencia.

Decir que 396 = 4 · 99 describe una relación. No explica de dónde sale 99.

Decir que a contiene √2 tampoco explica por qué aparece esa raíz.

La pregunta de fondo es qué estructura produce simultáneamente los coeficientes y hace que su combinación converja exactamente a 1/π.

Esa estructura se ha estudiado mediante funciones elípticas, ecuaciones modulares y valores algebraicos especiales. En esta fórmula interviene el caso modular N = 58.

Podemos ver una parte concreta de esa conexión.

UNA MISMA RAÍZ ALGEBRAICA

En la derivación aparece una cantidad:

u = (5 + √29)/2

Su sexta potencia es exactamente:

u⁶ = 9801 + 1820√29

Como:

9801² − 29 · 1820² = 1

su inverso cumple:

u⁻⁶ = 9801 − 1820√29

Al sumar ambos desaparece la raíz:

u⁶ + u⁻⁶ = 19602

Por tanto:

x = 2/(u⁶ + u⁻⁶) = 1/9801 = 1/99²

En la serie transformada interviene x²:

x² = 1/99⁴

La cuarta potencia de 99 surge así de una evaluación algebraica común.

La conexión con los factoriales se ve en esta identidad:

(4k)!/(k!)⁴ = 256ᵏ · (¼)ₖ(½)ₖ(¾)ₖ/(k!)³

Aquí (r)ₖ representa el producto ascendente r(r + 1)…(r + k − 1), y (r)₀ = 1.

El factor 256ᵏ se combina con el denominador:

256ᵏ/396⁴ᵏ = (1/99⁴)ᵏ

No hemos escogido una cuarta potencia por conveniencia: aparece al transformar la estructura de la serie.

LA RAÍZ DE DOS Y EL COEFICIENTE 26390

La diferencia de las dos potencias anteriores conserva la raíz:

(u⁶ − u⁻⁶)/2 = 1820√29

Al combinarla con √58:

√58 · 1820√29 = 1820 · 29√2

Y, exactamente:

1820 · 29√2 = 2√2 · 26390

Aquí aparecen unidos √2 y 26390.

También el coeficiente 1103 resulta de una cancelación exacta en otra evaluación elíptica:

[297(33√29 − 148) − √29(9801 − 1820√29)]/(2√2)

Como 297 · 33 = 9801, los términos con √29 se cancelan. Queda:

(−43956 + 52780)/(2√2)
= 8824/(2√2)
= 2√2 · 1103

Estos cálculos muestran cómo emergen las constantes a partir de valores comunes. La demostración completa debe justificar también las evaluaciones elípticas de partida.

¿DÓNDE ESTÁ π?

El puente incluye la relación de Legendre:

K E′ + E K′ − K K′ = π/2

K y E son integrales elípticas completas. Aquí las primas indican las integrales correspondientes al módulo complementario; no representan derivadas.

Las transformaciones de estas relaciones en series permiten obtener 1/π.

Así se enlazan una identidad analítica que contiene π y unas evaluaciones algebraicas que producen enteros y radicales.

GRUPOS, TRANSFORMACIONES E INVARIANTES

La teoría de grupos interviene porque distintas descripciones pueden representar una misma estructura geométrica.

En el contexto modular aparecen transformaciones:

τ → (pτ + q)/(rτ + s)

con p, q, r y s enteros y ps − qr = 1.

Utilizo letras distintas para no confundirlas con los cuatro parámetros de la serie.

Estas transformaciones forman el marco del grupo modular. Sus subgrupos permiten estudiar funciones y cantidades invariantes bajo determinadas transformaciones.

La pregunta ya no se limita a qué valor tiene una constante. También pregunta qué permanece cuando cambia la descripción y qué relaciones quedan obligadas por la estructura.

CLASES: UN NUEVO PROYECTO DESDE UNIHOLOG

Este es el punto de partida del nuevo proyecto CLASES: una investigación que toma como base mis clases de UNIHOLOG.

El objetivo será precisar sus elementos, definir las transformaciones admisibles y estudiar qué relaciones permanecen invariantes.

Después habrá que comprobar qué estructura forman esas transformaciones: un grupo, cuando satisfagan sus condiciones, u otra estructura algebraica cuando no las satisfagan.

La pregunta central será:

¿Podemos deducir relaciones entre constantes a partir de las clases y sus invariantes, sin introducir previamente los valores que pretendemos explicar?

La fórmula de Ramanujan aporta un ejemplo de relaciones profundas entre constantes aparentemente separadas. No demuestra por sí sola que exista una relación universal entre todas las constantes físicas.

Pero ofrece una dirección de trabajo: buscar la estructura que obliga a los valores, además de calcular los valores que aparecen.

CONSTANTES Y UNIDADES NATURALES

Todos los números de esta identidad son adimensionales.

En física debemos distinguir las constantes cuyo valor numérico depende de las unidades de aquellas combinaciones adimensionales que conservan su valor al cambiar de unidades.

Las unidades naturales simplifican la expresión de las leyes. Las relaciones entre cantidades adimensionales permiten preguntar qué contenido permanece independientemente de esa elección.

Por eso el proyecto deberá distinguir una simplificación debida a las unidades de una relación deducida de la estructura.

Una coincidencia decimal puede sugerir una búsqueda. Una demostración establece la relación.

RAMANUJAN Y EL DESCUBRIMIENTO

Ramanujan publicó esta fórmula en 1914. No es correcto afirmar que desconocía por completo las matemáticas elípticas: había desarrollado por su cuenta parte de ese terreno, con métodos y notaciones propios.

Lo que no conocemos completamente es el recorrido de descubrimiento que lo llevó a cada resultado.

Las demostraciones posteriores explican por qué funciona la identidad. No reconstruyen necesariamente cómo llegó él a descubrirla.

Ese espacio entre reconocer una relación y demostrarla sigue siendo una de las cuestiones más interesantes de la investigación.

Mi propuesta es convertir esta pregunta en trabajo concreto desde UNIHOLOG: definiciones explícitas, transformaciones, invariantes y relaciones que puedan comprobarse.

¿Por qué esas constantes?

¿Son los valores el punto de partida, o son la consecuencia visible de una estructura que debemos desentrañar?

Víctor Estrada Díaz
Einstein-VED · Proyecto CLASES · UNIHOLOG

Web del autor:
https://estradad.es

Publicación principal Einstein-VED:
https://doi.org/10.5281/zenodo.17172925

ORCID:
https://orcid.org/0000-0001-9942-1021

REFERENCIAS

S. Ramanujan. Modular equations and approximations to π. Quarterly Journal of Mathematics, 45, 350–372, 1914.
https://ramanujan.sirinudi.org/Volumes/published/ram06.html

Chieh-Lei Wong. On the elegance of Ramanujan’s series for π, 2021. Especialmente el caso N = 58.
https://arxiv.org/abs/2104.12412

Thang Pang Ern y Devandhira Wijaya Wangsa. A Proof of Ramanujan’s Classic π Formula, 2024.
https://arxiv.org/abs/2411.15803

J. S. Milne. Modular Functions and Modular Forms.
https://www.jmilne.org/math/CourseNotes/mf.html

LICENCIA DUAL

Texto: CC BY-NC-SA 4.0.
https://creativecommons.org/licenses/by-nc-sa/4.0/

Código, si se incorpora al proyecto: Hippocratic License 3.0, HL3.
https://firstdonoharm.dev/version/3/0/

Condiciones éticas del autor: prohibidos los usos para guerras, violaciones de derechos humanos, daño ambiental, explotación, vigilancia masiva y discriminación.
https://estradad.es/licencia.php

#CLASES #Ramanujan #Pi #Matemáticas #TeoríaDeGrupos #Constantes #UNIHOLOG #EinsteinVED #Investigación


