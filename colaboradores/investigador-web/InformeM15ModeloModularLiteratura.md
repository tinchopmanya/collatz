# Informe CodexInvestigadorWeb

Fecha: 2026-04-25
Tema: M15 - modelo modular 2-adico vs modelo geometrico independiente
Pregunta: si `P(next_tail | q mod 8)` ya aparece en la literatura de Collatz como mejora predictiva de supervivencia orbital, stopping time o blocks_to_descend frente al modelo geometrico independiente.

## Respuesta corta

Existe en la literatura?

Parcialmente. La parte matematica de condicionar por residuos modulo potencias de 2, parity vectors/parity sequences, stopping time y cadenas odd-to-odd esta muy establecida desde Terras y Everett. Tambien existe el modelo geometrico/aleatorio de las valuaciones `v2(3n+1)` y modelos estocasticos para stopping time/total stopping time.

No encontre una comparacion explicita equivalente a M15: un modelo empirico `P(next_tail | q mod 8)` contra un baseline geometrico independiente para predecir supervivencia orbital, stopping time o blocks_to_descend.

Desde cuando?

Desde 1976-1977 para stopping time, parity vectors y clases de congruencia modulo `2^k` (Terras, Everett). Desde al menos 1985 la relacion con modelos probabilisticos, mezcla 2-adica y stopping time esta sintetizada por Lagarias. Los modelos estocasticos mas formales aparecen en Lagarias-Weiss (1992) y luego en Kontorovich-Lagarias (2009/2010).

Con que nombre aparece?

- parity vector, parity sequence, symbolic dynamics
- congruence classes modulo `2^k`, residue classes
- coefficient stopping time, stopping time, total stopping time
- accelerated 3x+1 map / Syracuse map / odd-to-odd map
- `o-sequence` o valuation sequence: los exponentes `o_i = ord_2(3n_i+1)`
- 2-adic extension, 2-adic shift, conjugacy to the shift
- stochastic models: MRP, BRW, RRW, branching random walk, Markov chains

Nivel de novedad estimado:

Bajo como fenomeno matematico local: `q mod 8` es un cilindro/residuo 2-adico muy pequeno, y el hecho de que prediga el siguiente patron de paridad/valuacion es esperable.

Medio-bajo como experimento aplicado del proyecto: no encontre la ablation exacta `P(next_tail | q mod 8)` vs geometrico independiente con metrica de supervivencia/stopping/blocks_to_descend. Parece una reformulacion experimental util de ingredientes conocidos, no evidencia fuerte de una idea teorica nueva.

## Fuentes revisadas

- Fuente: Riho Terras, "A stopping time problem on the positive integers"
- Tipo: paper primario, Acta Arithmetica 30 (1976), 241-252
- Fecha: 1976
- Link: https://eudml.org/doc/205476 ; https://doi.org/10.4064/aa-30-3-241-252
- Relevancia: origen clasico del stopping time y coefficient stopping time. Usa parity vectors y clases de congruencia modulo `2^k` para contar densidades de enteros con stopping time finito.

- Fuente: C. J. Everett, "Iteration of the number-theoretic function f(2n)=n, f(2n+1)=3n+2"
- Tipo: paper primario, Advances in Mathematics 25 (1977), 42-45
- Fecha: 1977
- Link: https://doi.org/10.1016/0001-8708(77)90087-1
- Relevancia: resultado independiente tipo "almost all" para descenso; aparece junto a Terras en los surveys como base del tratamiento por vectores de paridad.

- Fuente: Jeffrey C. Lagarias, "The 3x+1 problem and its generalizations"
- Tipo: survey, American Mathematical Monthly 92 (1985), 3-23
- Fecha: 1985
- Link: https://www.cecm.sfu.ca/organics/papers/lagarias/ ; seccion parity/stopping: https://www.cecm.sfu.ca/organics/papers/lagarias/paper/html/node4.html
- Relevancia: explica explicitamente que los primeros `k` iterados quedan descritos por el parity vector, que Terras invierte esa descripcion en clases de congruencia modulo `2^k`, y que el problema central es entender propiedades de mezcla para potencias de 2.

- Fuente: Jeffrey C. Lagarias and A. Weiss, "The 3x+1 Problem: Two Stochastic Models"
- Tipo: paper primario, Annals of Applied Probability 2 (1992), 229-261
- Fecha: 1992
- Link: https://doi.org/10.1214/aoap/1177005779
- Relevancia: modelos estocasticos y Markov/branching para predicciones de trayectorias y arboles inversos. Es el antecedente mas cercano a comparar modelos probabilisticos, aunque no encontre una comparacion `q mod 8` vs geometrico independiente.

