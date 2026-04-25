# Residues modulo 512 hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_residues.py](../experiments/analyze_residues.py)
Salida CSV: [residue_mod_512_limit_1000000.csv](residue_mod_512_limit_1000000.csv)

## Records por clase

| Metrica | Residuo mod 512 | n | Valor |
| --- | ---: | ---: | ---: |
| Mayor tiempo total | 167 | 837799 | 524 pasos |
| Mayor stopping time | 155 | 626331 | 287 pasos |
| Mayor altura maxima | 511 | 704511 | 56991483520 |

## Top 12 por promedio de pasos totales

| Residuo | Promedio pasos totales | Maximo pasos | n del maximo |
| ---: | ---: | ---: | ---: |
| 511 | 189.547875 | 418 | 847359 |
| 283 | 176.605223 | 475 | 910107 |
| 510 | 175.530466 | 418 | 847358 |
| 447 | 174.834613 | 469 | 511935 |
| 127 | 174.738351 | 441 | 665215 |
| 169 | 174.709677 | 444 | 886953 |
| 255 | 173.979007 | 449 | 818943 |
| 239 | 173.732207 | 431 | 919791 |
| 159 | 172.897593 | 444 | 938143 |
| 359 | 172.460829 | 457 | 970599 |
| 415 | 164.611367 | 467 | 767903 |
| 382 | 164.096774 | 407 | 526206 |

## Top 12 por promedio de stopping time

| Residuo | Promedio stopping time | Maximo stopping time | n del maximo |
| ---: | ---: | ---: | ---: |
| 511 | 59.422939 | 251 | 376831 |
| 447 | 46.881208 | 267 | 270271 |
| 283 | 46.612903 | 264 | 543515 |
| 255 | 46.601126 | 272 | 401151 |
| 127 | 46.279058 | 269 | 601727 |
| 239 | 46.221198 | 285 | 667375 |
| 159 | 45.977983 | 181 | 927391 |
| 359 | 45.905786 | 269 | 362343 |
| 383 | 35.087558 | 264 | 540543 |
| 27 | 34.883316 | 207 | 824347 |
| 167 | 34.831541 | 215 | 756903 |
| 47 | 34.829069 | 223 | 434223 |

## Lectura inicial

- La familia `-1 mod 2^k` vuelve a quedar primera: `511 mod 512` lidera por promedio de pasos totales y por promedio de stopping time.
- `511 mod 512` tambien contiene el record de altura maxima dentro de `n <= 1000000`.
- El record puntual de pasos totales (`837799`) y el record puntual de stopping time (`626331`) no caen en `511`; esto separa "clase alta en promedio" de "record puntual".
- La senal `127 -> 255 -> 511` es ahora una hipotesis concreta para escalar, no una prueba.

## Hipotesis candidata

Los numeros congruentes con `-1 mod 2^k` tienen promedios altos de pasos totales y stopping time porque empiezan con una estructura binaria de muchos unos, lo que podria inducir prefijos de paridad y subidas tempranas mas largas que el promedio.

## Siguiente experimento

Medir prefijos de paridad y primeras excursiones para clases `511`, `255`, `127`, `447`, `283` y comparar contra clases pares cercanas como `510`.
