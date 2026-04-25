# Investigacion sobre el problema de Collatz

Fecha de cierre de esta ola: 2026-04-23 03:06:27 -03:00
Estado: primera ola cerrada
Resumen asociado: [ResumenInvestigacionSobreElProblemaDeCollatz.md](ResumenInvestigacionSobreElProblemaDeCollatz.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)

## 1. Que es el problema

La conjetura de Collatz parte de una regla extremadamente simple sobre enteros positivos:

- si `n` es par, se reemplaza por `n/2`;
- si `n` es impar, se reemplaza por `3n+1`.

La pregunta es si, empezando desde cualquier entero positivo, la iteracion siempre termina entrando en el ciclo `4 -> 2 -> 1`.

Tambien se lo llama problema `3n+1`, problema de Syracuse, problema de Ulam, problema de Kakutani o "hailstone problem". Fue formulado por Lothar Collatz en la decada de 1930 y seguia sin resolverse al 23 de abril de 2026.

## 2. Por que importa

El problema importa menos por una aplicacion directa y mas porque condensa una dificultad profunda: una dinamica definida por reglas minimas puede producir un comportamiento que parece aleatorio, altamente irregular y resistente a las herramientas habituales. Jeffrey Lagarias lo usa como ejemplo prototipico de un problema facil de formular y extraordinariamente dificil de resolver.

En otras palabras, Collatz es importante porque esta en el cruce de varias cosas:

- teoria de numeros;
- sistemas dinamicos discretos;
- combinatoria y dinamica simbolica;
- probabilidad y modelos estocasticos;
- teoria de la computacion;
- verificacion por computadora y automatizacion formal.

## 3. Reformulaciones utiles

Una reformulacion muy usada estudia la version "acelerada":

- `T(n) = n/2` si `n` es par;
- `T(n) = (3n+1)/2` si `n` es impar.

Esta version absorbe una division por 2 despues de cada paso impar y suele ser mas comoda para el analisis. Muchas publicaciones tecnicas trabajan con esta variante.

Tambien es comun mirar:

- el tiempo de parada: cuantos pasos tarda una orbita en bajar por primera vez por debajo del valor inicial;
- el tiempo total de parada: cuantos pasos tarda en llegar a `1`;
- la altura maxima o "maximum excursion": cuanto llega a subir antes de descender;
- el vector de paridades: la secuencia de pares e impares que va apareciendo;
- el arbol inverso: que numeros pueden llegar a un mismo nodo si se itera hacia atras.

Estas reformulaciones no resuelven el problema, pero organizan mejor el terreno.

## 4. Como se ve empiricamente

Empiricamente, las orbitas suelen tener dos rasgos a la vez:

- parecen caoticas a escala local;
- muestran una tendencia descendente en promedio a escala logaritmica.

Ese contraste explica buena parte de la fascinacion del problema. Una orbita puede subir muchisimo antes de bajar. El ejemplo clasico es `27`, cuya secuencia da muchisimos pasos antes de alcanzar `1` y pasa por valores bastante mayores que el inicial. Esto destruye cualquier intuicion monotona simple: no se puede probar la conjetura con un argumento ingenuo del tipo "casi siempre baja".

Segun la exposicion de Lagarias, los modelos probabilisticos sugieren tratar las paridades como si se comportaran aproximadamente como lanzamientos de moneda en ciertas escalas. Esa heuristica predice una pendiente descendente promedio en escala logaritmica y ayuda a explicar por que "casi todas" las orbitas parecen caer. Pero una heuristica no equivale a una prueba: lo dificil es controlar todas las orbitas, incluidas las excepcionales.

## 5. Lo que si se sabe con rigor

### 5.1. El problema sigue abierto

Al 23 de abril de 2026, la conjetura de Collatz no esta probada ni refutada. Si fuera falsa, tendria que ocurrir al menos una de estas dos cosas:

- existir una orbita divergente que nunca baje hasta `1`;
- existir un ciclo no trivial distinto de `4 -> 2 -> 1`.

Esa division en dos modos posibles de fallo es central para ordenar la investigacion.

### 5.2. Avance teorico mayor: Tao

El resultado moderno mas importante sigue siendo el de Terence Tao. El preprint aparecio en 2019 y la version publicada salio en 2022. El mensaje matematico fuerte es el siguiente, dicho en forma informal:

- para casi todos los enteros positivos, entendidos en el sentido de densidad logaritmica;
- la orbita de Collatz termina bajando por debajo de cualquier funcion `f(N)` que tienda a infinito, aunque lo haga lentisimo.

Esto no demuestra que todas las orbitas lleguen a `1`, pero si demuestra un descenso "masivo" para casi todos los casos. Es un resultado muy serio porque empuja el problema desde la intuicion probabilistica hacia un teorema riguroso de gran escala.

