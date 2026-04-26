# Decision ClaudeSocio - Propuesta M16

Fecha: 2026-04-25
Agente: ClaudeSocio (agente unico activo)
Material revisado: todo el repo, incluyendo MILESTONES.md, todas las decisiones del orquestador, reportes de Codex hijos, informe web, revision critica previa, Conlusion.md, reportes de modelos geometricos y supervivencia.

## Estado de git

Rama actual: `main` (todas las ramas previas integradas).
Lock file `.git/index.lock` impide commits desde el sandbox; el commit debera hacerse desde la maquina local del usuario.

## Resumen de lo que entendi

El proyecto lleva 16 milestones (M0-M15) investigando la conjetura de Collatz desde un enfoque empirico-computacional con rigor estadistico creciente.

Trayectoria cientifica:

1. M1-M5: infraestructura y primeros datos. Motor Collatz, datasets, paridad, residuos, reporte.
2. M6-M9: modelo estocastico. Se construyo un modelo geometrico independiente (`tail ~ Geom(1/2)`, `exit_v2 ~ Geom(1/2)`) que explica muy bien el cuerpo de la distribucion de cadenas odd-to-odd, pero sobreproduce extremos.
3. M10-M12: busqueda de estructura fina. Se busco anti-persistencia, sesgos por `exit_v2` alto, congruencias de `exit_v2 = 5`. Todas descartadas o explicadas como algebra local.
4. M13-M14: supervivencia orbital. Se encontro un residuo `prev_exit_v2 = 5 + interior_block` que no sobrevivio holdout independiente. Descarte limpio.
5. M15: busqueda confirmatoria. Se verifico que `q mod 8` predice `next_tail` (algebra esperable), pero la matriz de transicion `q mod 8` mezcla casi uniforme en un paso. M15 cerrado/enfriado.

Hallazgo robusto principal: el modelo geometrico independiente es un baseline excelente para el cuerpo de la distribucion. La unica desviacion sistematica confirmada es que **el modelo sobreproduce extremos** (cadenas muy largas y picos muy altos). Nadie en el proyecto ha explicado satisfactoriamente por que.

Hallazgos descartados: `exit_v2 = 5` como lemma, `prev_exit_v2 = 5 + interior` como senal, `q mod 8` marginal como memoria de supervivencia.

Hallazgo metodologico: el protocolo de preguntas antes/despues, holdout separado y descarte disciplinado funciona bien. Es el activo mas valioso del proyecto.

## Veredicto sobre M15

M15 esta correctamente cerrado/enfriado. La tabla `q mod 8 -> next_tail` es algebra local esperable; la matriz de transicion mezcla en un paso; no hay memoria marginal suficiente para afectar cadenas completas. No se gasto holdout fresco. Buen trabajo.

No reabrir M15 sin una razon teorica nueva (no empirica).

## Opciones para M16

Antes de proponer, aplico las preguntas obligatorias a cada opcion.

### Opcion A: Explicar la sobreproduccion de extremos del modelo geometrico

Pregunta: por que el modelo geometrico independiente genera mas cadenas largas y picos mas altos que la dinamica real?

Preguntas de filtro:

- Estamos en algo potencialmente virgen? Parcialmente. El fenomeno esta documentado en el proyecto (M9, reportes geometricos). La literatura conoce que modelos aleatorios sobreestiman extremos, pero las explicaciones formales son escasas. Kontorovich-Lagarias mencionan que los modelos estocasticos no capturan completamente los patrones empiricos de total stopping time.
- Alguien ya hizo esto? No exactamente como ablation: "que feature aritmetico explica el gap real-modelo en las colas?". Hay trabajos de Applegate-Lagarias sobre bounds de total stopping time, pero no una descomposicion del gap.
- Que seria nuevo si sale bien? Una explicacion constructiva (no post-hoc) de por que la dinamica real produce menos extremos que el modelo i.i.d. Esto tendria nivel 3-4 si es limpio.
- Que resultado destruiria la hipotesis? Que el gap desaparezca al ampliar el rango (seria efecto de finitud), o que el gap sea explicable trivialmente por el sesgo de que n es finito y las colas geometricas no lo son.
- Necesitamos web, algebra, experimento o critica? Web primero: buscar si existe una explicacion publicada del gap real-modelo en colas de stopping time. Algebra segundo: hay un argumento de contraccion (promedio `log(3/4)` por bloque) que limita colas reales mas estrictamente que el modelo i.i.d.?

### Opcion B: Reporte tecnico de cierre M12-M15

Pregunta: consolidar lo aprendido en un documento unico que sirva como caso de estudio de descarte disciplinado.

Preguntas de filtro:

- Estamos en algo virgen? No cientificamente, pero si metodologicamente: un caso documentado de multiples descartes pre-registrados en investigacion computacional de Collatz es poco comun.
- Que seria nuevo? El documento en si como referencia interna. No publicable externamente, pero util para el proyecto.
- Que resultado destruiria la hipotesis? N/A: es documentacion, no hipotesis.
- Necesitamos web, algebra, experimento o critica? Solo escritura y revision.

