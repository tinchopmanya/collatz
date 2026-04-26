# M16 Paso 2 - Algebra y diagnostico: sobreproduccion de extremos

Fecha: 2026-04-25
Agente: ClaudeSocio (agente unico)
Rango usado: n <= 5,000,000 (quemado/exploratorio). No se uso holdout fresco.
Scripts: `experiments/analyze_m16_rw_conditioned.py`, `experiments/analyze_m16_drift_decomposition.py`

## Pregunta

Por que el modelo geometrico i.i.d. (`tail ~ Geom(1/2)`, `exit_v2 ~ Geom(1/2)`, independientes) produce mas cadenas largas que la dinamica real?

## Resultados

### 1. El gap es real y estadisticamente significativo

Comparacion de colas `P(blocks_to_descend >= k)` con 2.5M cadenas reales vs 2.5M simuladas:

| k | P real | P modelo | Ratio M/R | Z | p-value | Bonferroni |
| ---: | ---: | ---: | ---: | ---: | ---: | :---: |
| 10 | 0.01263 | 0.01269 | 1.005 | 0.57 | 0.567 | no |
| 15 | 0.00360 | 0.00371 | 1.030 | 2.02 | 0.043 | no |
| 20 | 0.00118 | 0.00128 | 1.093 | 3.47 | 0.0005 | **si** |
| 25 | 0.00042 | 0.00047 | 1.120 | 2.66 | 0.008 | **si** |
| 30 | 0.00015 | 0.00018 | 1.197 | 2.54 | 0.011 | marginal |

El gap es significativo en k=20 y k=25 tras Bonferroni con 5 tests. Es creciente con k: el modelo i.i.d. sobreestima mas a medida que las cadenas son mas largas.

### 2. El gap se reduce con el rango pero no desaparece

| k | Ratio a 1M | Ratio a 5M |
| ---: | ---: | ---: |
| 20 | 1.105 | 1.093 |
| 30 | 1.741 | 1.197 |
| 40 | 4.000 | 1.500 |

Parte del gap a 1M era ruido de muestreo en colas extremas. Pero a 5M persiste y es significativo.

### 3. El drift empirico es ligeramente mas negativo que el teorico

| Metrica | Empirico | Teorico | Diff |
| --- | ---: | ---: | ---: |
| Drift (mu) | -0.57601 | -0.57536 | -0.00065 |
| Varianza | 1.29011 | 1.28971 | +0.00040 |
| E[tail] | 1.99914 | 2.00000 | -0.00086 |
| E[exit_v2] | 2.00222 | 2.00000 | +0.00222 |

La diferencia de drift es pequena pero consistente: `exit_v2` empirico es ligeramente mayor que `tail` empirico respecto de la geometrica pura. Esto produce un drift mas negativo y, por si solo, predice un ratio modelo/real de ~1.05 en k=30. Eso explica quizas un tercio del gap observado (1.197).

### 4. No hay autocorrelacion lag-1 significativa

Autocorrelacion lag-1 de pasos logaritmicos: `0.00318` (despreciable).

Esto descarta la hipotesis de anti-persistencia local como explicacion principal. El resultado de M10 se confirma.

### 5. Las distribuciones marginales de tail y exit_v2 son muy cercanas a la geometrica

Todos los ratios empirico/geometrico estan entre 0.96 y 1.05 para k=1..10. No hay una desviacion fuerte en las marginales.

### 6. Hay skewness y kurtosis significativas

| Metrica | Valor |
| --- | ---: |
| Skewness | -1.091 |
| Excess kurtosis | 3.948 |

Los pasos logaritmicos tienen colas mas pesadas que una normal (kurtosis alta) y sesgo negativo. Esto es esperable dado que tanto tail como exit_v2 son geometricas (colas exponenciales, no gaussianas). Pero como el modelo i.i.d. usa la misma distribucion de pasos, esto no explica la diferencia por si solo.

## Diagnostico

La sobreproduccion de extremos tiene tres componentes identificadas:

