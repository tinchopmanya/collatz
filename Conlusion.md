# Conlusion dinamica

Ultima actualizacion: 2026-04-25 02:40:15 -03:00
Tema activo: Collatz - Octava Ola cerrada

## Conlusion ejecutiva

La octava ola comparo las cadenas reales odd-to-odd contra un modelo geometrico independiente:

```text
s ~ Geom(1/2)
r ~ Geom(1/2)
log factor = s log(3/2) - r log(2)
```

El modelo ignora la aritmetica exacta y solo conserva la distribucion esperada de colas y divisiones de salida.

## Hallazgo principal

El modelo explica muy bien el cuerpo de la distribucion:

| Fuente | Media bloques | p90 | p99 | p999 | Max bloques |
| --- | ---: | ---: | ---: | ---: | ---: |
| Real | 1.742153 | 3 | 10 | 20 | 41 |
| Modelo | 1.746125 | 3 | 10 | 21 | 54 |

Pero sobreproduce extremos:

- `bloques >= 40`: real `3` casos, modelo `19`;
- `max pico/n >= 100000`: real `1` caso, modelo `13`;
- max pico real: `107860.689285`;
- max pico modelo: `2429179.311905`.

## Veredicto

No se probo Collatz. Pero tenemos una vara nueva y util:

> cualquier patron candidato debe explicar algo que el modelo geometrico independiente no explique.

La direccion prometedora ya no es buscar numeros raros a ciegas, sino estudiar por que la dinamica real parece menos extrema que el modelo independiente en la cola muy rara.

## Siguiente paso

Abrir una novena ola sobre anti-persistencia:

- medir correlacion entre factores logaritmicos consecutivos;
- medir rachas de bloques expansivos reales contra modelo;
- condicionar por `s >= 8` y ver que pasa despues;
- buscar una desigualdad o sesgo aritmetico que limite concatenaciones favorables.
