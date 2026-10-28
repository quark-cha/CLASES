# ES_49: — El nexo discreto-continuo mediante clases de equivalencia

## UNIHOLOG

Este documento reconstruye el desarrollo de ES_49 sobre el nexo entre lo discreto y lo continuo, formulado sin identificar falsamente $\mathbb N$ con $\mathbb R$.

El punto central no es que el conjunto de los naturales y el conjunto de los reales sean equivalentes como estructuras. No lo son. El punto central es más preciso: una construcción discreta indexada por $\mathbb N$ y una construcción continua definida sobre $\mathbb R$ pueden determinar exactamente un mismo objeto matemático de $\mathbb R$.

Ese objeto común funciona como nexo.

En ES_49 este nexo se expresa mediante familias o clases de equivalencia del tipo $U_e$, $U_\pi$, $U_\varphi$, $U_{ñ}$, $U_g$ y, en forma general, $U_{f_i}$.

Todas las fórmulas de este documento se escriben usando únicamente `$...$` para expresiones inline y `$$...$$` para bloques.

---

## 1. Punto de partida

Sea $\alpha\in\mathbb R$ una constante real.

Una misma constante puede aparecer mediante expresiones de naturaleza diferente.

Por ejemplo, puede aparecer como límite de una sucesión:

$$
\lim_{n\to\infty}a_n=\alpha,
$$

donde el índice $n$ pertenece a $\mathbb N$.

También puede aparecer mediante un proceso continuo:

$$
\lim_{dx\to0}Q(F,x,dx)=\alpha,
$$

donde $x$ y $dx$ pertenecen al marco de variación de $\mathbb R$.

La primera construcción usa una estructura discreta:

$$
n=1,2,3,\ldots
$$

La segunda usa una estructura continua:

$$
dx\to0.
$$

Sin embargo, si ambas construcciones determinan el mismo valor $\alpha$, entonces ambas pertenecen a una misma clase respecto de su valor.

El nexo no es una identidad entre dominios.

El nexo es el valor común.

---

## 2. Distinción fundamental entre expresión finita, proceso límite y valor

Antes de definir las clases $U_\alpha$, conviene separar tres niveles.

### 2.1 Expresión finita dependiente de un parámetro

Una expresión como

$$
\left(1+\frac1n\right)^n
$$

depende de $n$.

Para un valor finito de $n$, en general no es igual a su límite.

Por tanto,

$$
\left(1+\frac1n\right)^n\neq e
$$

para todo $n$ finito.

### 2.2 Proceso límite

El proceso completo

$$
\lim_{n\to\infty}\left(1+\frac1n\right)^n
$$

sí determina exactamente $e$.

La expresión finita no pertenece a $U_e$ como expresión exacta, pero el proceso límite completo sí pertenece a $U_e$.

### 2.3 Valor determinado

El valor determinado por el proceso es el objeto matemático:

$$
e.
$$

Así, ES_49 distingue:

1. aproximaciones finitas;
2. procesos límite;
3. valores exactos determinados por esos procesos.

Esta distinción evita confundir una sucesión de aproximaciones con la constante misma.

---

## 3. Definición de $U_\alpha$

Sea $\alpha\in\mathbb R$.

Definimos $U_\alpha$ como el conjunto de expresiones, definiciones, procesos o construcciones matemáticas que determinan exactamente el valor $\alpha$.

Formalmente:

$$
U_\alpha=
\left\{
A:\operatorname{valor}(A)=\alpha
\right\}.
$$

Aquí $\operatorname{valor}(A)$ debe interpretarse como el valor matemático determinado por $A$, siempre que dicho valor esté bien definido.

Si $A$ es una expresión exacta, entonces $\operatorname{valor}(A)$ es su valor directo.

Si $A$ es un proceso límite, entonces $\operatorname{valor}(A)$ es el límite, siempre que exista.

Por ejemplo:

$$
A=\sum_{k=0}^{\infty}\frac1{k!}
$$

determina $e$.

También:

$$
B=\lim_{n\to\infty}\left(1+\frac1n\right)^n
$$

determina $e$.

Por tanto:

$$
A\in U_e
$$

y

$$
B\in U_e.
$$

---

## 4. Relación de equivalencia asociada

Para una constante fija $\alpha\in\mathbb R$, definimos la relación:

$$
A\sim_\alpha B
\iff
\operatorname{valor}(A)=\operatorname{valor}(B)=\alpha.
$$