Lo importante es no sobredimensionarlo: Tao no probo la conjetura. Lo que logro fue demostrar una forma fuerte de descenso para casi todos los enteros, no para todos.

### 5.3. Frontera computacional: verificacion hasta `2^71`

La frontera computacional publicada mas fuerte que pude verificar para esta ola es la de David Barina. Su articulo de 2025 empuja la verificacion de la conjetura hasta `2^71`. Eso equivale aproximadamente a `2.36 x 10^21`.

Este punto merece una lectura muy precisa:

- "verificado hasta `2^71`" no significa "probado";
- significa que para todos los enteros positivos menores que ese limite, la orbita fue comprobada por computadora;
- por enorme que sea el rango, sigue siendo un conjunto finito;
- la conjetura pregunta por todos los enteros positivos, sin cota superior.

La conclusion correcta es: la evidencia computacional es gigantesca y favorable, pero todavia no sustituye una demostracion general.

### 5.4. Ciclos no triviales: cotas y obstrucciones

El frente de los ciclos no triviales tambien tuvo avances parciales importantes.

En 2023, Christian Hercher probo que no hay `m-cycles` con `m <= 91` en el sentido tecnico usado en ese trabajo. El articulo mejora cotas previas y muestra que, si existiera un ciclo no trivial, deberia ser bastante mas complejo de lo que ya estaba acotado antes.

En 2026, Kevin Knight publico "Collatz high cycles do not exist", donde elimina una familia relevante de "high cycles" dentro del estudio de ciclos racionales asociados al problema acelerado. Este resultado tampoco resuelve Collatz, pero reduce el espacio estructural en el que podria esconderse un ciclo no trivial.

La foto correcta del frente de ciclos es entonces:

- no se probo aun que no existan todos los ciclos no triviales;
- pero varias familias parciales y varias cotas minimas fueron descartadas con herramientas cada vez mas finas.

### 5.5. Automatizacion y pruebas asistidas

En 2023, Emre Yolcu, Scott Aaronson y Marijn Heule publicaron un trabajo que reformula el problema como una cuestion de terminacion de sistemas de reescritura. No probaron la conjetura completa, pero si mostraron una via automatizada interesante y lograron demostrar debilitamientos no triviales mediante tecnicas de termination proving.

Este frente importa porque indica algo clave: el problema no solo se esta atacando desde teoria de numeros clasica. Tambien se esta empujando desde:

- SAT/SMT y demostracion automatica;
- reescritura de terminos y terminacion;
- formalizacion mecanizada.

## 6. Lo que rodea al problema

Hablar de "todo lo relacionado" con Collatz obliga a abrir varios subcampos.

### 6.1. Modelos estocasticos

Una parte importante de la literatura construye modelos probabilisticos que imitan el comportamiento promedio de las orbitas. Estos modelos suelen predecir descenso en promedio para `3n+1` y comportamiento opuesto para variantes como `5n+1`. Son utiles para generar intuicion cuantitativa sobre tiempos de parada, maximas excursiones y distribuciones tipicas.

El limite de estos modelos es claro: describen muy bien lo comun, pero Collatz exige controlar lo extraordinario.

### 6.2. Generalizaciones

Hay muchisimos problemas de tipo Collatz: `an+b`, variantes por congruencias, mapas definidos por clases modulares, versiones aceleradas y extensiones a racionales, enteros negativos o reals. Estas generalizaciones no son una distraccion: ayudan a detectar que rasgos son especiales del caso `3n+1` y cuales pertenecen a una familia mas amplia.

Un dato importante de este ecosistema es que el problema generalizado de Collatz es indecidible en cierto sentido algoritimico. El resultado de Kurtz y Simon de 2007, apoyado en ideas previas de Conway, muestra que una generalizacion natural del problema ya entra en la zona de la indecidibilidad. Esto no demuestra que la conjetura clasica sea indecidible, pero si explica por que el paisaje conceptual es mas duro de lo que parece.

### 6.3. Estructuras 2-adicas y dinamica simbolica

Otra linea importante conecta Collatz con enteros 2-adicos, mapas de desplazamiento, conjugaciones y dinamica simbolica. Esta rama no es el foco de esta primera ola, pero aparece una y otra vez en encuestas serias porque ayuda a reorganizar el problema en espacios donde ciertas simetrias son mas visibles.

### 6.4. Versiones sobre otros dominios

Tambien hay trabajo sobre:

- enteros negativos, donde aparecen ciclos adicionales;
- racionales con denominador impar;
- analogos sobre la recta real;
- semigrupos y formulaciones algebraicas relacionadas.

