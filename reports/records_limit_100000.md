# Records Collatz hasta 100000

Fecha: 2026-04-25
Script: [experiments/generate_records.py](../experiments/generate_records.py)
Salida CSV: [records_limit_100000.csv](records_limit_100000.csv)

## Resultado

| Tipo de record | n | Pasos totales | Stopping time | Maximo alcanzado |
| --- | ---: | ---: | ---: | ---: |
| Tiempo total | 77031 | 350 | 145 | 21933016 |
| Stopping time | 35655 | 323 | 220 | 41163712 |
| Altura maxima | 77671 | 231 | 171 | 1570824736 |

## Lectura inicial

- En este rango, el numero con mas pasos totales no coincide con el de mayor altura maxima.
- El record de stopping time tambien es distinto del record de pasos totales.
- Esto justifica separar metricas: una orbita puede tardar mucho, bajar tarde o subir muy alto por razones distintas.

## Siguiente experimento

Escalar a `n <= 1_000_000` y comparar si los records nuevos mantienen firmas parecidas en prefijos de paridad y clases residuales.
