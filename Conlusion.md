# Conlusion dinamica

Ultima actualizacion: 2026-04-25 10:57:05 -03:00
Tema activo: Collatz - Decimotercera Ola cerrada

## Preguntas antes de la iteracion

```text
Estoy en algo virgen?
No. Estamos en modelos probabilisticos, supervivencia orbital, bloques Mersenne y stopping times, todos cercanos a literatura existente.

Puedo descubrir algo con esto?
Si: confirmar una dependencia fina o descartarla limpiamente.

Ya alguien estuvo buscando esto?
Si a nivel amplio. La parte propia era la celda post-hoc `prev_exit_v2 = 5` + interior.

Que tan lejos estoy de descubrir algo?
Lejos de una prueba. Esta iteracion era metodologica: evitar perseguir una senal falsa.
```

## Hallazgo principal

M14 fue sometido a prueba de destruccion.

En el rango original:

| Medida | Valor |
| --- | ---: |
| Real | `1551 / 3426 = 0.45271454` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff | `0.04657317` |
| p crudo | `0.0000939371` |
| Bonferroni M13 | `0.01390268` |
| Bonferroni conservador | `0.06519232` |
| bootstrap CI95 | `[0.02364649, 0.06933110]` |

En holdout independiente:

| Medida | Valor |
| --- | ---: |
| Rango | `5000001 <= n <= 10000000` |
| Real | `1380 / 3321 = 0.41553749` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff | `0.00939612` |
| p crudo | `0.43201832` |
| bootstrap CI95 | `[-0.01423070, 0.03272495]` |

Conclusion:

```text
El residuo `prev_exit_v2 = 5` + interior no sobrevive confirmacion independiente.
```

## Preguntas despues de la iteracion

```text
La originalidad cambio?
Si, a la baja. La pista no queda como hallazgo.

La probabilidad de relevancia subio?
Bajo. La senal exploratoria no se reprodujo.

Senal robusta o descarte?
Descarte limpio para la afirmacion real-modelo original.

Que aprendimos?
Claude tenia razon: sin holdout, una celda post-hoc puede parecer mucho mas fuerte de lo que es.

Seguir o abandonar?
Abandonar `prev_exit_v2 = 5` + interior como pista principal.
```

## Siguiente paso

M15 debe cambiar el metodo:

```text
buscar senales con train/holdout desde el inicio.
```

Regla nueva:

```text
ninguna senal post-hoc pasa a milestone fuerte sin holdout o test pre-registrado.
```
