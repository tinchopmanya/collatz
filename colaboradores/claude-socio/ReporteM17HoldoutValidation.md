# Reporte M17 - Validacion en holdout fresco

Fecha: 2026-04-25
Agente: ClaudeSocio
Revision: incorpora feedback del revisor critico externo

## Objetivo

Validar si el modelo depth-corrected (bootstrap por profundidad, calibrado en train n <= 5M) predice mejor la distribucion de `blocks_to_descend` que el modelo i.i.d. en un holdout completamente fresco: n in [15M, 25M], nunca tocado en el proyecto.

## Preregistro

- 3 tests: k = 15, 20, 25
- Bonferroni alfa = 0.05/3 = 0.017
- Criterio de exito: al menos 1/3 tests muestra mejora significativa
- Criterio de abandono: ningun test significativo, o sobrecompensacion (ratio < 0.90)

## Resultados

### Tabla comparativa holdout [15M, 25M]

| k | P_real | ratio_iid | ratio_corr |
|---|--------|-----------|------------|
| 5 | 0.0602 | 0.997 | 1.002 |
| 10 | 0.0127 | 0.997 | 0.992 |
| 15 | 0.00369 | 1.006 | 0.982 |
| 20 | 0.00127 | 0.967 | 0.949 |
| 25 | 0.00046 | 0.975 | 0.973 |
| 30 | 0.00019 | 0.926 | 0.817 |
| 40 | 0.000026 | 1.008 | 0.690 |

### Tests preregistrados

| k | ratio_iid | CI95_iid | 1.0 in CI? | ratio_corr | CI95_corr | 1.0 in CI? |
|---|-----------|----------|-----------|------------|-----------|-----------|
| 15 | 1.007 | [0.986, 1.027] | Si | 0.982 | [0.962, 1.002] | Si |
| 20 | 0.967 | [0.933, 1.001] | Si | 0.949 | [0.917, 0.984] | No |
| 25 | 0.975 | [0.920, 1.034] | Si | 0.973 | [0.919, 1.032] | Si |

### Referencia: resultados en train [3, 5M]

| k | ratio_iid | ratio_corr |
|---|-----------|------------|
| 15 | 1.032 | 1.006 |
| 20 | 1.041 | 1.023 |
| 25 | 1.079 | 1.077 |

## Observacion principal

**La direccion del gap observado cambia segun el rango de n, pero el cambio no es estadisticamente significativo en los tests preregistrados.**

- En train (n <= 5M): los ratios i.i.d. son > 1.0 (1.03-1.08), sugiriendo sobreproduccion.
- En holdout (15M-25M): los ratios i.i.d. son < 1.0 para k >= 20 (0.93-0.97), sugiriendo subproduccion.
- Sin embargo, **los CI del modelo i.i.d. contienen 1.0 en los 3 tests preregistrados** (k=15,20,25). Por lo tanto, no se puede afirmar que la subproduccion sea estadisticamente significativa. Lo que se observa es un cambio de tendencia, no un hallazgo robusto.

### Sobre el modelo corregido

En k=20, el modelo corregido queda en ratio=0.949 con CI [0.917, 0.984], que **no contiene 1.0**. Esto sugiere que el modelo corregido subproduce significativamente en holdout. Sin embargo, para afirmar rigurosamente que "empeora respecto del i.i.d." seria necesario un test pareado (bootstrap pareado de la diferencia de errores), que no fue preregistrado. Lo que se puede afirmar: el modelo corregido tiene un sesgo significativo hacia subproduccion en k=20 en holdout, mientras que el i.i.d. no lo tiene.

### Sobre la diferencia de log(n)

La diferencia en escala logaritmica entre los rangos es: `ln(20M) - ln(4M) = ln(5) = 1.61` (en log natural), o `log2(5) = 2.32` (en log base 2). En versiones anteriores de este reporte se decia "~2.5", lo cual era impreciso. La diferencia correcta es ~1.6 en log natural o ~2.3 en log base 2, dependiendo de la base usada.

## Veredicto

**M17: RESULTADO NEGATIVO. Tests preregistrados: 0/3 significativos para mejora del modelo corregido.**

El modelo depth-bootstrap no generaliza de train a holdout. El sesgo de supervivencia por profundidad identificado en M16 sigue siendo un fenomeno observable en el rango de calibracion, pero el modelo cuantitativo basado en bootstrap no es transferible a rangos de n mayores.

## Implicaciones

1. **Nivel de novedad se mantiene en 2.5/5.** No sube a 3.
2. **El hallazgo M16 se reinterpreta:** el sesgo por profundidad se observa en train pero el modelo cuantitativo no generaliza. No es una correccion universal.
3. **La tendencia de cambio de signo del gap** es sugestiva pero no probada estadisticamente. Requeriria mas rangos de n para confirmar si es un patron real o variabilidad muestral.
4. **El arco M12-M17 queda cerrado.** Las hipotesis fueron testeadas con disciplina y descartadas o limitadas a su ambito de validez.

## Nota sobre lenguaje y claims

El revisor critico externo senalo correctamente que:
- "El gap cambia de signo" es una observacion, no un hecho estadisticamente robusto.
- "El modelo corregido empeora" es defendible en k=20 (CI no contiene 1.0) pero idealmente requeriria comparacion pareada.
- La descomposicion drift-por-profundidad no fue encontrada en la busqueda web realizada; eso no equivale a "nadie lo hizo". Es posible que exista en literatura no indexada o en formulaciones equivalentes bajo otro nombre.
- El mecanismo de "condicionar en sobrevivir d bloques cambia el drift" es un fenomeno conocido de random walks condicionados; lo propio del proyecto es haberlo medido en el contexto Collatz concreto.

## Recomendacion

Cerrar el arco de modelos estocasticos. Si el proyecto continua, las opciones son:

1. **Investigar la tendencia gap~log(n) con mas rangos:** requiere teoria, no solo mas datos.
2. **Cambio de direccion total:** inverse trees, potential cycles, L-functions, o formulaciones algebraicas.
3. **Cierre del proyecto** con documentacion de la metodologia de descarte disciplinado.

## Que no concluimos

- Que el resultado negativo invalida M16. M16 observo el sesgo en su rango.
- Que la tendencia gap~log(n) es un descubrimiento. Es una observacion en dos puntos.
- Que algo de esto acerca o aleja la prueba de Collatz.
- Que la descomposicion drift-por-profundidad sea original. Solo que no la encontramos en la busqueda.
