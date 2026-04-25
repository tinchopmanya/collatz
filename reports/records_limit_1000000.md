# Records Collatz hasta 1000000

Fecha: 2026-04-25
Script: [experiments/generate_records.py](../experiments/generate_records.py)
Salida CSV: [records_limit_1000000.csv](records_limit_1000000.csv)

## Resultado

| Tipo de record | n | Pasos totales | Stopping time | Maximo alcanzado |
| --- | ---: | ---: | ---: | ---: |
| Tiempo total | 837799 | 524 | 171 | 2974984576 |
| Stopping time | 626331 | 508 | 287 | 7222283188 |
| Altura maxima | 704511 | 242 | 119 | 56991483520 |

## Lectura inicial

- `837799` confirma el record clasico de pasos totales dentro del primer millon.
- La altura maxima mas grande dentro del rango aparece en `704511`, no en `837799`.
- El mayor stopping time aparece en `626331`, que tarda mas en bajar por debajo de su valor inicial.
- La separacion entre estas tres metricas refuerza el foco del laboratorio: los extremos de Collatz no son un solo fenomeno.

## Siguiente experimento

Comparar estos tres records contra clases residuales modulo `2^k` y contra los prefijos de paridad de la poblacion general.