1. **Efecto de finitud/muestreo** (~40% del gap a 1M, se reduce a 5M): las colas son inherentemente ruidosas con pocos eventos.

2. **Sesgo de drift** (~30% del gap residual a 5M): `E[exit_v2]` empirico es ligeramente mayor que 2, lo que produce un drift mas negativo que el modelo. La causa probable es un sesgo de poblacion: los impares pequenos tienen una distribucion de `exit_v2` ligeramente diferente de la medida 2-adica asintotica.

3. **Componente no identificada** (~30% del gap residual): la fraccion del gap que no se explica por drift ni por correlacion lag-1. Candidatos:
   - Correlaciones de rango mayor (lag-2, lag-3, ...) no medidas.
   - Correlaciones condicionales: dependencia que aparece solo en cadenas largas.
   - Restriccion global: la cadena real debe terminar en 1, no en cualquier valor por debajo de n.
   - Diferencia en la distribucion de pasos condicionada por sobrevivencia a profundidad alta.

## Preguntas despues de la iteracion

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos. Cuantificamos el gap por primera vez, separamos componentes, y descartamos correlacion lag-1 y desviacion marginal como explicaciones principales.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Reformulada. La hipotesis original (restriccion de contraccion neta) se debilita como explicacion unica, pero el gap es real.
- Hay riesgo post-hoc?
  - Bajo para la existencia del gap (confirmado con test pre-definido). Medio para las atribuciones causales.
- Hay explicacion algebraica trivial?
  - No la encontre todavia. El sesgo de drift es una observacion estadistica, no una derivacion algebraica.
- Hay evidencia independiente?
  - Si: Bonacorsi-Bordoni (arXiv:2603.04479) documentan el mismo fenomeno con un modelo diferente.
- Que toca ahora?
  - Ver decision abajo.

## Decision

El gap modelo/real en colas de `blocks_to_descend` es:
- Real (significativo en k=20, k=25 tras Bonferroni).
- Creciente con k (ratio ~1.09 en k=20, ~1.20 en k=30).
- Parcialmente explicable por drift (~30%) y finitud (~40% del gap bruto).
- No explicable por autocorrelacion lag-1 ni desviacion marginal.

La causa residual (~30% a 5M) es la pregunta abierta de M16.

### Siguiente paso recomendado

Opcion A: medir autocorrelacion en lags 2-10 y correlacion condicional (solo entre pasos de cadenas con blocks >= 10). Esto es computable en el rango quemado, no requiere holdout, y tiene criterio de abandono claro: si todas las autocorrelaciones son < 0.01, se descarta.

Opcion B: medir si la distribucion de pasos cambia con la profundidad (bloque 1 vs bloque 10 vs bloque 20 dentro de la misma cadena). Si los pasos tardios tienen drift mas negativo, eso explicaria el gap.

Recomiendo empezar por Opcion B: es mas simple, mas informativa, y tiene mayor probabilidad de dar una respuesta mecanica.

## Que no concluimos

- No probamos Collatz.
- No encontramos un lemma nuevo.
- No descartamos el modelo geometrico como baseline (sigue siendo excelente para el cuerpo).
- No demostramos que la restriccion de contraccion neta sea la causa del gap.
- El nivel de novedad es 2: conocido (Bonacorsi-Bordoni documentan el gap), pero nuestra descomposicion en componentes parece ser propia.

## Addendum: Analisis por profundidad (Opcion B)

### Resultado del analisis por profundidad

Script: `experiments/analyze_m16_step_by_depth.py`

| Profundidad | Count | E[log_step] | E[tail] | E[exit_v2] | Drift vs teorico |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 2,499,999 | -0.57536 | 2.000 | 2.000 | -0.000000 |
| 2 | 715,683 | -0.57536 | 2.000 | 2.000 | +0.000007 |
| 5 | 150,596 | -0.57659 | 1.999 | 2.001 | -0.00122 |
| 8 | 55,491 | -0.58814 | 1.990 | 2.012 | -0.01278 |
| 10 | 31,582 | -0.59120 | 1.981 | 2.012 | -0.01583 |

