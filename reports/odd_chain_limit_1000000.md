# Cadena odd-to-odd por bloques alternantes hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_odd_chain.py](../experiments/analyze_odd_chain.py)
Salidas CSV:

- [odd_chain_limit_1000000_by_initial_tail.csv](odd_chain_limit_1000000_by_initial_tail.csv)
- [odd_chain_limit_1000000_blocks_to_stop.csv](odd_chain_limit_1000000_blocks_to_stop.csv)
- [odd_chain_limit_1000000_tail_transitions.csv](odd_chain_limit_1000000_tail_transitions.csv)
- [odd_chain_limit_1000000_records.csv](odd_chain_limit_1000000_records.csv)

## Objetivo

La sexta ola estudio un solo bloque:

```text
n = 2^s q - 1
e = 3^s q - 1
r = v2(e)
m = e / 2^r
```

Este reporte encadena ese salto entre impares:

```text
n_i -> n_{i+1}
```

y se detiene cuando `n_i < n_0`, cuando llega a `1`, o cuando supera el limite de bloques configurado.

La pregunta es si el bloque expansivo conserva estructura o si la salida mezcla la cola binaria y vuelve a un comportamiento casi generico.

## Comando reproducible

```powershell
python experiments\analyze_odd_chain.py --limit 1000000 --max-blocks 256 --out-dir reports --prefix odd_chain_limit_1000000
```

Rango medido:

```text
impares 3 <= n <= 1000000
```

Resultado global:

```text
maximo observado: 41 bloques odd-to-odd hasta bajar
casos maxed out: 0
```

## Resultado por cola inicial

| s inicial | Cantidad | Bloques promedio | Bloques expansivos promedio | Max cola promedio | Max impar/n promedio | Max pico/n promedio | Max bloques | Argmax bloques |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 249999 | 1.000000 | 0.000000 | 1.999832 | 1.000000 | 3.000013 | 1 | 5 |
| 2 | 125000 | 1.904776 | 0.758136 | 2.771344 | 1.967182 | 10.717955 | 41 | 626331 |
| 3 | 62500 | 2.311264 | 0.875248 | 3.481152 | 3.129403 | 18.857756 | 36 | 288615 |
| 4 | 31250 | 3.111968 | 1.352448 | 4.335584 | 5.320704 | 33.753527 | 41 | 667375 |
| 5 | 15625 | 3.756736 | 1.533888 | 5.211200 | 7.816798 | 51.386230 | 38 | 405407 |
| 6 | 7813 | 4.582491 | 1.893895 | 6.131320 | 14.102705 | 101.030774 | 38 | 270271 |
| 7 | 3906 | 5.283666 | 2.144649 | 7.071685 | 22.778853 | 173.858739 | 37 | 540543 |
| 8 | 1953 | 5.946237 | 2.328725 | 8.042499 | 36.171881 | 259.607361 | 37 | 401151 |
| 9 | 977 | 6.614125 | 2.513818 | 9.025589 | 39.772913 | 281.255882 | 34 | 528895 |
| 10 | 488 | 7.182377 | 2.668033 | 10.008197 | 45.545237 | 314.757991 | 33 | 437247 |
| 11 | 244 | 8.372951 | 3.077869 | 11.004098 | 72.444093 | 449.403736 | 31 | 206847 |
| 12 | 122 | 9.368852 | 3.319672 | 12.000000 | 130.527250 | 852.992984 | 31 | 847871 |

## Reset de cola entre bloques

Promedio de la siguiente cola `v2(n_{i+1} + 1)` condicionado por la cola actual:

| Cola actual | Transiciones | Siguiente cola promedio |
| ---: | ---: | ---: |
| 1 | 435942 | 1.999826 |
| 2 | 217672 | 1.998718 |
| 3 | 108620 | 2.001123 |
| 4 | 54347 | 2.002576 |
| 5 | 27123 | 1.997530 |
| 6 | 13680 | 1.995833 |
| 7 | 6918 | 2.001590 |
| 8 | 3473 | 2.016988 |
| 9 | 1635 | 2.026300 |
| 10 | 868 | 1.985023 |
| 11 | 395 | 1.997468 |
| 12 | 199 | 2.105528 |

