# Prefijos de paridad modulo 512 hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_parity_prefixes.py](../experiments/analyze_parity_prefixes.py)
Salida CSV: [parity_prefix_mod_512_limit_1000000.csv](parity_prefix_mod_512_limit_1000000.csv)

## Objetivo

Comparar la familia `-1 mod 2^k`, especialmente `511 mod 512`, contra clases control para ver si el promedio alto de pasos totales y stopping time se relaciona con prefijos de paridad.

## Clases comparadas

| Residuo mod 512 | Motivo |
| ---: | --- |
| 511 | `-1 mod 512`, clase candidata principal |
| 510 | clase par vecina, hereda estructura al dividir por 2 |
| 255 | `-1 mod 256` |
| 254 | control par de `255` |
| 127 | `-1 mod 128` |
| 126 | control par de `127` |
| 447, 283 | clases altas en promedios por residuos |
| 167, 155 | records puntuales de pasos y stopping time |
| 1, 0 | controles simples |

## Resumen

| Residuo | Promedio pasos | Promedio stopping time | Tasa impar primeros 16 | Tasa impar primeros 32 |
| ---: | ---: | ---: | ---: | ---: |
| 511 | 189.547875 | 59.422939 | 0.500000 | 0.430828 |
| 510 | 175.530466 | 1.000000 | 0.500000 | 0.409850 |
| 127 | 174.738351 | 46.279058 | 0.500000 | 0.409802 |
| 255 | 173.979007 | 46.601126 | 0.500000 | 0.409786 |
| 283 | 176.605223 | 46.612903 | 0.500000 | 0.409690 |
| 447 | 174.834613 | 46.881208 | 0.500000 | 0.409626 |
| 167 | 161.906298 | 34.831541 | 0.437500 | 0.389065 |
| 155 | 161.209421 | 34.250896 | 0.437500 | 0.388921 |
| 254 | 161.331797 | 1.000000 | 0.437500 | 0.388889 |
| 126 | 149.414235 | 1.000000 | 0.406234 | 0.368168 |
| 1 | 136.860287 | 3.000000 | 0.359199 | 0.347476 |
| 0 | 75.987711 | 1.000000 | 0.152394 | 0.232031 |

## Primeros 8 bits de paridad

| Residuo | Primeros 8 odd-rates |
| ---: | --- |
| 511 | `1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 1.000000 0.000000` |
| 510 | `0.000000 1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 1.000000` |
| 255 | `1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 1.000000 0.000000` |
| 127 | `1.000000 0.000000 1.000000 0.000000 1.000000 0.000000 1.000000 0.000000` |
| 1 | `0.999488 0.000000 0.000000 0.999488 0.000000 0.000000 0.999488 0.000000` |
| 0 | `0.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000 0.000000` |

## Lectura inicial

- Las clases `2^k - 1` muestran un prefijo determinista alternante `1,0,1,0...` en los primeros pasos de la funcion clasica.
- `511 mod 512` no solo comparte el promedio de 0.5 en los primeros 16 pasos; tambien conserva mas impares en los primeros 32 pasos que los controles principales.
- La clase `510 mod 512` tiene promedio alto de pasos totales, pero stopping time promedio `1` porque todo numero par baja inmediatamente por debajo de su valor inicial. Esto confirma que tiempo total y first descent deben analizarse por separado.
- El patron es compatible con la explicacion por cola binaria de unos / Mersenne tail, pero hace falta una derivacion formal para no sobrerreclamar.

## Hipotesis revisada

La ventaja estadistica de `2^k - 1 mod 2^k` parece venir de una estructura de paridad temprana muy rigida. No es un fenomeno nuevo, pero si puede cuantificarse de forma reproducible y compararse contra controles.

## Siguiente experimento

Medir la longitud efectiva del patron alternante y la primera excursion maxima para cada clase. En particular, comparar:

- `511`, `1023`, `2047` si se escala el modulo;
- controles pares `510`, `1022`, `2046`;
- clases altas no Mersenne como `447`, `283`, `239`.
