# Comparacion con modelo geometrico independiente hasta 1000000

Fecha: 2026-04-25
Scripts:

- [experiments/trace_odd_records.py](../experiments/trace_odd_records.py)
- [experiments/compare_geometric_model.py](../experiments/compare_geometric_model.py)

Salidas CSV:

- [odd_record_traces.csv](odd_record_traces.csv)
- [odd_record_traces_summary.csv](odd_record_traces_summary.csv)
- [geometric_model_limit_1000000_summary.csv](geometric_model_limit_1000000_summary.csv)
- [geometric_model_limit_1000000_blocks.csv](geometric_model_limit_1000000_blocks.csv)
- [geometric_model_limit_1000000_tail_probabilities.csv](geometric_model_limit_1000000_tail_probabilities.csv)
- [geometric_model_limit_1000000_records.csv](geometric_model_limit_1000000_records.csv)

## Objetivo

La septima ola encontro que la cola siguiente `v2(n_{i+1} + 1)` vuelve a promedio cercano a `2`. La octava ola pregunta si esa mezcla alcanza para explicar la distribucion de bloques hasta el primer descenso.

Para eso se compara la cadena real odd-to-odd contra un modelo nulo simple:

```text
s_i ~ Geom(1/2),  P(s_i = k) = 2^-k
r_i ~ Geom(1/2),  P(r_i = k) = 2^-k
s_i y r_i independientes
```

Cada bloque artificial usa el factor logaritmico:

```text
log(n_{i+1}/n_i) = s_i log(3/2) - r_i log(2)
```

y se detiene cuando la suma acumulada cae por debajo de `0`, que corresponde a `n_i < n_0`.

## Comandos reproducibles

```powershell
python experiments\trace_odd_records.py --max-blocks 256 --out-dir reports --prefix odd_record_traces
python experiments\compare_geometric_model.py --limit 1000000 --max-blocks 256 --seed 20260425 --out-dir reports --prefix geometric_model_limit_1000000
```

Muestras:

```text
real: 499999 impares, 3 <= n <= 1000000
modelo: 499999 cadenas simuladas
seed: 20260425
```

## Resultado principal

| Fuente | Media bloques | Mediana | p90 | p99 | p999 | Max bloques | Max pico/n |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Real | 1.742153 | 1 | 3 | 10 | 20 | 41 | 107860.689285 |
| Modelo | 1.746125 | 1 | 3 | 10 | 21 | 54 | 2429179.311905 |

La coincidencia en media, mediana, p90 y p99 es muy fuerte. Esto sugiere que el modelo independiente captura gran parte del comportamiento grueso de los bloques odd-to-odd.

La diferencia aparece en los extremos: el modelo genera mas casos de cola muy larga y picos exagerados que la dinamica real observada hasta un millon.

## Probabilidades de cola

| Metrica | Umbral | Real | Modelo | Modelo/Real |
| --- | ---: | ---: | ---: | ---: |
| Bloques >= | 5 | 0.06032612 | 0.06039212 | 1.001094 |
| Bloques >= | 10 | 0.01246602 | 0.01273403 | 1.021498 |
| Bloques >= | 20 | 0.00114400 | 0.00123400 | 1.078671 |
| Bloques >= | 30 | 0.00011600 | 0.00017400 | 1.500000 |
| Bloques >= | 40 | 0.00000600 | 0.00003800 | 6.333333 |
| Max pico/n >= | 100 | 0.01229202 | 0.01250603 | 1.017410 |
| Max pico/n >= | 1000 | 0.00124000 | 0.00121400 | 0.979032 |
| Max pico/n >= | 10000 | 0.00012200 | 0.00014400 | 1.180328 |
| Max pico/n >= | 100000 | 0.00000200 | 0.00002600 | 13.000000 |

Lectura: el modelo nulo funciona muy bien hasta colas moderadas, pero parece demasiado permisivo con eventos extremadamente raros.

## Trazas de records reales

| n | Bloques | Pasos comprimidos | Bloques expansivos | Max cola | Max impar/n | Max pico/n | Terminal impar |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 626331 | 41 | 287 | 18 | 14 | 2882.774119 | 11531.096478 | 597017 |
| 667375 | 41 | 286 | 17 | 8 | 924.574042 | 3698.296166 | 212047 |
| 704623 | 40 | 282 | 17 | 14 | 2562.463611 | 10249.854444 | 597017 |
| 159487 | 14 | 123 | 5 | 13 | 13482.586161 | 107860.689285 | 1559 |
| 270271 | 38 | 273 | 17 | 8 | 11399.705248 | 91197.641982 | 2513 |
| 288615 | 36 | 255 | 17 | 8 | 10675.154573 | 85401.236582 | 2513 |
| 704511 | 13 | 119 | 5 | 14 | 1578.200277 | 80895.093930 | 661115 |
| 405407 | 38 | 271 | 17 | 8 | 7599.794125 | 60798.353003 | 2513 |

Las trazas muestran otra separacion util:

- `626331` y `667375` son records de duracion.
- `159487` es record de altura relativa, pero baja en solo `14` bloques.
- `270271`, `288615` y `405407` combinan duracion alta con altura alta.

## Interpretacion prudente

El modelo independiente no prueba nada, pero ahora cumple un rol importante: es un modelo nulo fuerte.

Si una futura medicion encuentra un patron, debe vencer esta vara:

- explicar algo que el modelo independiente no explique;
- producir una desviacion estable al cambiar rango o semilla;
- idealmente convertirse en una afirmacion formal sobre dependencia entre bloques.

Por ahora, el hallazgo es doble:

- la distribucion gruesa de bloques hasta descenso parece casi aleatoria bajo colas geometricas independientes;
- la dinamica real podria ser menos extrema que el modelo independiente en la cola muy rara.

## Posible explicacion de la diferencia extrema

El modelo artificial permite concatenar bloques favorables sin restricciones aritmeticas reales. En cambio, en Collatz:

- `q` no se reelige libremente despues de cada bloque;
- las congruencias de salida pueden inducir anti-persistencia;
- el descenso exacto puede cortar cadenas que el modelo logaritmico todavia dejaria vivas;
- el rango finito hasta `1000000` limita que extremos aparecen como valores iniciales.

No se puede afirmar todavia cual de estas causas domina.

## Siguiente experimento

La pregunta siguiente ya es mas fina:

> Existe anti-persistencia demostrable entre bloques expansivos?

Experimentos sugeridos:

- medir correlacion entre factores logaritmicos consecutivos;
- medir probabilidad real y modelada de `j` bloques expansivos consecutivos;
- condicionar por bloques con `s >= 8` y estudiar el siguiente factor;
- repetir la comparacion en rangos mayores solo si el costo sigue siendo razonable;
- buscar una desigualdad que limite cadenas de factores positivos.

Si aparece una diferencia robusta, podria ser el primer objeto realmente prometedor para formalizar.