La lectura fuerte es que, aun dentro de cadenas reales y no solo en el primer bloque, la siguiente cola vuelve a promedio cercano a `2`. Esto apoya la idea de "reseteo" o mezcla 2-adica despues de cada bloque.

## Records por cantidad de bloques

| Rank | n | s inicial | Bloques | Bloques expansivos | Colas largas | Max cola | Max impar/n | Max pico/n |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 626331 | 2 | 41 | 18 | 2 | 14 | 2882.774119 | 11531.096478 |
| 2 | 667375 | 4 | 41 | 17 | 0 | 8 | 924.574042 | 3698.296166 |
| 3 | 704623 | 4 | 40 | 17 | 2 | 14 | 2562.463611 | 10249.854444 |
| 4 | 270271 | 6 | 38 | 17 | 0 | 8 | 11399.705248 | 91197.641982 |
| 5 | 405407 | 5 | 38 | 17 | 0 | 8 | 7599.794125 | 60798.353003 |
| 6 | 540543 | 7 | 37 | 17 | 0 | 8 | 5699.842079 | 45598.736633 |
| 7 | 608111 | 4 | 37 | 17 | 0 | 8 | 5066.525251 | 40532.202009 |
| 8 | 687871 | 8 | 37 | 20 | 0 | 8 | 5124.923669 | 29188.041851 |

## Records por altura local

| Rank | n | s inicial | Bloques | Max cola | Max impar/n | Max pico/n |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 1 | 159487 | 8 | 14 | 13 | 13482.586161 | 107860.689285 |
| 2 | 270271 | 6 | 38 | 8 | 11399.705248 | 91197.641982 |
| 3 | 288615 | 3 | 36 | 8 | 10675.154573 | 85401.236582 |
| 4 | 704511 | 14 | 13 | 14 | 1578.200277 | 80895.093930 |
| 5 | 665215 | 7 | 31 | 10 | 5194.846128 | 78896.725588 |
| 6 | 239231 | 7 | 14 | 13 | 8988.371988 | 71906.975902 |
| 7 | 376831 | 14 | 32 | 14 | 8098.653818 | 64789.230546 |
| 8 | 405407 | 5 | 38 | 8 | 7599.794125 | 60798.353003 |

## Lectura

Hay dos dimensiones distintas:

- duracion antes del primer descenso;
- altura maxima alcanzada antes de ese descenso.

El numero `626331` fue record de duracion en esta medicion, con `41` bloques odd-to-odd, pero no fue el record de altura. El numero `159487` tuvo solo `14` bloques, pero alcanzo el mayor pico relativo observado.

Esto sugiere que no conviene buscar "dificultad Collatz" con una sola metrica. Hay orbitas que son largas sin ser las mas altas, y orbitas que explotan alto pero bajan relativamente rapido.

## Interpretacion prudente

El resultado apoya tres ideas:

- si `s = 1`, el siguiente impar baja inmediatamente para todo `n > 1`;
- las colas iniciales largas aumentan en promedio la cantidad de bloques y la excursion;
- despues de cada bloque, la cola siguiente parece volver a una distribucion casi generica.

No es una prueba de Collatz. Tampoco es evidencia suficiente para una publicacion por si sola. Pero si da una direccion concreta: estudiar productos de factores locales y correlaciones entre colas consecutivas, no solo residuos iniciales.

## Siguiente experimento

Conviene construir trazas detalladas para los records:

- `626331`: mas bloques hasta bajar;
- `159487`: mayor pico relativo;
- `270271`: alto en duracion y altura, conectado con records clasicos de excursion;
- `704623` y `704511`: cercanos pero con perfiles distintos.

Luego comparar esas trazas contra un modelo donde las colas son independientes y geometricas. Si aparece una desviacion sistematica, ahi podria haber una contribucion mas original.