- Fuente: Alex V. Kontorovich and Jeffrey C. Lagarias, "Stochastic Models for the 3x+1 and 5x+1 Problems"
- Tipo: survey/paper, arXiv y capitulo en The Ultimate Challenge
- Fecha: 2009/2010
- Link: https://arxiv.org/abs/0910.1944
- Relevancia: formaliza modelos MRP/BRW/RRW/branching random walk; define el mapa acelerado `U(n)=(3n+1)/2^{ord_2(3n+1)}` sobre impares; muestra que las `o-sequences` tienen densidad natural igual a variables geometricas independientes de parametro `1/2`; revisa stopping time, total stopping time y excursion maxima.

- Fuente: Jeffrey C. Lagarias, "The 3x+1 Problem: An Overview"
- Tipo: survey, AMS 2010; arXiv 2021
- Fecha: 2010/2021
- Link: https://arxiv.org/abs/2111.02635
- Relevancia: sintetiza el estado del area. Afirma que los modelos probabilisticos tratan paridades como coin flips independientes para la funcion `T`, y que hay patrones empiricos de total stopping time todavia no explicados por modelos estocasticos adecuados.

- Fuente: Terence Tao, "Almost all orbits of the Collatz map attain almost bounded values"
- Tipo: paper primario, arXiv 2019; Forum of Mathematics, Pi 2022
- Fecha: 2019/2022
- Link: https://arxiv.org/abs/1909.03562 ; https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F
- Relevancia: resultado moderno "almost all" via Syracuse iteration y una variable de primer pasaje; no es una comparacion modular `q mod 8`, pero confirma que stopping/descent se estudia con herramientas probabilisticas finas, no con un unico residuo local.

- Fuente: Gunther J. Wirsching, "The Dynamical System Generated by the 3n+1 Function"
- Tipo: libro, Lecture Notes in Mathematics 1681, Springer
- Fecha: 1998
- Link: https://link.springer.com/book/10.1007/BFb0095985
- Relevancia: tratamiento dinamico del problema, predecessor sets, p-adic distribution y un capitulo de Markov chain asintoticamente homogenea. Relacionado con modelos de arbol inverso, no con el experimento M15 exacto.

- Fuente: Ilia Krasikov and Jeffrey C. Lagarias, "Bounds for the 3x+1 problem using difference inequalities"
- Tipo: paper primario, Acta Arithmetica 109 (2003), 237-258
- Fecha: 2003
- Link: https://arxiv.org/abs/math/0205002 ; https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/109/33/81918/bounds-for-the-3x-1-problem-using-difference-inequalities
- Relevancia: bounds de densidad para enteros que alcanzan 1; usa desigualdades y computacion asistida. No encontre una comparacion de prediccion por `q mod 8`.

- Fuente: David Applegate and Jeffrey C. Lagarias, "Lower bounds for the total stopping time of 3X+1 iterates"
- Tipo: paper primario, Mathematics of Computation 72 (2003), 1035-1049
- Fecha: arXiv 2001; publicacion 2003
- Link: https://arxiv.org/abs/math/0103054
- Relevancia: total stopping time y computacion grande; predice/contrasta constantes de modelos aleatorios para `sigma_infty(n)`. No es un modelo modular local.

- Fuente: Tomas Oliveira e Silva, "Empirical verification of the 3x+1 and related conjectures"
- Tipo: capitulo/estudio computacional en The Ultimate Challenge
- Fecha: 2010
- Link: citado en el overview de Lagarias: https://arxiv.org/abs/2111.02635
- Relevancia: verificacion empirica, records de excursion/stopping; no encontre en esta fuente una ablation `q mod 8` vs geometrico.

## Hallazgos

Conocido:

1. Condicionar por residuos modulo potencias de 2 es lenguaje estandar. En Lagarias 1985, cada parity vector truncado de longitud `k` corresponde a una clase de congruencia unica modulo `2^k`; Terras usa esto para describir stopping/coefficient stopping time.
2. El mapa odd-to-odd acelerado `U` usa exactamente las valuaciones `ord_2(3n+1)`. Kontorovich-Lagarias muestran que las `o-sequences` tienen distribucion de densidad natural igual a geometricas independientes con parametro `1/2`.
3. Los modelos aleatorios/geometricos son el baseline clasico: paridades como coin flips para `T`, exponentes de division por 2 como geometricos para `U`, y random walks/log-random walks para stopping time.
4. Existen modelos estocasticos mas fuertes para total stopping time y extremos: MRP, BRW, RRW, branching random walk, y modelos de arbol inverso.

Implicito:

1. `q mod 8` es un caso pequeno de condicionamiento 2-adico. En terminos de la literatura, es un cilindro modulo `2^3`, o una informacion parcial del parity vector/valuation sequence.
2. Si `q` representa un estado odd-to-odd, `q mod 8` contiene informacion sobre las primeras divisiones por 2 despues de `3q+1`; por eso que prediga `next_tail` no sorprende.
3. Una comparacion empirica entre "modelo modular finito" y "modelo geometrico independiente" puede verse como una ablation practica de cuanta informacion queda en un residuo 2-adico de baja profundidad. Esa formulacion experimental es compatible con la literatura, pero no aparece con esos nombres.