### Opcion C: Cerrar M0 (auditoria de fuentes)

M0 esta en progreso desde el inicio y nunca fue completado formalmente. `AuditoriaFuentesCollatz.md` existe pero no fue actualizado con los claims de M7-M15.

Preguntas de filtro:

- Estamos en algo virgen? No, es higiene.
- Que seria nuevo? Nada nuevo; es deuda tecnica.
- Necesitamos web, algebra, experimento o critica? Solo revision y actualizacion.

## Mi decision: Opcion A, con compuerta de literatura

Razon: la sobreproduccion de extremos del modelo geometrico es la unica desviacion sistematica robusta que ha sobrevivido todo el proyecto. Todas las pistas de M10-M15 fueron intentos de explicarla desde el lado de la dependencia modular, y todas fracasaron. Pero la pregunta raiz sigue viva.

El enfoque nuevo seria atacarla desde el otro lado: no "que dependencia aritmetica falta en el modelo" (eso ya se intento), sino "que restriccion global tiene la dinamica real que el modelo i.i.d. ignora".

Hay una candidata obvia que no vi explorada en el proyecto: la **restriccion de contraccion neta**. Para que una orbita real termine en 1, la suma total `sum(tail_i * log(3/2) - exit_v2_i * log(2))` debe ser exactamente `-log(n_0)`. El modelo i.i.d. no impone esa restriccion; genera cadenas donde la suma puede ser cualquier cosa negativa. Las cadenas reales extremas deben eventualmente compensar toda la expansion acumulada, lo cual puede imponer correlaciones negativas de largo alcance que el modelo i.i.d. no captura.

Esto no es anti-persistencia local (M10 la busco y no la encontro), sino una restriccion global: las cadenas muy largas necesitan que la suma logaritmica pase por cero muchas veces antes de caer definitivamente, y cada vez que "casi cae" la dinamica real produce un `next_tail` que esta correlacionado con el valor actual (porque `n` es un entero especifico, no un muestreo aleatorio).

## Plan concreto para M16

Nombre: M16 - Restriccion de contraccion neta y sobreproduccion de extremos.

### Paso 1: busqueda web (yo mismo)

Buscar si existe en la literatura una explicacion del gap entre modelos geometricos/aleatorios y datos reales en las colas de `blocks_to_descend` o stopping time. Buscar especificamente:

- "random walk overshoot" aplicado a Collatz;
- "conditioned random walk" o "bridge" para stopping times;
- diferencias entre random walk libre y random walk condicionado a cruzar un umbral.

Criterio de abandono del paso 1: si encuentro un paper que ya explica el gap completamente, M16 se reformula como replicacion, no como descubrimiento.

### Paso 2: algebra previa

Calcular que restriccion impone la condicion `sum = -log(n_0)` sobre la distribucion de trayectorias. Especificamente:

- En un random walk con drift `mu = E[tail*log(3/2) - exit_v2*log(2)]`, la distribucion de tiempo de primer cruce por `-log(n)` esta dada por la distribucion de Wald/inverse Gaussian.
- El modelo i.i.d. del proyecto NO condiciona por primer cruce; simplemente simula hasta que la suma sea negativa. Eso puede ser la fuente del gap.
- La pregunta testeable es: si reemplazamos el modelo i.i.d. por un modelo condicionado por primer cruce (random walk bridge o taboo process), el gap en extremos se cierra?

Criterio de abandono del paso 2: si la algebra muestra que el condicionamiento por primer cruce no cambia la distribucion de `blocks_to_descend` (porque el drift ya es negativo y el overshoot es despreciable), la hipotesis se descarta.

### Paso 3: experimento minimo preregistrado

Solo si los pasos 1 y 2 sobreviven.

Train: `n in [1, 5000000]` (rango quemado).
Holdout: `n in [15000001, 25000000]` (fresco).
H1 preregistrada: el modelo de random walk condicionado por primer cruce predice mejor la distribucion de `P(blocks >= k)` para `k >= 10` que el modelo i.i.d., medido por log-likelihood ratio.
Maximo 3 tests: `k = 10`, `k = 20`, `k = 30`. Bonferroni con alfa = 0.05/3.

Criterio de exito: mejora significativa (p < 0.017) en al menos uno de los tres umbrales, con misma direccion en train y holdout.
Criterio de abandono: ningun test significativo, o mejora solo en train.

## Que no deberiamos concluir

- Que la sobreproduccion de extremos prueba algo sobre Collatz.
- Que un modelo condicionado "resuelve" el problema.
- Que la restriccion de contraccion neta es una idea nueva (es implicita en toda la teoria de random walks con drift).

## Resultados de la busqueda web (Paso 1 completado)

### Hallazgo critico: Bonacorsi-Bordoni (arXiv:2603.04479, marzo 2026)

Paper: "Bayesian Modeling of Collatz Stopping Times: A Probabilistic Machine Learning Perspective".

Este paper hace algo muy cercano a lo que el proyecto intento en M15 y propone para M16:

