# Anti-persistencia entre bloques odd-to-odd hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_antipersistence.py](../experiments/analyze_antipersistence.py)
Salidas CSV:

- [antipersistence_limit_1000000_summary.csv](antipersistence_limit_1000000_summary.csv)
- [antipersistence_limit_1000000_conditional.csv](antipersistence_limit_1000000_conditional.csv)
- [antipersistence_limit_1000000_runs.csv](antipersistence_limit_1000000_runs.csv)

## Objetivo

La octava ola mostro que el modelo geometrico independiente explica muy bien el cuerpo de la distribucion, pero sobreproduce algunos extremos. La hipotesis siguiente fue:

> Tal vez Collatz real tiene anti-persistencia: despues de un bloque expansivo, el siguiente bloque seria menos expansivo que en el modelo independiente.

Este reporte mide esa hipotesis directamente.

## Comando reproducible

```powershell
python experiments\analyze_antipersistence.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix antipersistence_limit_1000000
```

Muestras:

```text
real: 499999 cadenas
modelo: 499999 cadenas
seed: 20260425
```

## Resultado principal

| Fuente | Bloques | Pares consecutivos | Fraccion expansiva | Media log factor | Corr log_i, log_{i+1} | Max racha expansiva |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Real | 871075 | 371076 | 0.28559768 | -0.577242880888 | 0.003178993200 | 10 |
| Modelo | 873061 | 373062 | 0.28616672 | -0.574952408102 | -0.002183105526 | 11 |

La correlacion entre factores consecutivos es casi cero en ambos casos. No aparece anti-persistencia lineal de primer orden.

## Expansion despues de expansion

| Fuente | P(siguiente expansivo despues de expansivo) | P(siguiente expansivo despues de no expansivo) |
| --- | ---: | ---: |
| Real | 0.28551273 | 0.28302766 |
| Modelo | 0.28606594 | 0.28614441 |

Esto refuta, al menos hasta `n <= 1000000`, la hipotesis simple:

```text
bloque expansivo -> siguiente bloque menos expansivo
```

En la cadena real, despues de un bloque expansivo la probabilidad de otra expansion no baja de forma relevante.

## Rachas de bloques expansivos

| Max racha expansiva | Real | Modelo |
| ---: | ---: | ---: |
| 0 | 0.71373143 | 0.71377743 |
| 1 | 0.19620439 | 0.19620639 |
| 2 | 0.06236812 | 0.06245412 |
| 3 | 0.01961404 | 0.01959804 |
| 4 | 0.00571201 | 0.00556801 |
| 5 | 0.00172400 | 0.00169800 |
| 6 | 0.00046000 | 0.00050600 |
| 7 | 0.00015200 | 0.00013000 |
| 8 | 0.00002000 | 0.00004400 |
| 9 | 0.00000600 | 0.00001000 |
| 10 | 0.00000800 | 0.00000600 |
| 11 | 0.00000000 | 0.00000200 |

Las rachas expansivas tambien se parecen mucho al modelo. Si hay una diferencia importante en extremos, no se explica simplemente por una reduccion visible de rachas expansivas.

## Condicionamientos

| Condicion previa | Fuente | Conteo | P siguiente expansivo | Promedio siguiente log | Promedio siguiente cola |
| --- | --- | ---: | ---: | ---: | ---: |
| bloque expansivo | Real | 248777 | 0.28551273 | -0.576785435974 | 1.99901518 |
| bloque expansivo | Modelo | 249841 | 0.28606594 | -0.577062679125 | 1.99862312 |
| cola previa >= 8 | Real | 6540 | 0.29159021 | -0.573229542248 | 2.01284404 |
| cola previa >= 8 | Modelo | 6475 | 0.28586873 | -0.589841778924 | 2.00864865 |
| exit_v2 previo >= 5 | Real | 1458 | 0.23662551 | -0.621436756799 | 1.89574760 |
| exit_v2 previo >= 5 | Modelo | 1425 | 0.28140351 | -0.566562519441 | 2.00491228 |

El unico condicionamiento que parece desviarse de forma interesante es `exit_v2 previo >= 5`. En la cadena real, despues de una salida muy divisible por `2`, el siguiente bloque parece menos expansivo y con cola promedio menor.

Pero la muestra es chica: `1458` pares reales. Esto todavia no alcanza para afirmar una ley.

## Interpretacion

La hipotesis inicial se debilita:

- no hay correlacion lineal significativa entre factores consecutivos;
- no baja la expansion despues de expansion;
- las rachas expansivas reales y modeladas son casi iguales.

La nueva hipotesis fina es:

> la dependencia no estaria ligada a "expansion previa", sino a salidas con alta valuacion `exit_v2`.

Esto tiene sentido como pista aritmetica: una salida muy divisible por `2` impone una congruencia fuerte sobre el siguiente impar, y esa congruencia podria sesgar la cola siguiente.

## Veredicto

No se encontro anti-persistencia de primer orden. Esta es una buena noticia metodologica: evita perseguir una explicacion demasiado simple.

El mejor hilo nuevo es condicionar por `exit_v2` alto y escalar esa medicion. Si el sesgo persiste en rangos mayores, podria transformarse en una afirmacion formal sobre congruencias de salida.

## Siguiente experimento

Conviene abrir una etapa especializada:

- medir `exit_v2 >= k` para varios `k`;
- aumentar rango o muestrear mas cadenas;
- calcular intervalos de confianza;
- derivar la congruencia que deja `exit_v2 >= k`;
- estudiar si esa congruencia fuerza menor cola siguiente.