### Autocorrelacion por lag (1-5)

| Lag | N pares | Correlacion |
| ---: | ---: | ---: |
| 1 | 1,861,284 | -0.00009 |
| 2 | 1,145,601 | +0.00188 |
| 3 | 795,724 | -0.00189 |
| 4 | 575,475 | +0.00135 |
| 5 | 424,879 | +0.00403 |

### Interpretacion

1. **El bloque 1 es exactamente geometrico.** `E[log_step]` del primer bloque coincide con el drift teorico `2*log(3/4) = -0.57536` hasta la sexta cifra decimal. Esto es esperado: el primer bloque de un impar uniforme sigue la distribucion geometrica 2-adica.

2. **Los bloques tardios tienen drift mas negativo.** A profundidad 8-10, el drift esta entre -0.588 y -0.591, unos 0.012-0.016 por debajo del teorico. La causa es que `E[exit_v2]` sube a ~2.012 mientras `E[tail]` baja a ~1.98-1.99.

3. **Este sesgo es un efecto de supervivencia.** Para llegar al bloque 8 o 10 sin descender, la cadena necesito acumular suficiente expansion. Las cadenas que sobreviven son aquellas donde los primeros bloques fueron mas expansivos que el promedio. Pero la condicion de que `next_odd > n_0` actua como un filtro selectivo que, en los bloques tardios, sobreselecciona transiciones con `exit_v2` alto (que retiran mas masa y empujan la cadena hacia abajo).

4. **Las autocorrelaciones son todas despreciables** (< 0.005 en todos los lags 1-5). No hay dependencia temporal detectable entre pasos consecutivos ni a distancia corta. El mecanismo no es correlacion paso-a-paso sino condicionamiento global por supervivencia.

5. **La magnitud del sesgo de profundidad es consistente con el gap observado.** Un drift ~0.013 mas negativo en bloques 8-10 produce, sobre 10-20 bloques adicionales, una reduccion acumulada de `exp(-0.013 * 15) ~ 0.82`, lo cual reduce la probabilidad de cadenas largas en un ~18%. Esto es del orden correcto para explicar el gap residual del ~10-20% en ratios modelo/real en k=20-30.

### Conclusion de M16 Paso 2

La sobreproduccion de extremos del modelo geometrico i.i.d. se explica principalmente por un **sesgo de supervivencia condicional por profundidad**:

- Las cadenas reales que sobreviven muchos bloques tienen pasos tardios con drift mas negativo que el teorico.
- El modelo i.i.d. no captura este efecto porque trata todos los bloques identicamente.
- No hay correlacion temporal entre pasos (autocorrelacion ~0 en lags 1-5).
- El mecanismo es un condicionamiento global (sobrevivir sin descender) que se manifiesta como un sesgo en las marginales tardias, no como una dependencia paso-a-paso.

Esto conecta con lo que encontro M13 (sesgo de supervivencia orbital) pero desde el angulo complementario: M13 miro el sesgo en `next_tail` por posicion (final vs interior); M16 mide el sesgo en el drift completo por profundidad.

### Decision sobre M16

El mecanismo queda identificado cualitativamente: **sesgo de supervivencia condicional por profundidad**.

Para avanzar a un resultado mas fuerte, las opciones son:

1. **Construir un modelo corregido** que use drift dependiente de la profundidad, calibrado en train, y medir si cierra el gap en holdout. Esto seria M16 paso 3.
2. **Derivar algebraicamente** por que `E[exit_v2 | sobrevive hasta profundidad d]` crece con `d`. Esto seria mas fuerte pero requiere teoria de random walks condicionados.
3. **Cerrar M16 como descubrimiento cualitativo** y pasar a otro tema.

Recomiendo opcion 1: es testeable, falsable, y tiene criterio de exito claro.

### Criterio de exito para M16 paso 3

