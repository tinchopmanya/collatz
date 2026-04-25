# Residues modulo 128 hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_residues.py](../experiments/analyze_residues.py)
Salida CSV: [residue_mod_128_limit_1000000.csv](residue_mod_128_limit_1000000.csv)

## Records por clase

| Metrica | Residuo mod 128 | n | Valor |
| --- | ---: | ---: | ---: |
| Mayor tiempo total | 39 | 837799 | 524 pasos |
| Mayor stopping time | 27 | 626331 | 287 pasos |
| Mayor altura maxima | 127 | 704511 | 56991483520 |

## Top 10 por promedio de pasos totales

| Residuo | Promedio pasos totales | Maximo pasos | n del maximo |
| ---: | ---: | ---: | ---: |
| 127 | 175.590502 | 449 | 818943 |
| 126 | 162.593318 | 418 | 847358 |
| 63 | 162.559836 | 469 | 511935 |
| 41 | 162.415461 | 444 | 886953 |
| 31 | 162.275438 | 467 | 767903 |
| 27 | 161.926789 | 508 | 626331 |
| 111 | 161.248720 | 503 | 704623 |
| 103 | 160.810932 | 457 | 970599 |
| 71 | 150.874552 | 435 | 389191 |
| 47 | 150.370408 | 418 | 854191 |

## Top 10 por promedio de stopping time

| Residuo | Promedio stopping time | Maximo stopping time | n del maximo |
| ---: | ---: | ---: | ---: |
| 127 | 46.847670 | 272 | 401151 |
| 27 | 34.548957 | 287 | 626331 |
| 63 | 34.511967 | 267 | 270271 |
| 31 | 34.424805 | 282 | 381727 |
| 111 | 34.282514 | 285 | 667375 |
| 103 | 34.270225 | 269 | 362343 |
| 71 | 20.928315 | 225 | 495687 |
| 47 | 20.762703 | 223 | 434223 |
| 39 | 20.734801 | 215 | 756903 |
| 123 | 20.692780 | 189 | 569595 |

## Lectura inicial

- La senal de `127 mod 128` se fortalece al escalar de `100000` a `1000000`.
- `127` queda primero tanto por promedio de pasos totales como por promedio de stopping time.
- El record de altura maxima dentro del millon tambien cae en `127 mod 128`.
- Los records puntuales de pasos totales y stopping time caen en `39` y `27`, asi que la clase con mejor promedio no necesariamente contiene todos los records.

## Siguiente experimento

Refinar `127 mod 128` con modulo `256` para ver si se concentra en una subclase.
