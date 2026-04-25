# Residues modulo 128 hasta 100000

Fecha: 2026-04-25
Script: [experiments/analyze_residues.py](../experiments/analyze_residues.py)
Salida CSV: [residue_mod_128_limit_100000.csv](residue_mod_128_limit_100000.csv)

## Records por clase

| Metrica | Residuo mod 128 | n | Valor |
| --- | ---: | ---: | ---: |
| Mayor tiempo total | 103 | 77031 | 350 pasos |
| Mayor stopping time | 71 | 35655 | 220 pasos |
| Mayor altura maxima | 103 | 77671 | 1570824736 |

## Top 10 por promedio de pasos totales

| Residuo | Promedio pasos totales | Maximo pasos | n del maximo |
| ---: | ---: | ---: | ---: |
| 127 | 148.943662 | 311 | 68479 |
| 63 | 139.107554 | 311 | 70335 |
| 31 | 137.881074 | 321 | 56095 |
| 41 | 137.790013 | 324 | 74793 |
| 111 | 136.960307 | 306 | 77039 |
| 126 | 135.567222 | 311 | 68478 |
| 27 | 134.686701 | 329 | 63387 |
| 103 | 133.654289 | 350 | 77031 |
| 9 | 128.122762 | 327 | 99721 |
| 71 | 127.992318 | 337 | 78791 |

## Top 10 por promedio de stopping time

| Residuo | Promedio stopping time | Maximo stopping time | n del maximo |
| ---: | ---: | ---: | ---: |
| 127 | 45.883483 | 205 | 37503 |
| 63 | 34.898848 | 202 | 56255 |
| 111 | 34.396927 | 148 | 94959 |
| 31 | 34.271100 | 197 | 84383 |
| 27 | 34.228900 | 200 | 57115 |
| 103 | 33.311140 | 171 | 10087 |
| 123 | 20.911652 | 127 | 33019 |
| 95 | 20.882202 | 114 | 42463 |
| 39 | 20.816901 | 119 | 18599 |
| 47 | 20.791293 | 207 | 60975 |

## Lectura inicial

- Las clases `127`, `63` y `31` aparecen arriba por promedio de pasos totales y por promedio de stopping time.
- Esa familia merece mirarse con cuidado porque son residuos cercanos a `-1` modulo potencias de 2.
- El record puntual de pasos totales y altura maxima cae en residuo `103`, asi que promedio alto y extremo puntual no son la misma cosa.
- Este resultado todavia es exploratorio: falta repetir con `n <= 1_000_000` y con otros modulos antes de tratarlo como senal estable.

## Siguiente experimento

Repetir para modulo `256` y `512`, y comparar si las clases altas son refinamientos de `127`, `63`, `31` o si el patron se diluye.
