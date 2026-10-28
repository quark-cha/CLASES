# ES_50: — Primalidad estructural de las clases $U_c$ y el grado de $ñ$

Víctor Estrada Díaz  
UNIHOLOG

## Resumen

En ES_49 se introdujo la idea de una clase $U_c$ como el conjunto de expresiones que determinan una misma constante $c$.

Este documento continúa esa construcción y plantea una pregunta más profunda: si una constante queda representada por una clase $U_c$, ¿puede dicha clase considerarse primaria, o depende estructuralmente de otras clases?

La cuestión se formula mediante una noción de primalidad estructural y mediante el orden estructural de dependencia:

$$
\operatorname{osd}(U_c).
$$

El caso central es la constante geométrica $ñ$, definida en el marco UNIHOLOG como una relación entre dos geometrías. Aunque puede escribirse como

$$
ñ=8\pi l_p^2,
$$

su sentido no procede de $G$, sino de una relación geométrica previa. Por ello, la cuestión no es si $ñ$ puede escribirse usando $l_p$, sino si $U_{ñ}$ es una clase prima o una clase compuesta.

## 1. Punto de partida

Sea $c$ una constante.

Definimos $U_c$ como el conjunto de expresiones que determinan exactamente el mismo valor $c$:

$$
U_c=\{A:\operatorname{valor}(A)=c\}.
$$

Dos expresiones $A$ y $B$ pertenecen a la misma clase $U_c$ si ambas determinan el mismo valor:

$$
A\sim_c B
\iff
\operatorname{valor}(A)=\operatorname{valor}(B)=c.
$$

Esta definición no identifica los procedimientos entre sí. Una expresión algebraica exacta, una sucesión, una integral, una derivada o una fracción continua pueden pertenecer a la misma clase si determinan el mismo valor.

Por ejemplo:

$$
e=\lim_{n\to\infty}\left(1+\frac1n\right)^n
$$

y

$$
e=\sum_{n=0}^{\infty}\frac1{n!}
$$

son expresiones distintas, pero ambas pertenecen a $U_e$.

## 2. Expresiones primarias y expresiones derivadas

No todas las expresiones de una clase $U_c$ tienen el mismo valor estructural.

Si una expresión se obtiene por una transformación trivial de otra expresión ya conocida, no abre una vía nueva hacia la constante.

Por ejemplo, si

$$
A\in U_c,
$$

entonces también:

$$
A+0\in U_c,
$$

$$
A\cdot1\in U_c,
$$

$$
\frac{2A}{2}\in U_c.
$$

Estas expresiones pertenecen formalmente a $U_c$, pero no son primarias.

Llamaremos expresión primaria de $U_c$ a una expresión que determina $c$ y que no se presenta como una simple transformación trivial de otra expresión ya incluida en el catálogo.

Esta noción es relativa al conocimiento disponible. Una expresión puede parecer primaria hasta que se encuentra una derivación que la conecta con otra expresión anterior.

Por tanto, definimos provisionalmente:

$$
U_c^{\mathrm{prim}}
=
\{A\in U_c:A\ \text{no es derivada trivial de otra expresión conocida de }U_c\}.
$$

## 3. Generación entre clases

Sea $\mathcal B$ una familia de clases:

$$
\mathcal B=\{U_{c_1},U_{c_2},\ldots,U_{c_k}\}.
$$

Diremos que una constante $c$ es generable desde $\mathcal B$ si existe una función admisible $F$ tal que:

$$
c=F(c_1,c_2,\ldots,c_k).
$$

En ese caso:

$$
U_c\subseteq\operatorname{Gen}(\mathcal B).
$$

Aquí $\operatorname{Gen}(\mathcal B)$ representa el conjunto de clases obtenibles a partir de $\mathcal B$ mediante operaciones admitidas.

Estas operaciones pueden incluir suma, producto, cociente, potencias, raíces, límites, series, productos infinitos, integrales, derivadas o funciones especiales, siempre que estén bien definidas y justificadas.

Por ejemplo, si:

$$
A\in U_\alpha
$$

y

$$
B\in U_\beta,
$$

entonces:

$$
A+B\in U_{\alpha+\beta},
$$

$$
AB\in U_{\alpha\beta},
$$

y, si $\beta\ne0$:

$$
\frac{A}{B}\in U_{\alpha/\beta}.
$$

