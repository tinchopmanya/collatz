# Prefijo alternante y excursion temprana modulo 512 hasta 1000000

Fecha: 2026-04-25
Script: [experiments/analyze_alternating_prefix.py](../experiments/analyze_alternating_prefix.py)
Salida CSV: [alternating_prefix_mod_512_limit_1000000.csv](alternating_prefix_mod_512_limit_1000000.csv)

## Objetivo

Medir si las clases residuales con promedios altos tienen una estructura inicial distinguible: longitud del prefijo alternante de paridad y crecimiento maximo dentro de los primeros 64 pasos.

## Resultado principal

| Residuo mod 512 | Longitud alternante promedio | Pico temprano promedio | Promedio pasos totales | Promedio stopping time |
| ---: | ---: | ---: | ---: | ---: |
| 511 | 19.993856 | 347.125344 | 189.547875 | 59.422939 |
| 510 | 18.993856 | 136.859853 | 175.530466 | 1.000000 |
| 255 | 16.000000 | 175.302741 | 173.979007 | 46.601126 |
| 254 | 15.000000 | 54.801260 | 161.331797 | 1.000000 |
| 127 | 14.000000 | 150.722211 | 174.738351 | 46.279058 |
| 126 | 13.000000 | 17.771604 | 149.414235 | 1.000000 |
| 447 | 12.000000 | 135.092082 | 174.834613 | 46.881208 |
| 167 | 6.000000 | 40.400781 | 161.906298 | 34.831541 |
| 155 | 4.000000 | 38.148436 | 161.209421 | 34.250896 |
| 283 | 4.000000 | 119.764531 | 176.605223 | 46.612903 |
| 1 | 2.000000 | 5.436926 | 136.860287 | 3.000000 |
| 0 | 1.000000 | 1.000190 | 75.987711 | 1.000000 |

## Lectura

- `511 mod 512` tiene la mayor longitud alternante promedio: casi 20 pasos.
- `510 mod 512` tambien tiene longitud alternante alta, pero su stopping time es 1 porque cada numero par baja inmediatamente por debajo de si mismo.
- Las clases `255`, `127` y sus controles pares muestran una escalera clara: al aumentar la cola binaria de unos, aumenta la longitud alternante inicial.
- `511 mod 512` tambien tiene el mayor pico temprano promedio dentro de los primeros 64 pasos.
- La diferencia entre `511` y `510` es especialmente util: comparten alternancia larga, pero solo la clase impar mantiene una bajada inicial no trivial.

## Interpretacion prudente

Este resultado da una explicacion computacional parcial del fenomeno `-1 mod 2^k`: las clases Mersenne-like inducen un prefijo de paridad muy rigido que provoca crecimiento temprano y retrasa la bajada. Esto coincide con la idea de Mersenne tails / trailing ones ya presente en la literatura.

No es una prueba de Collatz ni una familia nueva. Si es una medicion reproducible que conecta:

- clase residual;
- prefijo de paridad;
- excursion temprana;
- stopping time;
- pasos totales.

## Siguiente pregunta

Para convertir esto en un lemma pequeno, habria que demostrar formalmente algo del tipo:

> Si `n == -1 mod 2^k`, entonces los primeros pasos de paridad bajo el mapa clasico siguen un patron alternante durante una cantidad controlada de iteraciones, y eso implica una cota inferior explicita para la excursion temprana.

Luego habria que separar lo que ya es conocido de lo que nuestro laboratorio puede aportar como cuantificacion o visualizacion.