Esta relación identifica expresiones por su valor común, no por su forma sintáctica ni por su procedimiento de obtención.

### Teorema 1 — $\sim_\alpha$ es una relación de equivalencia

Sea $\alpha\in\mathbb R$ y sea $U_\alpha$ el conjunto de construcciones que determinan $\alpha$. Entonces $\sim_\alpha$ es una relación de equivalencia sobre $U_\alpha$.

### Demostración

Reflexividad:

Si $A\in U_\alpha$, entonces

$$
\operatorname{valor}(A)=\alpha.
$$

Por tanto:

$$
A\sim_\alpha A.
$$

Simetría:

Si $A\sim_\alpha B$, entonces:

$$
\operatorname{valor}(A)=\operatorname{valor}(B)=\alpha.
$$

Por igualdad simétrica:

$$
\operatorname{valor}(B)=\operatorname{valor}(A)=\alpha.
$$

Luego:

$$
B\sim_\alpha A.
$$

Transitividad:

Si $A\sim_\alpha B$ y $B\sim_\alpha C$, entonces:

$$
\operatorname{valor}(A)=\operatorname{valor}(B)=\alpha
$$

y

$$
\operatorname{valor}(B)=\operatorname{valor}(C)=\alpha.
$$

Por tanto:

$$
\operatorname{valor}(A)=\operatorname{valor}(C)=\alpha.
$$

Luego:

$$
A\sim_\alpha C.
$$

Así, $\sim_\alpha$ es reflexiva, simétrica y transitiva. Por consiguiente, es una relación de equivalencia.

---

## 5. Nexo entre $\mathbb N$ y $\mathbb R$

Sea $\alpha\in\mathbb R$.

Supongamos que existe una sucesión $(a_n)_{n\in\mathbb N}$ tal que:

$$
\lim_{n\to\infty}a_n=\alpha.
$$

Supongamos además que existe un proceso continuo asociado a una función $F$ tal que:

$$
\lim_{dx\to0}Q(F,x,dx)=\alpha.
$$

Entonces ambas construcciones pertenecen a $U_\alpha$.

La situación puede representarse esquemáticamente como:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\alpha
\xleftarrow{\ dx\to0\ }
\mathbb R.
$$

Esta escritura no significa:

$$
\mathbb N=\mathbb R.
$$

Tampoco significa:

$$
\mathbb N\cong\mathbb R
$$

como conjuntos, espacios topológicos, cuerpos o estructuras de orden.

Significa únicamente que dos procedimientos definidos desde naturalezas distintas pueden determinar el mismo elemento $\alpha$ de $\mathbb R$.

### Teorema 2 — Nexo discreto-continuo

Sea $\alpha\in\mathbb R$. Si existe una construcción discreta $A_N$ indexada por $\mathbb N$ y una construcción continua $A_R$ definida sobre $\mathbb R$ tales que:

$$
\operatorname{valor}(A_N)=\alpha
$$

y

$$
\operatorname{valor}(A_R)=\alpha,
$$

entonces:

$$
A_N\sim_\alpha A_R.
$$

En consecuencia, $A_N$ y $A_R$ pertenecen a la misma clase $U_\alpha$.

### Demostración

Por hipótesis:

$$
\operatorname{valor}(A_N)=\alpha
$$

y

$$
\operatorname{valor}(A_R)=\alpha.
$$

Entonces:

$$
\operatorname{valor}(A_N)=\operatorname{valor}(A_R)=\alpha.
$$

Por definición de $\sim_\alpha$:

$$
A_N\sim_\alpha A_R.
$$

Por tanto:

$$
A_N,A_R\in U_\alpha.
$$

Queda probado.

---

## 6. Aplicación a $e$

La constante $e$ constituye un ejemplo central porque aparece de forma natural tanto en construcciones discretas como en caracterizaciones continuas.

### 6.1 Construcción discreta

Consideremos la sucesión:

$$
a_n=\left(1+\frac1n\right)^n,
\qquad n\in\mathbb N.
$$

Entonces:

$$
\lim_{n\to\infty}\left(1+\frac1n\right)^n=e.
$$

La construcción está indexada por valores discretos:

$$
n=1,2,3,\ldots
$$

El valor $e$ aparece como límite cuando:

$$
n\to\infty.
$$

Por tanto:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
e.
$$

