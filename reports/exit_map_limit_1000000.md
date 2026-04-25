# Mapa de salida del bloque alternante hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_exit_map.py](../experiments/analyze_exit_map.py)
Salidas CSV:

- [exit_map_limit_1000000_by_tail.csv](exit_map_limit_1000000_by_tail.csv)
- [exit_map_limit_1000000_exit_v2.csv](exit_map_limit_1000000_exit_v2.csv)
- [exit_map_limit_1000000_transitions.csv](exit_map_limit_1000000_transitions.csv)

## Objetivo

La quinta ola formalizo el bloque alternante inicial. Para un impar positivo:

```text
n = 2^s q - 1
s = v2(n + 1)
q impar
```

el bloque alternante termina en:

```text
C^(2s)(n) = 3^s q - 1
```

Este reporte mide que ocurre inmediatamente despues. Definimos:

```text
r = v2(3^s q - 1)
m = (3^s q - 1) / 2^r
```

donde `m` es el siguiente impar despues del bloque y las divisiones pares forzadas.

## Comando reproducible

```powershell
python experiments\analyze_exit_map.py --limit 1000000 --out-dir reports --prefix exit_map_limit_1000000
```

## Resultado por longitud de cola

| s = v2(n+1) | Cantidad | Promedio r | Promedio siguiente cola | Fraccion con m > n | Promedio pico/n | Promedio m/n |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 250000 | 1.999988 | 1.999828 | 0.000000 | 3.000017 | 0.500003 |
| 2 | 125000 | 2.000032 | 1.999856 | 0.500000 | 4.500036 | 0.750006 |
| 3 | 62500 | 2.000016 | 1.999984 | 0.500000 | 6.750063 | 1.125010 |
| 4 | 31250 | 2.000000 | 2.000224 | 0.749984 | 10.125101 | 1.687500 |
| 5 | 15625 | 2.000000 | 2.000320 | 0.750016 | 15.187654 | 2.531368 |
| 6 | 7813 | 1.999744 | 2.001024 | 0.874952 | 22.781478 | 3.796533 |
| 7 | 3906 | 1.999488 | 1.999488 | 0.937276 | 34.172205 | 5.694778 |
| 8 | 1953 | 2.003584 | 2.000000 | 0.937020 | 51.258283 | 8.539120 |
| 9 | 977 | 1.997953 | 2.008188 | 0.968270 | 76.887381 | 12.820983 |
| 10 | 488 | 1.997951 | 1.997951 | 0.969262 | 115.331003 | 19.223700 |
| 11 | 244 | 1.995902 | 2.024590 | 0.983607 | 172.996394 | 28.827442 |
| 12 | 122 | 2.008197 | 2.098361 | 0.991803 | 259.494420 | 43.117461 |

## Distribucion de r

| r = v2(3^s q - 1) | Cantidad | Fraccion |
| ---: | ---: | ---: |
| 1 | 250001 | 0.500002 |
| 2 | 124996 | 0.249992 |
| 3 | 62500 | 0.125000 |
| 4 | 31253 | 0.062506 |
| 5 | 15626 | 0.031252 |
| 6 | 7813 | 0.015626 |
| 7 | 3904 | 0.007808 |
| 8 | 1952 | 0.003904 |
| 9 | 979 | 0.001958 |
| 10 | 489 | 0.000978 |
| 11 | 246 | 0.000492 |
| 12 | 120 | 0.000240 |

La distribucion observada es casi exactamente:

```text
P(r = k) = 2^-k
```

Esto no parece accidental. Para `s` fijo, `3^s` es invertible modulo `2^k`, y entre los `q` impares la congruencia:

```text
3^s q == 1 mod 2^k
```

selecciona una clase residual. Por densidad natural:

```text
P(r >= k) = 2^-(k-1)
P(r = k) = 2^-k
E[r] = 2
```

## Lectura principal

El bloque alternante produce expansion aproximada:

```text
pico/n ~= 2 * (3/2)^s
```

Despues de dividir por `2^r`, el siguiente impar tiene razon aproximada:

```text
m/n ~= (3/2)^s / 2^r
```

Como `r` tiene distribucion geometrica con `P(r = k) = 2^-k`, se espera:

```text
E[2^-r] = 1/3
E[m/n | s] ~= (3/2)^s / 3
```

Para `s = 9`, esto predice:

```text
(3/2)^9 / 3 ~= 12.814
```

El valor medido fue:

```text
12.820983
```

La fraccion de casos con crecimiento `m > n` tambien queda bien aproximada por el umbral:

```text
(3/2)^s / 2^r > 1
```

equivalentemente:

```text
r < s * log2(3/2)
```

Esto explica por que la fraccion de crecimiento sube con `s`: `0.5`, `0.75`, `0.875`, `0.9375`, etc.

## Interpretacion prudente

Este resultado no prueba Collatz y tampoco sugiere por si solo divergencia. Lo que muestra es mas fino:

- una cola binaria larga de unos fuerza un bloque expansivo;
- la salida par de ese bloque suele tener una valuacion 2-adica pequena;
- por eso la expansion local normalmente sobrevive hasta el siguiente impar cuando `s` es grande;
- pero la siguiente cola `v2(m + 1)` vuelve a promedio cercano a `2`, como un impar generico.

La parte interesante no es solamente que haya expansion. Es que la expansion local parece resetear la cola en lugar de conservarla. La dificultad global de Collatz podria verse como una competencia entre episodios raros de cola larga y muchos bloques genericos que contraen o mezclan.

## Siguiente experimento

Conviene pasar del bloque inicial a una cadena odd-to-odd:

```text
n_i = 2^s q - 1
n_{i+1} = (3^s q - 1) / 2^r
```

y medir:

- correlacion entre `s_i` y `s_{i+1}`;
- distribucion de productos locales `n_{i+1}/n_i`;
- frecuencia de multiples colas largas consecutivas;
- diferencias entre datos reales y un modelo independiente con colas geometricas;
- numeros que logran varios bloques expansivos antes del primer descenso.

Ese es el proximo borde razonable para buscar algo publicable: no una prueba global todavia, sino una descripcion cuantitativa de la dinamica por bloques.