## 4. Primalidad estructural

La analogía con los números primos aparece cuando preguntamos si una clase puede obtenerse a partir de otras.

Un número primo no se descompone como producto no trivial de enteros menores.

De modo análogo, una clase $U_c$ puede llamarse estructuralmente prima si no se obtiene como combinación no trivial de otras clases independientes.

Definimos:

$$
U_c\ \text{es prima respecto de}\ \mathcal B
$$

si:

$$
c\notin\operatorname{Gen}(\mathcal B\setminus\{U_c\}).
$$

Esto no significa que $U_c$ carezca de estructura interna.

Una clase prima puede contener muchas expresiones:

$$
A_1,A_2,A_3,\ldots\in U_c.
$$

Lo que se niega no es la multiplicidad interna de expresiones, sino la dependencia externa respecto de otras clases.

## 5. Desarrollo interno mediante $\mathbb N$

Toda constante computable admite al menos una representación mediante una sucesión indexada por números naturales.

Es decir, para una constante computable $c$, existe una sucesión racional o real:

$$
a:\mathbb N\to\mathbb Q
$$

tal que:

$$
\lim_{n\to\infty}a_n=c.
$$

Por tanto:

$$
\lim_{n\to\infty}a_n\in U_c.
$$

Esto muestra que una clase puede ser estructuralmente prima y, al mismo tiempo, admitir desarrollos internos infinitos.

La primalidad no excluye el desarrollo.

Solo excluye la dependencia generativa no trivial respecto de otras clases.

## 6. Orden estructural de dependencia

Definimos el orden estructural de dependencia de una clase $U_c$ como:

$$
\operatorname{osd}(U_c).
$$

Informalmente, $\operatorname{osd}(U_c)$ mide el número mínimo de clases necesarias para determinar $U_c$ mediante una relación estructural cerrada.

Una formulación posible es:

$$
\operatorname{osd}(U_c)
=
\min
\left\{
k:
\exists R(c,c_1,\ldots,c_k)=0
\right\},
$$

donde la relación $R$ debe ser no trivial y no debe poder reducirse eliminando una de las clases participantes.

Si:

$$
\operatorname{osd}(U_c)=1,
$$

entonces $U_c$ se comporta como una clase primaria.

Si:

$$
\operatorname{osd}(U_c)>1,
$$

entonces $U_c$ aparece como parte de una relación mínima con otras clases.

## 7. La identidad de Euler

La identidad de Euler es:

$$
e^{i\pi}+1=0.
$$

Esta relación conecta las clases:

$$
U_e,\quad U_i,\quad U_\pi,\quad U_1,\quad U_0.
$$

No afirma que:

$$
U_e=U_\pi.
$$

Tampoco afirma que $e$ y $\pi$ sean la misma constante.

Lo que muestra es que existe una relación estructural cerrada en la que estas clases aparecen simultáneamente.

Si se toma una de ellas como incógnita, las otras son necesarias para reconstruirla dentro de esa relación.

Por ejemplo, formalmente:

$$
e^{i\pi}=-1.
$$

Si se intenta despejar $\pi$, aparece:

$$
\pi=\frac{\log(-1)}{i},
$$

pero esta expresión exige ya la estructura compleja, la unidad, el cero, la exponencial y una elección de rama del logaritmo.

Por tanto, Euler no elimina la independencia de $e$, $\pi$ o $i$. Muestra una relación mínima donde ninguna de esas clases puede retirarse sin cambiar la estructura.

## 8. Independencia y relación no son lo mismo

Dos clases pueden ser independientes y, aun así, estar relacionadas.

La independencia generativa afirma que una clase no se obtiene desde otra mediante las reglas admitidas:

$$
U_a\not\subseteq\operatorname{Gen}(U_b).
$$

Pero puede existir una relación:

$$
R(a,b)=0.
$$

Por tanto, debe distinguirse:

$$
\text{dependencia generativa}
$$

de:

$$
\text{relación estructural}.
$$

La identidad de Euler es precisamente un ejemplo de relación estructural profunda entre clases que no se reducen de manera trivial unas a otras.

## 9. El caso de $ñ$

En UNIHOLOG, la constante $ñ$ se presenta como una constante geométrica.

Puede escribirse:

$$
ñ=8\pi l_p^2.
$$

