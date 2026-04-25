# Conlusion dinamica

Ultima actualizacion: 2026-04-25 02:45:03 -03:00
Tema activo: Collatz - Novena Ola cerrada

## Conlusion ejecutiva

La novena ola testeo si la dinamica real tiene anti-persistencia simple entre bloques expansivos.

Resultado:

| Fuente | Corr log_i, log_{i+1} | P exp despues de exp | Max racha expansiva |
| --- | ---: | ---: | ---: |
| Real | 0.003178993200 | 0.28551273 | 10 |
| Modelo | -0.002183105526 | 0.28606594 | 11 |

La hipotesis simple no se sostiene. Despues de un bloque expansivo, Collatz real no muestra una reduccion clara de la expansion siguiente frente al modelo independiente.

## Hallazgo nuevo

La senal mas interesante aparece condicionando por salida muy divisible:

```text
exit_v2 previo >= 5
```

| Fuente | Conteo | P siguiente expansivo | Promedio siguiente cola |
| --- | ---: | ---: | ---: |
| Real | 1458 | 0.23662551 | 1.89574760 |
| Modelo | 1425 | 0.28140351 | 2.00491228 |

Esto podria indicar un sesgo aritmetico despues de salidas con alta valuacion 2-adica. Todavia es muestra chica.

## Veredicto

No se probo Collatz. Y, mas importante, se descarto una explicacion demasiado simple.

La direccion prometedora ahora es:

> estudiar congruencias dejadas por `exit_v2` alto y comprobar si reducen la cola o expansion siguiente.

## Siguiente paso

Abrir una decima ola especializada en `exit_v2` alto:

- medir umbrales `exit_v2 >= k`;
- escalar o muestrear mas cadenas;
- calcular intervalos de confianza;
- derivar congruencias exactas de salida;
- buscar una afirmacion formalizable.