Esta expresión no afirma que $e\in\mathbb N$.

Afirma que una sucesión indexada por $\mathbb N$ determina, en el límite, un elemento de $\mathbb R$.

### 6.2 Construcción por serie

También se tiene:

$$
e=\sum_{k=0}^{\infty}\frac1{k!}.
$$

Esta representación también posee una estructura discreta, pues está indexada por $k\in\mathbb N$.

El objeto determinado es el mismo:

$$
\sum_{k=0}^{\infty}\frac1{k!}=e.
$$

### 6.3 Caracterización continua

Consideremos la función:

$$
f(x)=e^x.
$$

Su derivada se define por:

$$
f'(x)=
\lim_{dx\to0}
\frac{f(x+dx)-f(x)}{dx}.
$$

Sustituyendo:

$$
f'(x)=
\lim_{dx\to0}
\frac{e^{x+dx}-e^x}{dx}.
$$

Factorizando:

$$
f'(x)=
e^x
\lim_{dx\to0}
\frac{e^{dx}-1}{dx}.
$$

La base $e$ se caracteriza por:

$$
\lim_{dx\to0}
\frac{e^{dx}-1}{dx}=1.
$$

Por tanto:

$$
\frac{d}{dx}e^x=e^x.
$$

En particular:

$$
e=e^1.
$$

Aquí $e$ aparece dentro de una estructura continua, ligada al límite diferencial:

$$
dx\to0.
$$

Así:

$$
\mathbb R
\xrightarrow{\ dx\to0\ }
e.
$$

### 6.4 Clase $U_e$

Definimos:

$$
U_e=
\left\{
E_i:\operatorname{valor}(E_i)=e
\right\}.
$$

Ejemplos de elementos de $U_e$ son:

$$
\lim_{n\to\infty}\left(1+\frac1n\right)^n,
$$

$$
\sum_{k=0}^{\infty}\frac1{k!},
$$

$$
\exp(1),
$$

$$
\int_1^e\frac1x\,dx=1
$$

como caracterización indirecta de $e$, es decir, $e$ es el único número real positivo que satisface:

$$
\int_1^e\frac1x\,dx=1.
$$

No todas estas expresiones tienen la misma forma. Algunas son límites, otras series, otras valores funcionales y otras caracterizaciones implícitas.

Sin embargo, todas determinan $e$.

Por tanto, pertenecen a la misma clase $U_e$.

### 6.5 $U_e$ conocido y $U_e$ desconocido

El conjunto total $U_e$ puede dividirse conceptualmente en dos regiones:

$$
U_e=U_e^{\mathrm{conocido}}\cup U_e^{\mathrm{desconocido}}.
$$

Aquí $U_e^{\mathrm{conocido}}$ representa las expresiones ya identificadas, verificadas o aceptadas como determinaciones de $e$ dentro de un marco matemático dado.

Por ejemplo:

$$
\exp(1)\in U_e^{\mathrm{conocido}}.
$$

También:

$$
\sum_{k=0}^{\infty}\frac1{k!}\in U_e^{\mathrm{conocido}}.
$$

Y:

$$
\lim_{n\to\infty}\left(1+\frac1n\right)^n\in U_e^{\mathrm{conocido}}.
$$

En cambio, $U_e^{\mathrm{desconocido}}$ designa las expresiones todavía no descubiertas, no clasificadas o no demostradas como equivalentes a $e$.

Esta división no es ontológica sino epistemológica.

El valor $e$ no cambia porque una expresión sea conocida o desconocida.

Lo que cambia es nuestro catálogo de expresiones reconocidas.

### 6.6 Enumeración de expresiones

Si se fija un lenguaje formal con un alfabeto finito o numerable y reglas sintácticas efectivas, el conjunto de expresiones finitas de ese lenguaje es numerable.

Por tanto, es posible enumerarlas sintácticamente:

$$
E_1,E_2,E_3,\ldots
$$

Sin embargo, no toda expresión sintáctica determina un valor real.

Y no siempre existe un procedimiento general que decida, para cualquier expresión suficientemente rica, si:

$$
\operatorname{valor}(E_i)=e.
$$

Por tanto, puede existir una enumeración sintáctica de candidatos sin que exista una clasificación completa y efectiva de $U_e$.

Esta observación separa tres cosas:

1. enumerar expresiones posibles;
2. evaluar expresiones bien definidas;
3. demostrar pertenencia a $U_e$.