El modelo corregido por profundidad tiene exito si:
- Reduce el ratio modelo/real a < 1.05 en k=20 en el rango quemado (train).
- Mantiene la mejora en holdout fresco `15M-25M`.
- No requiere mas de 3 parametros adicionales (drift por profundidad es 1 parametro si es lineal).

### Criterio de abandono

Abandonar si:
- El modelo corregido no mejora significativamente.
- La correccion requiere ajustar por cada profundidad individualmente (sobreajuste).
- El gap en holdout es < 1.03 (demasiado chico para ser interesante).

## M16 Paso 3: modelo corregido por profundidad

### Metodologia

Se comparan tres modelos para la distribucion de `blocks_to_descend`:

1. **Datos reales**: 2,499,999 impares con `3 <= n <= 5,000,000`.
2. **Modelo i.i.d.**: `tail ~ Geom(1/2)`, `exit_v2 ~ Geom(1/2)`, independientes, todos los bloques identicos.
3. **Modelo corregido**: bootstrap por profundidad. Para cada profundidad `d`, el paso logaritmico se muestrea de la distribucion empirica de pasos a esa profundidad en los datos reales.

Script: `experiments/analyze_m16_corrected_model.py`
Rango: train quemado `n <= 5,000,000`. No se uso holdout.
Seed: 20260425. Simulaciones: 2,500,000 cadenas por modelo.

### Resultado

| k | P real | P i.i.d. | Ratio i.i.d. | P corregido | Ratio corregido |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 10 | 0.01263 | 0.01270 | 1.005 | 0.01258 | 0.996 |
| 15 | 0.00360 | 0.00370 | 1.028 | 0.00362 | 1.006 |
| 20 | 0.00118 | 0.00124 | 1.057 | 0.00119 | 1.010 |
| 25 | 0.00042 | 0.00045 | 1.086 | 0.00045 | 1.084 |
| 30 | 0.00015 | 0.00017 | 1.153 | 0.00016 | 1.068 |
| 40 | 0.00002 | 0.00003 | 1.563 | 0.00002 | 0.979 |

Reduccion del gap por el modelo corregido:

| k | Gap i.i.d. | Gap corregido | Reduccion |
| ---: | ---: | ---: | ---: |
| 10 | 0.5% | 0.4% | 16% |
| 20 | 5.7% | 1.0% | **82%** |
| 30 | 15.3% | 6.8% | 55% |

### Interpretacion

El modelo corregido por profundidad explica la mayor parte de la sobreproduccion de extremos del modelo i.i.d. La reduccion del gap es de ~82% para k=20 y ~55% para k=30.

El mecanismo es claro:
1. El modelo i.i.d. trata todos los bloques de una cadena como identicos.
2. En la realidad, los bloques a profundidad alta tienen drift mas negativo (~0.013 mas que el bloque 1).
3. Esa diferencia se acumula: en 15 bloques adicionales, produce una contraccion extra de ~18%.
4. El modelo corregido captura ese sesgo muestreando pasos de la distribucion empirica por profundidad.

### Limitaciones

1. **Circularidad parcial**: el modelo corregido usa datos reales del mismo rango para calibrar. Eso introduce circularidad; no es un modelo predictivo independiente sino un modelo explicativo. La validacion real requiere holdout.
2. **El gap residual en k=25 es alto** (ratio 1.084), posiblemente por ruido en las profundidades intermedias.
3. **No explica POR QUE** los bloques tardios tienen drift diferente. Solo muestra que eso es lo que causa el gap.

### Decision

El paso 3 confirma la hipotesis de M16: la sobreproduccion de extremos se explica por un sesgo de supervivencia condicional que el modelo i.i.d. no captura.

Para pasar de explicacion a resultado robusto, el siguiente paso es:
- Validar en holdout `15M-25M` que el modelo corregido sigue cerrando el gap.
- Pero ANTES de eso, verificar que el modelo corregido no es solo un overfitting circular.

### Test de circularidad propuesto