1. Usan `n mod 8` como covariable para predecir stopping time via un modelo Bayesiano jerarquico (NB2-GLM).
2. Proponen un modelo generativo mecanicista basado en la descomposicion odd-block, con `K(m) = v2(3m+1)` como longitud de bloque aleatorizada.
3. Confirman que condicionar la distribucion de longitudes de bloque por `m mod 8` mejora marcadamente el ajuste distribucional del generador.
4. El posterior predictive check del NB2-GLM ajusta bien el bulk pero **sobreestima ligeramente la masa de la cola derecha extrema**.
5. En datos holdout, el NB2-GLM tiene mayor predictive likelihood que los generadores de bloques.

### Impacto sobre M16

Esto cambia significativamente el panorama:

1. **La Opcion A original (explicar sobreproduccion de extremos) queda parcialmente cubierta.** Bonacorsi-Bordoni confirman que el fenomeno existe y que modelos mas sofisticados (incluyendo condicionamiento por `m mod 8`) aun lo exhiben. Eso refuerza que el gap no es trivial.

2. **El nivel de novedad baja.** Si otro grupo ya uso `n mod 8` para predecir stopping time y ya documento la sobreestimacion de colas, nuestra contribucion no puede ser "descubrir" eso. Pero ellos no parecen haber explorado la causa del gap (restriccion de contraccion neta / random walk condicionado).

3. **La pregunta sobrevive reformulada:** Bonacorsi-Bordoni documentan el gap pero no lo explican mecanicamente. Nuestro angulo de "random walk condicionado por primer cruce vs random walk libre" sigue sin estar cubierto, hasta donde pude verificar.

### Otros hallazgos de la busqueda

- Kontorovich-Lagarias (2009): el modelo RRW (Repeated Random Walk) predice `lim sup(sigma_inf(n)/log(n)) ~ 41.68`, consistente con datos empiricos hasta `10^11`. Predicen extremos via large deviations, pero no explican por que el modelo i.i.d. simple sobreproduce colas respecto de datos finitos.
- No encontre un paper que aborde explicitamente la diferencia entre random walk libre y random walk condicionado por primer cruce como explicacion del gap en colas de `blocks_to_descend` o stopping time.
- El termino "conditioned random walk" + "Collatz" no arroja resultados directos.

### Decision revisada

M16 sigue vivo, pero con reformulacion:

- **No es "descubrir la sobreproduccion de extremos"** (Bonacorsi-Bordoni ya lo documentan).
- **Es "explicar mecanicamente el gap via condicionamiento por primer cruce"**, que no aparece en la literatura encontrada.
- **Nivel de novedad honesto:** 2-3 (reformulacion experimental de ingredientes conocidos de random walks). Si el modelo condicionado cierra el gap cuantitativamente, podria ser 3 (formulacion propia util).

## Proxima accion concreta

Paso 2: algebra previa. Debo calcular:

1. El drift del random walk logaritmico del modelo del proyecto: `mu = E[tail * log(3/2) - exit_v2 * log(2)]`. Con `tail, exit_v2 ~ Geom(1/2)`: `E[tail] = E[exit_v2] = 2`, por lo tanto `mu = 2*log(3/2) - 2*log(2) = 2*log(3/4) = -0.5754...`. El drift es negativo.

2. La distribucion de primer cruce de un random walk con drift negativo y pasos discretos. Para drift negativo, el random walk cruza cualquier umbral negativo con probabilidad 1. La distribucion del tiempo de primer cruce sigue la distribucion de Wald (inverse Gaussian) en el limite continuo.

3. La diferencia clave: el modelo del proyecto simula hasta que la suma acumulada sea negativa por primera vez (`blocks_to_descend`). Eso ya es un problema de primer cruce. Pero el modelo i.i.d. no impone que la cadena termine en un valor especifico (`1`); solo que cruce `0` hacia abajo. La diferencia entre "cruzar 0" y "llegar exactamente a -log(n)" puede generar diferencias en la cola si el overshoot importa.

4. Para cadenas largas (`blocks >= k`), la probabilidad de sobrevivir `k` bloques en el random walk con drift `-0.575` es aproximadamente `exp(-lambda * k)` para alguna constante de decaimiento. La pregunta es si la constante de decaimiento real difiere de la del modelo i.i.d. debido a restricciones aritmeticas.

Esto puedo calcularlo algebraicamente y verificarlo con un script chico. Lo hare en el siguiente paso.

## Fuentes de la busqueda web

- [Bonacorsi & Bordoni - Bayesian Modeling of Collatz Stopping Times (arXiv:2603.04479)](https://arxiv.org/abs/2603.04479)
- [Kontorovich & Lagarias - Stochastic Models for the 3x+1 and 5x+1 Problems (arXiv:0910.1944)](https://arxiv.org/abs/0910.1944)
- [nissy220 - Collatz problem stochastic model (GitHub)](https://github.com/nissy220/Collatz_problem)
- [Lagarias - The 3x+1 Problem: An Overview (arXiv:2111.02635)](https://arxiv.org/abs/2111.02635)
- [IOP Science - Stochastic-like characteristics of arithmetic dynamical systems](https://iopscience.iop.org/article/10.1088/2632-072X/ad271f)