No encontrado:

1. No encontre las probabilidades M15 exactas:
   - `q=1 mod 8 -> P(next_tail=1)=5/6`
   - `q=3 mod 8 -> 2/3`
   - `q=5 mod 8 -> 1/6`
   - `q=7 mod 8 -> 1/3`
2. No encontre un paper que compare especificamente `P(next_tail | q mod 8)` contra el modelo geometrico independiente para predecir supervivencia orbital, stopping time o blocks_to_descend.
3. No encontre los terminos `next_tail` ni `blocks_to_descend` en la literatura clasica; parecen terminologia interna del proyecto.
4. No encontre en Terras, Everett, Wirsching, Lagarias, Tao, Oliveira e Silva, Krasikov-Lagarias o Applegate-Lagarias la pregunta experimental M15 formulada como evaluacion predictiva de un feature modular `q mod 8`.

Confuso o pendiente:

1. Hay que distinguir distribucion global de `ord_2(3n+1)` en densidad natural de distribucion condicionada por un subconjunto del proyecto. La literatura dice que, globalmente y para secuencias finitas del mapa acelerado, el modelo geometrico independiente coincide con densidades naturales. M15 puede estar midiendo una poblacion sesgada por supervivencia, por definicion de `tail`, o por filtrado de blocks.
2. Una mejora predictiva real para survival/stopping podria desaparecer al controlar por informacion mas rica: longitud previa del bloque, altura logaritmica, numero acumulado de impares, o una parity/o-sequence mas larga.

## Impacto sobre la decision

Recomiendo:

Tratar M15 como experimento de ablation util, no como resultado teorico fuerte. La pregunta correcta no es si `q mod 8` "descubre" dinamica nueva, sino si un residuo 2-adico barato mejora out-of-sample la prediccion de supervivencia/stopping frente al baseline geometrico bajo el mismo muestreo.

No recomiendo:

No presentar el resultado como novedad matematica local. La dependencia de `next_tail` respecto de `q mod 8` es esperable por dinamica 2-adica y por el lenguaje de parity vectors/residue classes.

Riesgo principal:

Confundir una correlacion local condicionada por la poblacion experimental con una desviacion global del modelo geometrico. Kontorovich-Lagarias dan una razon fuerte para esperar independencia geometrica en densidad natural para `o-sequences`; M15 debe especificar claramente su condicionamiento y metrica de validacion.

## Citas clave

Notas breves con fuente:

1. Terras 1976: introduce stopping/coefficient stopping time y cuenta enteros por clases de congruencia/parity vectors. En Lagarias 1985 se resume como el resultado de que casi todos los enteros tienen stopping time finito.
2. Lagarias 1985: los primeros `k` iterados de `T` quedan completamente descritos por un parity vector; al invertir esa descripcion, cada vector corresponde a una clase modulo `2^k`.
3. Lagarias 1985: el obstaculo central del heuristico probabilistico es entender mezcla para todas las potencias de 2; esto ubica `q mod 8` como una version muy baja de esa informacion.
4. Kontorovich-Lagarias 2009: para el mapa acelerado, las `o-sequences` tienen densidad `2^{-(o_1+...+o_k)}`, igual a variables geometricas independientes de parametro `1/2`.
5. Kontorovich-Lagarias 2009: los modelos para forward iteration incluyen multiplicative random product y random walk logaritmico; para extremos y arbol inverso usan repeated random walk y branching random walks.
6. Lagarias 2010/2021: los modelos estocasticos aun no explican completamente algunos patrones empiricos de total stopping time en intervalos cortos.
7. Tao 2019/2022: el avance moderno sobre "almost all" usa Syracuse iteration, variables de primer pasaje y analisis armonico/3-adico, no un condicionamiento local `mod 8`.

## Preguntas abiertas

- En los datos M15, cual es exactamente la poblacion condicionada antes de medir `P(next_tail | q mod 8)`?
- La mejora del modelo modular sobre geometrico se mantiene en validacion out-of-sample por rangos de magnitud no mezclados?
- La mejora sobrevive si el baseline geometrico se condiciona por el mismo historial disponible, por ejemplo longitud de bloque, altura logaritmica o parity/o-sequence parcial?
- `mod 8` es el punto optimo, o `mod 16`, `mod 32` saturan rapidamente y revelan solo informacion local trivial?
- La variable objetivo `blocks_to_descend` esta mas correlacionada con residuos 2-adicos locales o con suma acumulada de `log(3)-o_i log(2)`?

