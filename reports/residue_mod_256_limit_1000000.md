# Residues modulo 256 hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_residues.py](../experiments/analyze_residues.py)
Salida CSV: [residue_mod_256_limit_1000000.csv](residue_mod_256_limit_1000000.csv)

## Records por clase

| Metrica | Residuo mod 256 | n | Valor |
| --- | ---: | ---: | ---: |
| Mayor tiempo total | 167 | 837799 | 524 pasos |
| Mayor stopping time | 155 | 626331 | 287 pasos |
| Mayor altura maxima | 255 | 704511 | 56991483520 |

## Top 12 por promedio de pasos totales

| Residuo | Promedio pasos totales | Maximo pasos | n del maximo |
| ---: | ---: | ---: | ---: |
| 255 | 181.763441 | 449 | 818943 |
| 127 | 169.417563 | 441 | 665215 |
| 169 | 169.128008 | 444 | 886953 |
| 191 | 169.041987 | 469 | 511935 |
| 159 | 168.754480 | 467 | 767903 |
| 27 | 168.693371 | 475 | 910107 |
| 254 | 168.431132 | 418 | 847358 |
| 103 | 166.972094 | 457 | 970599 |
| 239 | 166.615463 | 431 | 919791 |
| 71 | 157.196877 | 435 | 389191 |
| 82 | 156.976959 | 410 | 720722 |
| 83 | 156.976959 | 410 | 720723 |

## Top 12 por promedio de stopping time

| Residuo | Promedio stopping time | Maximo stopping time | n del maximo |
| ---: | ---: | ---: | ---: |
| 255 | 53.012033 | 272 | 401151 |
| 191 | 40.823349 | 267 | 270271 |
| 27 | 40.746609 | 264 | 543515 |
| 127 | 40.683308 | 269 | 601727 |
| 159 | 40.190732 | 264 | 405407 |
| 239 | 40.188940 | 285 | 667375 |
| 103 | 40.109319 | 269 | 362343 |
| 71 | 28.856631 | 225 | 495687 |
| 31 | 28.660353 | 282 | 381727 |
| 47 | 28.523420 | 223 | 434223 |
| 167 | 28.471582 | 215 | 756903 |
| 231 | 28.431132 | 225 | 856551 |

## Lectura inicial

- Al pasar de modulo `128` a modulo `256`, la clase fuerte `127 mod 128` se refina principalmente en `255 mod 256`.
- `255 mod 256` queda primero por promedio de pasos totales y por promedio de stopping time.
- El record de altura maxima del millon tambien cae en `255 mod 256`.
- Esto sugiere una familia candidata cercana a `-1 mod 2^k`, pero todavia no prueba estabilidad para modulos mayores ni rangos mayores.

## Siguiente experimento

Repetir con modulo `512`, y luego comparar prefijos de paridad de las clases `255`, `127`, `191`, `159` y `239`.
