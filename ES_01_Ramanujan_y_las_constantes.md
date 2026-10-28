RAMANUJAN, π Y LA ESTRUCTURA QUE RELACIONA LAS CONSTANTES

CLASES · Artículo 01
Una propuesta de investigación desde las clases de UNIHOLOG

Víctor Estrada Díaz

Hay fórmulas que permiten calcular. Otras, además, nos obligan a preguntar.

La de Ramanujan para el inverso de π pertenece a ambas categorías:

$$
\frac{1}{\pi}=\frac{2\sqrt{2}}{9801}\sum_{k=0}^{\infty}\frac{(4k)!}{(k!)^4}\frac{1103+26390k}{396^{4k}}
$$

La suma comienza en $k=0$ y continúa indefinidamente.

No es una coincidencia decimal ni una aproximación convertida en igualdad. La serie converge exactamente a $1/\pi$. Lo aproximado es el resultado cuando detenemos la suma después de un número finito de términos.

Su rapidez es extraordinaria: cada término aporta aproximadamente ocho cifras decimales correctas adicionales. Invirtiendo la suma parcial obtenemos una aproximación a π con esa misma rapidez asintótica.

Conviene expresarlo con precisión: no existe una garantía general de que cada iteración fije exactamente ocho cifras nuevas. La ganancia asintótica es de unas 7,98 cifras por término. La exactitud pertenece a la identidad infinita.

Pero mi interés no termina en calcular $\pi$.

La pregunta es: ¿por qué aparecen precisamente esas constantes?

CUATRO CONSTANTES BAJO UNA MISMA SUMA

Podemos escribir la estructura general así:

$$
F(a,b,c,d)=a\sum_{k=0}^{\infty}\frac{(4k)!}{(k!)^4}\frac{b+ck}{d^{4k}}
$$

En la fórmula de Ramanujan:

$$
a=\frac{2\sqrt{2}}{9801}
$$
$$
b=1103
$$
$$
c=26390
$$
$$
d=396
$$

Su factorización es:

$$
9801=99^2=3^4\cdot11^2
$$

$$
a=\frac{2\sqrt{2}}{3^4\cdot11^2}
$$

$b=1103$, número primo

$$
c=26390=2\cdot5\cdot7\cdot13\cdot29
$$

$$
d=396=2^2\cdot3^2\cdot11=4\cdot99
$$

Y, por tanto:

$$
d^4=2^8\cdot3^8\cdot11^4=256\cdot99^4
$$

Esta escritura ya muestra algo: 9801 y 396 comparten la estructura de 99. No son números desligados.

También hay una redundancia en nuestra parametrización. La serie depende de los productos $ab$ y $ac$. Multiplicar $a$ por un número $\lambda$ distinto de cero y dividir $b$ y $c$ por ese mismo $\lambda$ deja cada término inalterado.

Podemos elegir cuatro parámetros para definir una familia de series, pero eso no convierte los valores de Ramanujan en cuatro grados de libertad independientes dentro de la identidad.

¿POR QUÉ ESAS CUATRO CONSTANTES?

Factorizar permite reconocer componentes, pero todavía no explica su procedencia.

Decir que $396=4\cdot99$ describe una relación. No explica de dónde sale 99.

Decir que $a$ contiene $\sqrt{2}$ tampoco explica por qué aparece esa raíz.

La pregunta de fondo es qué estructura produce simultáneamente los coeficientes y hace que su combinación converja exactamente a $1/\pi$.

Esa estructura se ha estudiado mediante funciones elípticas, ecuaciones modulares y valores algebraicos especiales. En esta fórmula interviene el caso modular $N=58$.

Podemos ver una parte concreta de esa conexión.

UNA MISMA RAÍZ ALGEBRAICA

En la derivación aparece una cantidad:

$$
u=\frac{5+\sqrt{29}}{2}
$$

Su sexta potencia es exactamente:

$$
u^6=9801+1820\sqrt{29}
$$

Como:

$$
9801^2-29\cdot1820^2=1
$$

su inverso cumple:

$$
u^{-6}=9801-1820\sqrt{29}
$$

Al sumar ambos desaparece la raíz:

$$
u^6+u^{-6}=19602
$$

Por tanto:

$$
x=\frac{2}{u^6+u^{-6}}=\frac{1}{9801}=\frac{1}{99^2}
$$

En la serie transformada interviene $x^2$:

$$
x^2=\frac{1}{99^4}
$$

La cuarta potencia de 99 surge así de una evaluación algebraica común.

La conexión con los factoriales se ve en esta identidad:

$$
\frac{(4k)!}{(k!)^4}=256^k\frac{\left(\frac14\right)_k\left(\frac12\right)_k\left(\frac34\right)_k}{(k!)^3}
$$

Aquí $(r)_k$ representa el producto ascendente $r(r+1)\cdots(r+k-1)$, y $(r)_0=1$.

El factor $256^k$ se combina con el denominador:

$$
\frac{256^k}{396^{4k}}=\left(\frac{1}{99^4}\right)^k
$$

No hemos escogido una cuarta potencia por conveniencia: aparece al transformar la estructura de la serie.

LA RAÍZ DE DOS Y EL COEFICIENTE 26390

La diferencia de las dos potencias anteriores conserva la raíz:

$$
\frac{u^6-u^{-6}}{2}=1820\sqrt{29}
$$

Al combinarla con $\sqrt{58}$:

$$
\sqrt{58}\cdot1820\sqrt{29}=1820\cdot29\sqrt{2}
$$

Y, exactamente:

$$
1820\cdot29\sqrt{2}=2\sqrt{2}\cdot26390
$$

Aquí aparecen unidos $\sqrt{2}$ y $26390$.

También el coeficiente 1103 resulta de una cancelación exacta en otra evaluación elíptica:

$$
\frac{297(33\sqrt{29}-148)-\sqrt{29}(9801-1820\sqrt{29})}{2\sqrt{2}}
$$

Como $297\cdot33=9801$, los términos con $\sqrt{29}$ se cancelan. Queda:

$$
\frac{-43956+52780}{2\sqrt{2}}=\frac{8824}{2\sqrt{2}}=2\sqrt{2}\cdot1103
$$

Estos cálculos muestran cómo emergen las constantes a partir de valores comunes. La demostración completa debe justificar también las evaluaciones elípticas de partida.

¿DÓNDE ESTÁ $\pi$?

El puente incluye la relación de Legendre:

$$
K E^{\prime}+E K^{\prime}-K K^{\prime}=\frac{\pi}{2}
$$

$K$ y $E$ son integrales elípticas completas. Aquí las primas indican las integrales correspondientes al módulo complementario; no representan derivadas.

Las transformaciones de estas relaciones en series permiten obtener $1/\pi$.

Así se enlazan una identidad analítica que contiene $\pi$ y unas evaluaciones algebraicas que producen enteros y radicales.

GRUPOS, TRANSFORMACIONES E INVARIANTES

La teoría de grupos interviene porque distintas descripciones pueden representar una misma estructura geométrica.

En el contexto modular aparecen transformaciones:

$$
\tau\longmapsto\frac{p\tau+q}{r\tau+s}
$$

con $p$, $q$, $r$ y $s$ enteros y $ps-qr=1$.

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

Chieh-Lei Wong. On the elegance of Ramanujan’s series for π, 2021. Especialmente el caso $N=58$.
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