Estas extensiones no prueban la conjetura original, pero sirven para entender que partes del fenomeno dependen de la aritmetica de los enteros positivos.

## 7. Por que el problema es tan dificil

Esta es la parte mas importante de la primera ola. Collatz no resiste porque sea enorme o tecnicamente rebuscado, sino porque mezcla propiedades enemigas:

- una regla local muy simple;
- un crecimiento ocasional muy fuerte debido a `3n+1`;
- reducciones frecuentes por divisiones entre `2`;
- una interaccion de paridades que parece pseudoaleatoria;
- ausencia visible de un invariante simple que fuerce la convergencia.

Si una orbita baja "en promedio", eso no basta. Habria que demostrar que ninguna orbita excepcional puede escapar indefinidamente ni cerrar un ciclo no trivial. Esa brecha entre promedio y universalidad es exactamente donde Collatz rompe los enfoques intuitivos.

Lagarias lo expresa bien en su panorama: buena parte de la dificultad parece residir en la incapacidad actual de analizar la naturaleza pseudoaleatoria de las iteraciones sucesivas.

## 8. Que hacer con la pagina de Wikipedia enlazada

La pagina en espanol que marcaste sirve bien como puerta de entrada. Pero para trabajar en serio conviene usarla con dos reservas:

- el propio articulo tenia aviso de estilo y de referencias adicionales colocado el 3 de septiembre de 2025;
- Wikipedia es util para orientarse, no para fijar el estado mas fino del problema.

La forma correcta de usarla en esta investigacion es como mapa inicial de nombres, ejemplos y terminologia, y luego pasar rapidamente a encuestas y articulos revisados por pares.

## 9. Estado actual sintetico al 23 de abril de 2026

- La conjetura clasica sigue abierta.
- El mejor avance teorico general de gran escala sigue siendo el de Tao sobre "casi todas" las orbitas.
- La mejor verificacion computacional publicada que pude confirmar llega a `2^71`.
- Se siguen mejorando cotas y exclusiones parciales de ciclos no triviales.
- La investigacion moderna esta repartida entre teoria de numeros, dinamica, computacion de alto rendimiento y metodos automatizados.
- El problema sigue generando muchisimo ruido bibliografico; por eso conviene separar encuestas serias y articulos revisados por pares de preprints o "pruebas" no validadas.

## 10. Recomendacion para la segunda ola

La siguiente ola deberia dividirse en una de estas rutas:

- Ruta A: historia formal y resultados clasicos hasta Lagarias.
- Ruta B: Tao, densidad logaritmica y por que su resultado es fuerte pero insuficiente.
- Ruta C: ciclos no triviales, cotas, racionales, high cycles y familia de obstrucciones.
- Ruta D: verificacion computacional, algoritmos, HPC y records de trayectorias.
- Ruta E: generalizaciones, indecidibilidad y relacion con FRACTRAN.
- Ruta F: automatizacion, SAT, termination proving y formalizacion actual.

## Fuentes base usadas en esta ola

- Wikipedia en espanol, como puerta de entrada y referencia de terminologia: <https://es.wikipedia.org/wiki/Conjetura_de_Collatz>
- Jeffrey C. Lagarias, "The 3x+1 Problem: An Overview" (arXiv / AMS): <https://arxiv.org/abs/2111.02635>
- Version HTML navegable del panorama de Lagarias: <https://ar5iv.labs.arxiv.org/html/2111.02635>
- Terence Tao, "Almost all orbits of the Collatz map attain almost bounded values" (publicado en 2022; preprint 2019): <https://doi.org/10.1017/fmp.2022.8>
- Version arXiv del trabajo de Tao: <https://arxiv.org/abs/1909.03562>
- David Barina, "Improved verification limit for the convergence of the Collatz conjecture" (2025): <https://doi.org/10.1007/s11227-025-07337-0>
- Proyecto de verificacion computacional de Barina: <https://pcbarina.fit.vutbr.cz/>
- Christian Hercher, "There are no Collatz m-Cycles with m <= 91" (2023): <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html>
- Emre Yolcu, Scott Aaronson, Marijn J. H. Heule, "An Automated Approach to the Collatz Conjecture" (2023): <https://doi.org/10.1007/s10817-022-09658-8>
- S. A. Kurtz y J. Simon, "The undecidability of the generalized Collatz problem" (2007): <https://doi.org/10.1007/978-3-540-72504-6_49>
- Kevin Knight, "Collatz high cycles do not exist" (2026): <https://doi.org/10.1016/j.disc.2025.114812>
- Collatz Conjecture Challenge, esfuerzo de formalizacion de literatura: <https://ccchallenge.org/>