### Corolario 1 — El catálogo conocido es parcial

El conjunto $U_e^{\mathrm{conocido}}$ no agota necesariamente $U_e$.

### Demostración

Por definición, $U_e^{\mathrm{conocido}}$ contiene las expresiones cuya pertenencia a $U_e$ ha sido reconocida dentro de un marco dado.

Pero la definición de $U_e$ no exige que sus elementos sean conocidos por nosotros. Solo exige que determinen $e$.

Por tanto, salvo que se demuestre una caracterización completa del lenguaje y de todos sus valores, no se puede concluir que:

$$
U_e^{\mathrm{conocido}}=U_e.
$$

Luego el catálogo conocido debe tratarse como parcial.

---

## 7. Aplicación a $\pi$

La constante $\pi$ también aparece como nexo entre construcciones discretas y continuas.

### 7.1 Serie discreta

Una representación clásica es:

$$
\pi=
4\sum_{k=0}^{\infty}
\frac{(-1)^k}{2k+1}.
$$

Equivalentemente:

$$
\pi=
\lim_{n\to\infty}
4\sum_{k=0}^{n}
\frac{(-1)^k}{2k+1}.
$$

Esta construcción está indexada por:

$$
n\in\mathbb N.
$$

Luego:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\pi.
$$

### 7.2 Integral continua

También se tiene:

$$
\pi=
4\int_0^1
\frac1{1+x^2}\,dx.
$$

La integral se construye mediante particiones de un intervalo real y el refinamiento de esas particiones.

En términos de escala:

$$
\Delta x\to0.
$$

Así:

$$
\mathbb R
\xrightarrow{\ \Delta x\to0\ }
\pi.
$$

### 7.3 Clase $U_\pi$

Definimos:

$$
U_\pi=
\left\{
P_i:\operatorname{valor}(P_i)=\pi
\right\}.
$$

Entonces pertenecen a $U_\pi$:

$$
4\sum_{k=0}^{\infty}
\frac{(-1)^k}{2k+1},
$$

$$
4\int_0^1
\frac1{1+x^2}\,dx,
$$

$$
\frac{C}{d}
$$

cuando $C$ es la longitud de una circunferencia euclídea y $d$ su diámetro.

Estas expresiones no son idénticas como procedimientos, pero son equivalentes respecto del valor que determinan.

Por tanto:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\pi
\xleftarrow{\ \Delta x\to0\ }
\mathbb R.
$$

### Corolario 2 — $\pi$ como invariante de representaciones

La constante $\pi$ actúa como invariante entre representaciones geométricas, analíticas, integrales y seriales.

### Demostración

Todas las expresiones anteriores determinan el mismo valor $\pi$ bajo sus hipótesis respectivas.

Por definición de $U_\pi$:

$$
P_i\in U_\pi
\iff
\operatorname{valor}(P_i)=\pi.
$$

Por tanto, todas pertenecen a la misma clase de equivalencia.

---

## 8. Aplicación a $\varphi$

Sea $\varphi$ la razón áurea:

$$
\varphi=
\frac{1+\sqrt5}{2}.
$$

Esta constante admite una definición algebraica exacta:

$$
\varphi^2=\varphi+1.
$$

También aparece como límite de cocientes de números de Fibonacci.

Sea $(F_n)$ la sucesión definida por:

$$
F_0=0,
$$

$$
F_1=1,
$$

y

$$
F_{n+1}=F_n+F_{n-1}.
$$

Entonces:

$$
\lim_{n\to\infty}
\frac{F_{n+1}}{F_n}
=\varphi.
$$

La construcción por Fibonacci es discreta, pues depende de $n\in\mathbb N$.

La construcción algebraica pertenece al cuerpo real.

Definimos:

$$
U_\varphi=
\left\{
\Phi_i:\operatorname{valor}(\Phi_i)=\varphi
\right\}.
$$

Entonces:

$$
\frac{1+\sqrt5}{2}\in U_\varphi
$$

y

$$
\lim_{n\to\infty}
\frac{F_{n+1}}{F_n}\in U_\varphi.
$$

De nuevo:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\varphi
\xleftarrow{\ \mathrm{algebra}\ }
\mathbb R.
$$

La notación anterior es esquemática: no afirma que el álgebra real sea un proceso diferencial. Solo señala que $\varphi$ puede ser determinado tanto desde una recurrencia discreta como desde una ecuación exacta en $\mathbb R$.