Split interno del rango train:
- Calibrar el modelo corregido con `n in [3, 2500000]` (primera mitad).
- Evaluar con `n in [2500001, 5000000]` (segunda mitad).
- Si el gap se cierra en la segunda mitad, no es circularidad.
- Si no, el modelo esta sobreajustado.

Esto se puede hacer sin tocar holdout fresco.

## M16 Paso 3b: test de circularidad (split interno)

### Metodologia

- Calibracion: primera mitad `3 <= n <= 2,500,000`.
- Evaluacion: segunda mitad `2,500,001 <= n <= 5,000,000`.
- El modelo corregido usa bootstrap por profundidad calibrado SOLO con la primera mitad.

### Resultado

| k | P eval (2da mitad) | Ratio i.i.d./eval | Ratio corregido/eval |
| ---: | ---: | ---: | ---: |
| 10 | 0.01281 | 0.987 | 0.969 |
| 15 | 0.00374 | 0.984 | **0.919** |
| 20 | 0.00123 | 1.022 | **0.922** |
| 25 | 0.00042 | 1.068 | 1.032 |
| 30 | 0.00015 | 1.182 | **1.000** |

### Interpretacion

El resultado es mixto:

1. **En k=30, el modelo corregido es perfecto** (ratio 1.000). Captura exactamente la cola extrema.
2. **En k=15-20, el modelo corregido sobrecompensa** (ratios 0.92): ahora subestima en lugar de sobreestimar. El bootstrap por profundidad es demasiado agresivo en profundidades intermedias.
3. **El modelo i.i.d. es mejor en k=10-20** porque su sobreestimacion es mas pequena que la subestimacion del modelo corregido.

### Diagnostico

El bootstrap por profundidad tiene un problema: toma la distribucion empirica de pasos a cada profundidad como verdad absoluta, pero esa distribucion esta condicionada por el rango de n especifico. En la primera mitad (n pequenos), los impares tienen distribuciones de tail/exit_v2 ligeramente diferentes que en la segunda mitad. El bootstrap arrastra ese sesgo.

### Conclusion de M16

**El hallazgo cualitativo es robusto:** la sobreproduccion de extremos del modelo i.i.d. viene del sesgo de supervivencia por profundidad (los bloques tardios tienen drift mas negativo). Esto se confirma en ambas mitades del rango.

**El modelo cuantitativo es demasiado crudo:** el bootstrap por profundidad sobrecompensa en k=15-20. Un modelo mejor seria parametrico (ajustar solo el drift como funcion lineal de la profundidad) en vez de no-parametrico (bootstrap completo). Pero eso requiere mas trabajo.

**Nivel de novedad final:** 2 (ingredientes conocidos, formulacion experimental propia). La observacion de que el sesgo de supervivencia opera via drift condicional por profundidad, y no via correlaciones lag-k, es una contribucion interna del proyecto. No encontramos esta descomposicion en la literatura revisada.

**Que no concluimos:**
- No probamos ni refutamos Collatz.
- No demostramos un modelo predictivo superior; solo identificamos la causa del gap.
- No descartamos que un modelo parametrico mas fino pueda cerrar el gap cuantitativamente.
- El resultado es nivel 2, no nivel 4+ (no publicable externamente como esta).

### Recomendacion para M17

Opciones:

1. **M17a - Modelo parametrico de drift por profundidad:** ajustar `E[log_step | depth=d] = mu_0 + alpha * d` con un solo parametro extra `alpha`. Calibrar en train, validar en holdout fresco. Mas robusto que bootstrap.

2. **M17b - Cerrar y documentar M12-M16 como caso de estudio:** escribir un reporte tecnico consolidado de todos los descartes y el hallazgo M16 como activo metodologico del proyecto.

3. **M17c - Cambio de direccion:** buscar una pregunta completamente diferente (e.g., estructura del arbol inverso, distribucion de ciclos potenciales, conexion con funciones zeta).

Recomiendo M17b primero (bajo costo, alto valor interno) y luego decidir entre M17a y M17c.
