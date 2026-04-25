# Investigacion sobre el problema de Collatz - Segunda Ola

Fecha de cierre de esta ola: 2026-04-23 06:20:00 -03:00
Estado: segunda ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzSegundaOla.md](ResumenInvestigacionSobreCollatzSegundaOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [InvestigacionSobreElProblemaDeCollatz.md](InvestigacionSobreElProblemaDeCollatz.md)

---

## 1. Objetivo de esta ola

La primera ola cubrio un panorama amplio: enunciado, historia basica, estado actual, resultados parciales y lineas de trabajo. Esta segunda ola profundiza en cada subfrente con detalle tecnico, cubriendo las seis rutas propuestas al cierre de la primera ola:

- Ruta A: historia formal y resultados clasicos.
- Ruta B: el resultado de Tao en detalle.
- Ruta C: ciclos no triviales y cotas.
- Ruta D: verificacion computacional.
- Ruta E: generalizaciones, indecidibilidad y FRACTRAN.
- Ruta F: automatizacion, SAT y termination proving.

Ademas se agregan dos rutas nuevas:

- Ruta G: modelos estocasticos y heuristicas probabilisticas.
- Ruta H: analisis 2-adico y dinamica simbolica.

---

## 2. Ruta A: Historia formal y difusion del problema

### 2.1. Origen

Lothar Collatz concibio el problema alrededor de 1937, dos anos despues de recibir su doctorado. Mientras estudiaba en Gottingen, Collatz se intereso por la representacion grafica de la iteracion de funciones aritmeticas. En sus cuadernos de los anos 1930 aparecen iteraciones de funciones similares, y probablemente en esa epoca formulo la variante especifica `3n+1`.

### 2.2. Difusion y nombres multiples

El problema adquirio multiples nombres a medida que circulaba por la comunidad matematica:

- **Problema de Syracuse**: Helmut Hasse y Shizuo Kakutani lo llevaron a la Universidad de Syracuse en la decada de 1950. Kakutani lo difundio en Yale y Chicago, donde conto que "durante un mes, todos en Yale trabajaron en el problema sin resultado. Un fenomeno similar ocurrio cuando lo mencione en la Universidad de Chicago. Se hizo el chiste de que el problema era parte de una conspiracion para frenar la investigacion matematica en Estados Unidos."

- **Conjetura de Ulam**: Stanislaw Ulam discutio el problema en los anos 1960, contribuyendo a su difusion.

- **Problema de Kakutani**: por el propio Shizuo Kakutani, quien lo popularizo internacionalmente.

- **Problema de Hailstone** (granizo): por la forma en que las orbitas suben y bajan como piedras de granizo antes de caer.

- Bryan Thwaites, matematico britanico, ofrecio un premio temprano en los anos 1980 por una prueba o contraejemplo.

### 2.3. Encuesta de Lagarias

Jeffrey C. Lagarias publico la encuesta de referencia mas importante del problema: "The 3x+1 Problem: An Overview" (arXiv: 2111.02635, publicada por la AMS). Esta encuesta cubre la historia, resultados conocidos, modelos probabilisticos, generalizaciones y la pregunta central: como puede ser tan dificil un problema tan facil de enunciar. Lagarias identifica la pseudoaleatoriedad de las iteraciones sucesivas como la fuente principal de la dificultad.

---

## 3. Ruta B: El resultado de Tao en detalle

### 3.1. Enunciado preciso

Terence Tao probo el siguiente teorema (preprint 2019, publicado en Forum of Mathematics, Pi, 2022):

> Para cualquier funcion `f : N+ -> R` con `lim f(N) = +infinito`, se tiene que `Col_min(N) <= f(N)` para casi todos los `N` en el sentido de densidad logaritmica.

Esto significa, por ejemplo, que `Col_min(N) < log log log log N` para casi todos los `N`.

Una formulacion equivalente: para todo `delta > 0`, existe una constante `C_delta` tal que `Col_min(N) <= C_delta` para todos los `N` en un subconjunto de densidad logaritmica inferior al menos `1 - delta`. Los argumentos dan una constante del orden `C_delta ~ exp(delta^{-O(1)})`.

### 3.2. Estrategia de la prueba

La prueba establece una propiedad de transporte aproximado para una cierta variable aleatoria de primer paso asociada con la iteracion de Collatz (o la iteracion de Syracuse estrechamente relacionada). Esta propiedad se obtiene de la estimacion de la funcion caracteristica de un cierto paseo aleatorio sesgado sobre un grupo ciclico 3-adico en frecuencias altas. La estimacion se logra estudiando como un cierto proceso de renovacion bidimensional interactua con una union de triangulos asociados a una frecuencia dada.

### 3.3. Que prueba y que no prueba

Lo que SI prueba:
- Un descenso masivo para una fraccion abrumadora de los enteros positivos.
- Que la intuicion probabilistica del descenso es correcta en un sentido riguroso para "casi todos" los casos.
- Que el minimo orbital puede hacerse tan pequeno como se quiera para densidad logaritmica cercana a 1.

Lo que NO prueba:
- Que TODAS las orbitas llegan a 1.
- Que no existen orbitas divergentes.
- Que no existen ciclos no triviales.

La barrera: el resultado usa densidad logaritmica, no densidad natural. Y "casi todos" sigue dejando fuera un conjunto potencialmente infinito de excepciones (aunque de densidad cero).

### 3.4. Relacion con la heuristica probabilistica

Tao convierte una heuristica clasica en un teorema riguroso. La heuristica dice que las paridades se comportan aproximadamente como lanzamientos de moneda, lo que predice un drift descendente. Tao logra hacer rigurosa esta intuicion para casi todos los enteros, pero el salto a "todos" requiere controlar las correlaciones finas entre pasos sucesivos, algo que sus tecnicas no alcanzan.

---

## 4. Ruta C: Ciclos no triviales, cotas y obstrucciones

### 4.1. Contexto

Si la conjetura de Collatz fuera falsa, una de las dos formas posibles de fallo es la existencia de un ciclo no trivial: una orbita que vuelve a si misma sin pasar por `4 -> 2 -> 1`. El trabajo en este frente busca demostrar que tales ciclos no pueden existir, o al menos elevar las cotas minimas que deberian satisfacer.

### 4.2. m-cycles y el resultado de Hercher (2023)

Un "m-cycle" es un ciclo que contiene exactamente `m` numeros impares. Los resultados previos de Simons y de Weger habian probado que `m >= 76`. Con verificacion computacional adicional, se sabia que `m >= 83`.

Christian Hercher (Europa-Universitat Flensburg) probo en 2023 que no existen m-cycles con `m <= 91`, publicado en el Journal of Integer Sequences, Vol. 26, Article 23.3.5. El resultado eleva significativamente la cota y muestra que, si un ciclo no trivial existiera, deberia contener al menos 92 numeros impares.

Un punto tecnico importante del trabajo de Hercher: demostro que para elevar la cota a `K >= 1.375 x 10^11`, basta con verificar que todo entero menor o igual a `1536 x 2^60 = 3 x 2^69` entra en el ciclo trivial. Esto reduce el rango de numeros a verificar en casi un 60%.

### 4.3. High cycles y el resultado de Knight (2026)

Kevin Knight publico "Collatz high cycles do not exist" en Discrete Mathematics, Vol. 349(3), articulo 114812, en marzo de 2026.

El resultado principal: no existen "high cycles" de enteros positivos, extendiendo resultados previos sobre circuitos. El paper usa vectores de paridad y propiedades de palabras de Christoffel para caracterizar y eliminar la posibilidad de estos ciclos.

Un resultado cuantitativo importante del paper: cualquier orbita ciclica no trivial bajo la iteracion de Collatz debe contener al menos 17,087,915 elementos.

### 4.4. Panorama actual del frente de ciclos

- No se ha probado la inexistencia total de ciclos no triviales.
- Pero las cotas minimas son enormes: al menos 92 impares, al menos ~17 millones de elementos totales.
- Varias familias estructurales (m-cycles bajos, high cycles, ciertas familias racionales) han sido descartadas.
- El espacio donde podria esconderse un ciclo no trivial se sigue reduciendo.

---

## 5. Ruta D: Verificacion computacional

### 5.1. Estado actual: Barina y la frontera en 2^71

David Barina (Brno University of Technology) publico "Improved verification limit for the convergence of the Collatz conjecture" en The Journal of Supercomputing (2025). La verificacion alcanza `2^71`, aproximadamente `2.36 x 10^21`.

### 5.2. Metodologia

- Algoritmos altamente optimizados para CPU y GPU.
- La aceleracion total desde el primer algoritmo en CPU hasta el mejor algoritmo en GPU es de 1,335x.
- Distribucion de tareas a miles de workers paralelos ejecutandose en varios supercomputadores europeos.
- Durante la verificacion de convergencia, el programa tambien busca records de trayectoria, y se encontraron cuatro nuevos path records.

### 5.3. Que significa y que no

Verificado hasta `2^71` significa:
- Para todo entero positivo menor que `2^71`, la orbita de Collatz fue computada y se confirmo que llega a 1.
- Es evidencia empirica gigantesca y favorable.

Verificado hasta `2^71` NO significa:
- Una demostracion general. El conjunto verificado es finito; la conjetura pregunta por infinitos enteros.
- Que no pueda existir un contraejemplo mas alla de `2^71`.

### 5.4. Frontera historica de verificacion

La frontera ha ido creciendo exponencialmente:
- Oliveira e Silva llego a `5.76 x 10^18` (~2^62.5) en 2009.
- Barina alcanzo `2^68` en 2020 (publicado en Journal of Supercomputing).
- Barina alcanzo `2^71` en 2025 (articulo actualizado).

Cada salto requiere mejoras algoritmicas, no solo mas potencia de computo.

### 5.5. Suficiencia recursiva

Un resultado reciente (Notes on Number Theory and Discrete Mathematics, Vol. 31, 2025) explora la suficiencia recursiva para la conjetura de Collatz, buscando maneras de reducir el rango efectivo de numeros que necesitan ser verificados, complementando la verificacion exhaustiva.

---

## 6. Ruta E: Generalizaciones, indecidibilidad y FRACTRAN

### 6.1. El problema generalizado

El problema de Collatz puede generalizarse a funciones del tipo `f(n)` definidas por clases de congruencia: para n en cierta clase modular, se aplica una transformacion lineal especifica. La version clasica `3n+1` es solo un caso particular.

### 6.2. Conway y FRACTRAN

En 1972, John Horton Conway demostro que una generalizacion natural del problema de Collatz es algoritmicamente indecidible. Conway lo hizo a traves de FRACTRAN, un lenguaje de programacion minimalista que es Turing-completo: cualquier maquina de Turing puede ser simulada por un programa FRACTRAN.

La conexion clave: Conway mostro que la pregunta "dado un programa FRACTRAN F y un numero N, la orbita contiene alguna vez una potencia de 2?" es indecidible (equivalente al problema de la detencion).

### 6.3. Kurtz y Simon (2007)

Stuart A. Kurtz y Janos Simon (Universidad de Chicago) extendieron el resultado de Conway. Probaron que el problema universalmente cuantificado (es decir, "dado g, la secuencia g^k(n) alcanza 1 para todo n > 0?") es indecidible. Mas precisamente, es Pi-2-0-completo.

### 6.4. Que implica para Collatz clasico

Que el problema generalizado sea indecidible NO implica que la conjetura clasica `3n+1` sea indecidible. La indecidibilidad se refiere a la clase completa de funciones tipo Collatz, no a una instancia particular. Sin embargo, explica algo profundo: la estructura del paisaje conceptual es mucho mas dura de lo que la simplicidad de la regla sugiere. No puede existir un metodo general que resuelva todas las variantes.

### 6.5. La variante 5n+1

La variante `5n+1` es un caso instructivo. A diferencia de `3n+1`, en `5n+1` se observan tres ciclos distintos y al menos una secuencia (la que empieza en 11, pasando por 7 y 9) que exhibe crecimiento ilimitado. Esto sugiere divergencia genuina.

La razon heuristica: en `3n+1`, el factor de crecimiento promedio por paso impar es `3/4` (se multiplica por 3 y luego se divide al menos una vez por 2), lo que da un drift descendente. En `5n+1`, el factor promedio es `5/4`, que da drift ascendente. La conjetura de Collatz "funciona" para `3n+1` porque el multiplicador esta justo por debajo del umbral critico.

### 6.6. Enteros negativos

Si se extiende la funcion de Collatz a enteros negativos, aparecen ciclos adicionales. Se conocen al menos tres ciclos negativos ademas del ciclo trivial en 0:

- El ciclo que contiene -1 (analogo al ciclo 4-2-1 positivo).
- Ciclos que contienen -5 y -17.
- Otro ciclo adicional.

La existencia de multiples ciclos en el dominio negativo contrasta fuertemente con el caso positivo, donde solo se conoce el ciclo trivial. Esto sugiere que las propiedades aritmeticas especificas de los enteros positivos juegan un papel crucial.

---

## 7. Ruta F: Automatizacion, SAT y termination proving

### 7.1. El trabajo de Yolcu, Aaronson y Heule (2023)

Emre Yolcu, Scott Aaronson y Marijn J. H. Heule publicaron "An Automated Approach to the Collatz Conjecture" en el Journal of Automated Reasoning (2023).

### 7.2. Idea central

El enfoque reformula el problema de Collatz como un problema de terminacion de sistemas de reescritura de cadenas. Construyen un sistema de reescritura que simula la aplicacion iterada de la funcion de Collatz sobre cadenas que corresponden a representaciones binario-ternarias mixtas de enteros positivos. Prueban que la terminacion de este sistema de reescritura es equivalente a la conjetura de Collatz.

### 7.3. Tecnicas usadas

- SAT solvers (satisfiability solvers): programas que determinan si existe una solucion para una formula dada un conjunto de restricciones.
- Interpretaciones matriciales naturales y articas para probar terminacion.
- Un demostrador de terminacion minimo implementado ad hoc.

### 7.4. Resultados

No prueban la conjetura completa, pero si demuestran debilitamientos no triviales de la misma de forma automatica. El valor principal esta en abrir un camino donde herramientas de logica automatica puedan capturar partes crecientes del fenomeno.

Aaronson y Heule trabajaron en este enfoque durante cinco anos. Segun sus propias palabras: "Aunque no logramos probar la conjetura de Collatz, creemos que las ideas aqui presentadas representan un nuevo enfoque interesante."

### 7.5. Significado para el futuro

Este frente indica que Collatz ya no se ataca solo desde la teoria de numeros clasica. Tambien se empuja desde:

- SAT/SMT y demostracion automatica.
- Reescritura de terminos y terminacion.
- Formalizacion mecanizada.
- Esfuerzos como el Collatz Conjecture Challenge (ccchallenge.org), que busca formalizar la literatura existente.

---

## 8. Ruta G: Modelos estocasticos y heuristicas probabilisticas

### 8.1. El modelo clasico

La heuristica probabilistica basica trata a la secuencia de paridades en una orbita de Collatz como si fueran aproximadamente independientes y uniformes: cada numero tiene probabilidad 1/2 de ser par y 1/2 de ser impar.

Bajo este modelo:
- Si `n` es par, se divide por 2 (factor multiplicativo: 1/2).
- Si `n` es impar, pasa a `(3n+1)/2` en la version acelerada (factor multiplicativo: ~3/2).
- El factor promedio por paso es `(1/2)^{1/2} x (3/2)^{1/2} = sqrt(3/4) ~ 0.866`.
- Como este factor es menor que 1, el modelo predice un drift descendente en escala logaritmica.

### 8.2. Predicciones cuantitativas

Los modelos estocasticos predicen:
- Que todas las orbitas convergen a un conjunto acotado.
- Que el tiempo total de parada para un punto de partida aleatorio deberia ser aproximadamente `6.95212 x log(n)` pasos.
- Que la distribucion de tiempos de parada alrededor de ese valor medio es aproximadamente gaussiana cuando `n` tiende a infinito.

### 8.3. El resultado de Terras

Riho Terras probo que casi todos los enteros positivos tienen un tiempo de parada finito (es decir, la orbita baja por primera vez por debajo del valor inicial en un numero finito de pasos). La prueba se basa en la distribucion de vectores de paridad y usa el teorema del limite central.

### 8.4. Comportamiento estocastico observado

Investigacion reciente (Journal of Physics: Complexity, 2024) confirma que las orbitas de Collatz exhiben propiedades globales de movimiento browniano geometrico. Tests de criptografia, espectro de potencias, fluctuacion sin tendencia, autocorrelacion y medidas de entropia confirman este comportamiento estocasitico.

### 8.5. Limites del enfoque

El limite fundamental de los modelos estocasticos es claro: describen muy bien el comportamiento tipico, pero Collatz exige controlar lo extraordinario. Que las orbitas bajen "en promedio" o "casi todas" no resuelve el problema. La conjetura pide convergencia universal.

Ademas, se ha observado que potencias de 3, 7, 19 y 53 presentan una distribucion de tiempos de parada tipo ley de potencias, lo que contradice los modelos puramente probabilisticos y abre vias para enfoques estructurales.

### 8.6. La variante 5n+1 como test del modelo

Los modelos estocasticos predicen correctamente que `5n+1` deberia divergir (porque el factor promedio `sqrt(5/4) > 1`), y efectivamente se observan orbitas divergentes. Esto da confianza al modelo en general, pero no lo valida como prueba para `3n+1`.

---

## 9. Ruta H: Analisis 2-adico y dinamica simbolica

### 9.1. Extension a los enteros 2-adicos

La funcion de Collatz se extiende naturalmente al anillo Z_2 de los enteros 2-adicos, donde es continua y preserva la medida 2-adica. Mas aun, la dinamica en Z_2 es ergodica.

### 9.2. Ciclos fantasma

En los enteros 2-adicos existen puntos periodicos de la funcion de Collatz que no corresponden a orbitas periodicas en los enteros positivos. Estos "ciclos fantasma" son algebraicamente validos en Z_2 pero no se manifiestan como soluciones enteras. La distincion entre ciclos genuinos y ciclos fantasma es uno de los desafios centrales de este enfoque.

### 9.3. Limitaciones logicas (2025-2026)

Trabajo reciente (arXiv: 2601.12772, enero 2026) demuestra obstrucciones 2-adicas a la caracterizacion de ciclos de Collatz en aritmetica de Presburger. Las soluciones 2-adicas fallan en ser semilineales y por lo tanto no son definibles en aritmetica de Presburger. Esto significa que los enfoques que intentan distinguir ciclos enteros genuinos de ciclos fantasma 2-adicos usando solo aritmetica lineal o automatas finitos son inherentemente insuficientes.

Un resultado aun mas reciente (arXiv: 2602.06066, febrero 2026) establece "limites semanticos del razonamiento existencial positivo en dinamica aritmetica", reforzando que ciertas clases de argumentos algebraicos no pueden resolver el problema.

### 9.4. Dinamica simbolica

Una formulacion en dinamica simbolica representa la funcion de Collatz usando mapas de desplazamiento con enteros representados en base 2 o base 3. La intuicion es que el mapeo deberia ser describible usando shift maps. Esta reformulacion conecta Collatz con la teoria ergodica y la codificacion simbolica, y permite importar herramientas de esos campos.

### 9.5. Arbol inverso y representacion binaria

El arbol inverso de Collatz comienza en la raiz 1 y explora todos los valores predecesores posibles usando operaciones inversas. El analisis de este arbol revela propiedades estructurales a traves de representaciones binarias:

- Los numeros naturales se categorizan en tres subconjuntos: numeros puramente impares, puramente pares y mixtos.
- La transformacion `3n+1` puede analizarse en terminos de su efecto sobre los digitos binarios.
- La convergencia de la secuencia parece estar guiada por propiedades intrinsecas de las operaciones binarias.

---

## 10. Intentos de prueba recientes (2024-2026)

### 10.1. Contexto

El problema de Collatz genera un volumen enorme de "pruebas" publicadas en repositorios abiertos (arXiv, Preprints.org, Academia.edu, figshare, Zenodo). La gran mayoria no han pasado revision por pares rigurosa y no son aceptadas por la comunidad matematica.

### 10.2. Algunos intentos notables

- Un paper en Contemporary Mathematics (Taylor & Francis, 2025) presenta una "prueba estructural indirecta" via el arbol de Collatz.
- Varios preprints en 2025-2026 afirman probar la conjetura por analisis de secuencias acotadas, unicidad de ciclos, o entropia termodinamica.
- Un preprint en Zenodo (2026) afirma una prueba completa.

### 10.3. Criterio correcto

Al dia de hoy (abril 2026), ningun intento de prueba completa ha sido aceptado por la comunidad matematica despues de revision por pares. La regla practica que sugiere Lagarias es priorizar encuestas serias y articulos en revistas revisadas por pares por sobre preprints aislados.

---

## 11. Por que Collatz sigue siendo tan dificil: sintesis ampliada

### 11.1. La mezcla de propiedades enemigas

Collatz no es dificil por ser grande o tecnicamente rebuscado. Es dificil porque mezcla propiedades que se resisten mutuamente:

- Una regla local minima (par/impar).
- Crecimiento ocasional fuerte (`3n+1` puede elevar bastante).
- Reducciones frecuentes (divisiones por 2).
- Interaccion de paridades pseudoaleatoria.
- Ausencia de un invariante simple que fuerce convergencia.
- Indecidibilidad del problema general (no se puede atacar con un metodo universal).

### 11.2. La brecha entre promedio y universalidad

La evidencia probabilistica dice: "en promedio, las orbitas bajan". Tao formalizo esto como un teorema para "casi todos". Pero "casi todos" no es "todos". La conjetura pide convergencia para cada entero, sin excepcion. Esa brecha entre comportamiento tipico y comportamiento universal es exactamente donde vive la dificultad.

### 11.3. Barreras logicas

Los resultados de 2-adicos y Presburger muestran que ciertas familias de argumentos algebraicos son inherentemente insuficientes. Esto no dice que Collatz sea indecidible en ZFC, pero si que muchos enfoques "naturales" tienen techos estructurales.

---

## 12. Estado sintetico al 23 de abril de 2026

- La conjetura clasica sigue abierta.
- Mejor avance teorico general: Tao (2019/2022), casi todas las orbitas descienden masivamente.
- Mejor verificacion computacional: Barina (2025), hasta `2^71`.
- Ciclos: m-cycles descartados hasta `m <= 91` (Hercher, 2023); high cycles descartados (Knight, 2026); cota minima de ~17 millones de elementos para un ciclo no trivial.
- Modelos estocasticos: confirman drift descendente, predicen tiempo de parada ~6.95 log(n), pero no prueban universalidad.
- Automatizacion: SAT/termination proving (Yolcu-Aaronson-Heule, 2023) abre caminos pero no resuelve.
- 2-adicos: obstrucciones logicas demostradas (2026), limitando ciertos enfoques.
- Generalizaciones: problema generalizado indecidible (Conway/Kurtz-Simon), 5n+1 muestra divergencia.
- Ninguna prueba completa aceptada por la comunidad.

---

## 13. Recomendacion para la tercera ola

La tercera ola podria profundizar en:

- Ruta I: analisis detallado del paper de Tao, tecnicas de paseo aleatorio 3-adico.
- Ruta J: formalizacion mecanizada y estado del Collatz Conjecture Challenge.
- Ruta K: la conexion con la conjetura de Erdos-Straus y otros problemas abiertos relacionados.
- Ruta L: analisis de la estructura del arbol inverso con herramientas de teoria de grafos.
- Ruta M: comparacion sistematica de variantes (3n+1, 5n+1, 7n+1) y umbrales criticos.
- Ruta N: conexiones con teoria ergodica y medida de Haar en Z_2.

---

## Fuentes usadas en esta ola

- Terence Tao, "Almost all orbits of the Collatz map attain almost bounded values": <https://arxiv.org/abs/1909.03562>
- Blog de Tao sobre el resultado: <https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/>
- Version publicada (Forum of Mathematics, Pi, 2022): <https://doi.org/10.1017/fmp.2022.8>
- Charla de Tao, "The Notorious Collatz conjecture": <https://terrytao.files.wordpress.com/2020/02/collatz.pdf>
- Christian Hercher, "There are no Collatz m-Cycles with m <= 91" (JIS, 2023): <https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html>
- Kevin Knight, "Collatz high cycles do not exist" (Discrete Mathematics, 2026): <https://doi.org/10.1016/j.disc.2025.114812>
- Preprint de Knight (HAL, 2023): <https://hal.science/hal-04261183/document>
- David Barina, "Improved verification limit..." (J. Supercomputing, 2025): <https://doi.org/10.1007/s11227-025-07337-0>
- Proyecto de verificacion de Barina: <https://pcbarina.fit.vutbr.cz/>
- David Barina, "Convergence verification of the Collatz problem" (J. Supercomputing, 2020): <https://doi.org/10.1007/s11227-020-03368-x>
- Jeffrey C. Lagarias, "The 3x+1 Problem: An Overview": <https://arxiv.org/abs/2111.02635>
- Yolcu, Aaronson, Heule, "An Automated Approach to the Collatz Conjecture" (JAR, 2023): <https://doi.org/10.1007/s10817-022-09658-8>
- Preprint arXiv: <https://arxiv.org/abs/2105.14697>
- Presentacion Simons Institute: <https://simons.berkeley.edu/talks/sat-math>
- MIT Technology Review sobre el enfoque: <https://www.technologyreview.com/2021/07/02/1027475/computers-ready-solve-this-notorious-math-problem/>
- Kurtz y Simon, "The Undecidability of the Generalized Collatz Problem" (2007): <https://doi.org/10.1007/978-3-540-72504-6_49>
- PDF del articulo: <https://people.cs.uchicago.edu/~simon/RES/collatz.pdf>
- Conway y FRACTRAN: <https://raganwald.com/2020/05/03/fractran.html>
- Alex V. Kontorovich, "Stochastic Models for the 3x+1 and 5x+1 Problems": <https://arxiv.org/pdf/0910.1944>
- Stochastic-like characteristics (J. Phys. Complexity, 2024): <https://doi.org/10.1088/2632-072X/ad271f>
- Blog de Tao sobre Littlewood-Offord y Collatz: <https://terrytao.wordpress.com/2011/08/25/the-collatz-conjecture-littlewood-offord-theory-and-powers-of-2-and-3/>
- Obstrucciones 2-adicas (arXiv, 2026): <https://arxiv.org/html/2601.12772>
- Limites semanticos (arXiv, 2026): <https://arxiv.org/html/2602.06066>
- Extension 2-adica (Karger, U. Chicago): <https://www.math.uchicago.edu/~may/VIGRE/VIGRE2011/REUPapers/Karger.pdf>
- Formulacion simbolica (arXiv, 2024): <https://arxiv.org/html/2403.19699>
- Suficiencia recursiva (NNTDM, 2025): <https://nntdm.net/volume-31-2025/number-3/471-480/>
- Wikipedia en espanol: <https://es.wikipedia.org/wiki/Conjetura_de_Collatz>
- Wikipedia en ingles: <https://en.wikipedia.org/wiki/Collatz_conjecture>
- Collatz Conjecture Challenge: <https://ccchallenge.org/>
- Barina, "7x +/- 1" (variantes): <https://arxiv.org/pdf/1807.00908>