Pero esta escritura no debe interpretarse necesariamente en el sentido:

$$
G\longrightarrow l_p\longrightarrowñ.
$$

En el marco UNIHOLOG, la dirección conceptual es:

$$
\text{relación entre dos geometrías}
\longrightarrow
ñ
\longrightarrow
l_p^2
\longrightarrow
G.
$$

Es decir, $ñ$ no se introduce como una constante derivada de $G$, sino como una relación geométrica previa.

Después, si se usa:

$$
l_p^2=\frac{\left(\frac{h}{2\pi}\right) G}{c^3},
$$

entonces:

$$
ñ=\frac{4h G}{c^3}.
$$

Y por tanto:

$$
G=\frac{ñ c^3}{4h}.
$$

Así, en este marco, $G$ no es primaria respecto de $ñ$.

Al contrario:

$$
U_G\subseteq\operatorname{Gen}(U_{ñ},U_c,U_h).
$$

Por tanto:

$$
U_G\ \text{es compuesta respecto de}\ U_{ñ}.
$$

## 10. Anticircularidad de $ñ$

La objeción de circularidad dice:

$$
ñ=8\pi l_p^2
$$

y:

$$
l_p^2=\frac{\left(\frac{h}{2\pi}\right) G}{c^3}.
$$

Por tanto, parecería que $ñ$ depende de $G$.

Pero esa objeción solo es válida si $G$ se toma como premisa.

Si $ñ$ se obtiene independientemente como relación geométrica entre dos estructuras, entonces $G$ no es premisa, sino consecuencia:

$$
G=\frac{ñ c^3}{4h}.
$$

La misma igualdad puede leerse en dos direcciones.

La lectura estándar es:

$$
G\to l_p^2\toñ.
$$

La lectura UNIHOLOG es:

$$
ñ\to l_p^2\to G.
$$

Por tanto, no hay circularidad si la derivación de $ñ$ es geométrica e independiente de $G$.

## 11. La pregunta abierta

No conocemos todavía el grado estructural de $ñ$.

La pregunta es:

$$
\operatorname{osd}(U_{ñ})=1
$$

o:

$$
\operatorname{osd}(U_{ñ})>1.
$$

Si:

$$
\operatorname{osd}(U_{ñ})=1,
$$

entonces $U_{ñ}$ sería una clase primaria.

En ese caso, $ñ$ sería un valor geométrico que no depende de otras clases para quedar determinado.

Si:

$$
\operatorname{osd}(U_{ñ})>1,
$$

entonces deberá existir una relación matemática o geométrica mínima:

$$
R(ñ,c_1,c_2,\ldots,c_k)=0.
$$

En ese caso, $ñ$ no sería primaria aislada, sino una constante emergente de una relación estructural más profunda.

## 12. Consecuencia conceptual

La búsqueda de $ñ$ no consiste en buscar una combinación numérica cualquiera.

La búsqueda correcta es:

$$
\exists R:
R(ñ,c_1,\ldots,c_k)=0
$$

donde $R$ sea:

- no trivial;
- mínima;
- geométricamente interpretable;
- independiente de $G$ como premisa;
- capaz de determinar $ñ$.

Si tal relación se encuentra, entonces se habrá identificado el orden estructural de dependencia de $U_{ñ}$.

Si no existe tal relación y $ñ$ solo depende de sí misma como relación geométrica primaria, entonces:

$$
\operatorname{osd}(U_{ñ})=1.
$$

## 13. Conclusión

ES_49 permitió definir clases de expresiones $U_c$.

ES_50 introduce una pregunta nueva:

$$
\text{¿qué clases son estructuralmente primas?}
$$

La identidad de Euler muestra que varias clases pueden estar relacionadas en una estructura mínima sin reducirse trivialmente unas a otras.

El caso de $ñ$ plantea una pregunta análoga:

$$
\boxed{
\operatorname{osd}(U_{ñ})=1
\quad\text{o}\quad
\operatorname{osd}(U_{ñ})>1
}
$$

Si $U_{ñ}$ es prima, entonces $ñ$ expresa una constante geométrica irreducible.

Si no es prima, entonces algún día deberá encontrarse una relación matemática o geométrica mínima que la determine.

En ambos casos, $G$ queda situado como una clase derivada respecto de $ñ$, no como su fundamento.