---

## 9. Sobre $U_{ñ}$

En ES_49 aparece la necesidad de representar el paso conceptual entre un índice natural $n$ y una forma extendida, interpolada o representada en un entorno continuo. Para ello se introduce la notación $ñ$.

La interpretación rigurosa debe ser cuidadosa.

No se debe afirmar que un natural $n$ sea idéntico a un real continuo.

Sí se puede considerar una aplicación de inclusión:

$$
\iota:\mathbb N\to\mathbb R
$$

dada por:

$$
\iota(n)=n.
$$

Esta inclusión permite ver cada número natural como un real particular, pero no convierte a $\mathbb N$ en $\mathbb R$.

También puede considerarse una interpolación o extensión de una sucesión discreta.

Si se tiene una sucesión:

$$
a:\mathbb N\to\mathbb R,
$$

puede buscarse una función:

$$
\tilde a:\mathbb R_{\ge 0}\to\mathbb R
$$

tal que:

$$
\tilde a(n)=a_n
$$

para todo $n\in\mathbb N$.

En este contexto, $ñ$ no representa una igualdad entre lo discreto y lo continuo. Representa una extensión, codificación o interpolación controlada.

Definimos entonces:

$$
U_{ñ}=
\left\{
N_i:\operatorname{valor}(N_i)=ñ
\right\},
$$

siempre que $ñ$ haya sido previamente definido dentro del sistema.

### Observación

$U_{ñ}$ no debe usarse como prueba de que $\mathbb N$ y $\mathbb R$ son equivalentes.

Debe usarse como familia de representaciones de una extensión o imagen concreta de un índice discreto dentro de una construcción más amplia.

---

## 10. Sobre $U_g$

Sea $g$ una magnitud real determinada por un modelo.

Por ejemplo, si $g$ representa la aceleración gravitatoria local, entonces no debe tratarse sin más como una constante universal absoluta, porque su valor depende del lugar, de la altura y del modelo físico usado.

En un marco local idealizado se puede fijar:

$$
g\approx 9.80665\,\mathrm{m/s^2}.
$$

Si el marco fija un valor exacto o convencional de $g$, entonces puede definirse:

$$
U_g=
\left\{
G_i:\operatorname{valor}(G_i)=g
\right\}.
$$

Una expresión dinámica posible es:

$$
s(t)=s_0+v_0t-\frac12gt^2.
$$

De ella se obtiene:

$$
\frac{d^2s}{dt^2}=-g.
$$

También puede aparecer mediante una ley de gravitación idealizada:

$$
g=\frac{GM}{r^2},
$$

bajo las hipótesis de masa central $M$, distancia $r$ y constante gravitacional $G$.

Ambas expresiones pertenecen a $U_g$ solo si determinan el mismo valor de $g$ dentro del mismo marco físico y con las mismas condiciones.

### Advertencia rigurosa

No es correcto afirmar sin condiciones que todas las expresiones con el símbolo $g$ pertenecen a la misma clase.

Solo pertenecen a $U_g$ aquellas que determinan exactamente el mismo valor fijado por el modelo.

---

## 11. Diferenciación e integración como procesos límite

La diferenciación y la integración aparecen en ES_49 como dos modos complementarios de operar con límites.

### 11.1 Diferenciación

La derivada se define mediante:

$$
f'(x)=
\lim_{dx\to0}
\frac{f(x+dx)-f(x)}{dx}.
$$

Este proceso toma una variación:

$$
dx
$$

y estudia su comportamiento cuando:

$$
dx\to0.
$$

La derivada expresa una razón instantánea de cambio.

### 11.2 Integración

La integral definida puede construirse como límite de sumas de Riemann:

$$
\int_a^b f(x)\,dx
=
\lim_{n\to\infty}
\sum_{k=1}^{n}
f(\xi_k)\Delta x_k.
$$

Aquí aparece una suma finita indexada por:

$$
k=1,2,\ldots,n.
$$

El paso al continuo se realiza mediante el refinamiento:

$$
n\to\infty
$$

y

$$
\max_k\Delta x_k\to0.
$$

Así, la integral une una estructura discreta de sumas con un objeto continuo de área o acumulación.

### 11.3 Teorema fundamental del cálculo

Si $f$ es continua en $[a,b]$ y se define:

$$
F(x)=\int_a^x f(t)\,dt,
$$

entonces:

$$
F'(x)=f(x)
$$

para todo $x\in(a,b)$.

Además, si $F$ es una primitiva de $f$, entonces:

$$
\int_a^b f(x)\,dx=F(b)-F(a).
$$

Este resultado conecta diferenciación e integración.

La diferenciación estudia la variación local.

La integración reconstruye la acumulación global.

En ES_49, esta relación refuerza la idea de que procesos aparentemente opuestos pueden ser compatibles dentro de una misma estructura.

---

## 12. Clases exactas y clases límite

Para evitar ambigüedad, conviene distinguir dos subfamilias:

$$
U_\alpha^{\mathrm{exacto}}
=
\left\{
A:\operatorname{valor}(A)=\alpha
\right\}
$$

y

$$
U_\alpha^{\mathrm{limite}}
=
\left\{
(A_n):\lim_{n\to\infty}A_n=\alpha
\right\}.
$$

Esta notación requiere cuidado.

Un proceso límite completo puede ser una expresión exacta de $\alpha$.

Pero los términos finitos del proceso no son, en general, expresiones exactas de $\alpha$.

Así:

$$
\lim_{n\to\infty}A_n\in U_\alpha^{\mathrm{exacto}}
$$

si el límite existe y vale $\alpha$.

Pero:

$$
A_n\notin U_\alpha^{\mathrm{exacto}}
$$

para un $n$ finito, salvo que por alguna razón particular $A_n=\alpha$.

Por eso puede escribirse de forma más fina:

$$
U_\alpha=
U_\alpha^{\mathrm{directo}}
\cup
U_\alpha^{\mathrm{limite}}
\cup
U_\alpha^{\mathrm{implicito}}
\cup
U_\alpha^{\mathrm{funcional}},
$$

donde las categorías pueden solaparse.

---

## 13. Generalización a $U_{f_i}$

Hasta ahora se han considerado constantes. Pero la idea puede generalizarse a funciones.

Sea $f_i:D\to C$ una función definida sobre un dominio $D$ con codominio $C$.

Definimos:

$$
U_{f_i}
=
\left\{
F_j:
\operatorname{valor}(F_j)=f_i
\right\},
$$

donde $\operatorname{valor}(F_j)=f_i$ significa que $F_j$ determina la misma función que $f_i$ sobre el dominio relevante.

Más explícitamente:

$$
F_j\in U_{f_i}
\iff
\forall x\in D,\ F_j(x)=f_i(x).
$$

Si se trabaja con funciones definidas casi en todas partes, distribuciones, clases de equivalencia de funciones o dominios restringidos, debe declararse el criterio de igualdad correspondiente.

### Ejemplo

Sea:

$$
f(x)=e^x.
$$

Entonces pertenecen a $U_f$:

$$
x\mapsto e^x,
$$

$$
x\mapsto \sum_{k=0}^{\infty}\frac{x^k}{k!},
$$

y la solución del problema diferencial:

$$
y'=y,
$$

$$
y(0)=1.
$$

Estas tres representaciones determinan la misma función sobre $\mathbb R$.

Por tanto, pertenecen a una misma clase $U_f$.

### Teorema 3 — Equivalencia funcional

Sea $D$ un dominio y sean $F,G:D\to C$. Si:

$$
\forall x\in D,\ F(x)=G(x),
$$

entonces $F$ y $G$ pertenecen a la misma clase de equivalencia funcional.

### Demostración

Por hipótesis, $F$ y $G$ tienen el mismo valor para cada punto de $D$.

Por tanto, determinan la misma función como relación entre elementos de $D$ y elementos de $C$.

Luego:

$$
F\sim_f G.
$$

Queda probado.

---

## 14. Teoremas y corolarios principales

### Teorema 4 — Invariante de valor

Sea $\alpha\in\mathbb R$. Si $A$ y $B$ son construcciones matemáticas bien definidas y:

$$
\operatorname{valor}(A)=\operatorname{valor}(B)=\alpha,
$$

entonces $A$ y $B$ son equivalentes respecto de $U_\alpha$.

### Demostración

Es inmediata por la definición de $\sim_\alpha$.

### Corolario 3 — Distinción de procedimiento

Dos expresiones pueden pertenecer a la misma clase $U_\alpha$ sin ser el mismo procedimiento.

### Demostración

La pertenencia a $U_\alpha$ exige igualdad de valor, no igualdad sintáctica ni igualdad de método.

Por tanto, si dos procedimientos distintos determinan $\alpha$, ambos pertenecen a $U_\alpha$ aunque sigan siendo procedimientos distintos.

### Corolario 4 — No equivalencia estructural de $\mathbb N$ y $\mathbb R$

La existencia de un nexo discreto-continuo para una constante $\alpha$ no implica que $\mathbb N$ y $\mathbb R$ sean equivalentes como estructuras.

### Demostración

Del hecho de que:

$$
\lim_{n\to\infty}a_n=\alpha
$$

y

$$
\lim_{dx\to0}Q(F,x,dx)=\alpha
$$

solo se sigue que ambas construcciones determinan el mismo valor $\alpha$.

No se sigue ninguna biyección estructural, homeomorfismo, isomorfismo de cuerpos, equivalencia de orden completo ni igualdad entre $\mathbb N$ y $\mathbb R$.

Por tanto, la conclusión válida es la pertenencia común a $U_\alpha$, no la identidad entre dominios.

---

## 15. Conjeturas y extensiones

Las siguientes ideas deben tratarse como conjeturas o programas de investigación, no como teoremas demostrados en este documento.

### Conjetura 1 — Crecimiento abierto de $U_\alpha^{\mathrm{conocido}}$

Para constantes matemáticamente ricas como $e$, $\pi$ y $\varphi$, el conjunto de expresiones conocidas que las determinan puede crecer indefinidamente con nuevos marcos, nuevas identidades y nuevas traducciones entre teorías.

Esto no afirma que $U_\alpha$ sea literalmente inagotable en todo lenguaje formal fijado.

Afirma que, desde la práctica matemática, el catálogo reconocido de expresiones puede ampliarse sin que el valor $\alpha$ cambie.

### Conjetura 2 — Nodos de compatibilidad

Constantes como $e$, $\pi$ y $\varphi$ pueden interpretarse como nodos de compatibilidad entre regiones distintas de la matemática.

Por ejemplo, $\pi$ conecta geometría, análisis, trigonometría, series e integración.

$e$ conecta crecimiento, cálculo diferencial, series, límites discretos y ecuaciones diferenciales.

$\varphi$ conecta álgebra, recurrencias, proporciones y límites de sucesiones.

Esta lectura es estructural y conceptual. No sustituye a las demostraciones particulares de cada identidad.

### Conjetura 3 — Extensión UNIHOLOG

En el marco UNIHOLOG, cada familia $U_{f_i}$ puede estudiarse como una red de expresiones equivalentes que revela conexiones entre dominios discretos, continuos, algebraicos, geométricos, dinámicos y físicos.

La parte demostrable consiste en verificar, caso por caso, que dos expresiones determinan el mismo objeto.

La parte conjetural consiste en interpretar la red completa como arquitectura de compatibilidad entre teorías.

---

## 16. Síntesis final

ES_49 no afirma que $\mathbb N$ y $\mathbb R$ sean lo mismo.

Afirma algo más sutil y matemáticamente defendible:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\alpha
\xleftarrow{\ dx\to0\ }
\mathbb R
$$

cuando existen construcciones discretas y continuas que determinan el mismo $\alpha\in\mathbb R$.

La constante $\alpha$ actúa como invariante.

La clase $U_\alpha$ reúne las expresiones que determinan ese mismo valor.

En el caso de $e$:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
e
\xleftarrow{\ dx\to0\ }
\mathbb R.
$$

En el caso de $\pi$:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\pi
\xleftarrow{\ \Delta x\to0\ }
\mathbb R.
$$

En el caso de $\varphi$:

$$
\mathbb N
\xrightarrow{\ n\to\infty\ }
\varphi
\xleftarrow{\ \mathrm{algebra}\ }
\mathbb R.
$$

En el caso general:

$$
U_{f_i}
=
\left\{
F_j:\forall x\in D,\ F_j(x)=f_i(x)
\right\}.
$$

La potencia de ES_49 está en distinguir cuidadosamente:

1. dominio de construcción;
2. procedimiento;
3. expresión;
4. proceso límite;
5. valor exacto;
6. clase de equivalencia;
7. interpretación conjetural.

Con esta separación, el puente entre discreto y continuo deja de ser una afirmación vaga y se convierte en una estructura rigurosa:

distintos caminos pueden conservar un mismo objeto.

Ese objeto común es el nexo.
