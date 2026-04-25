# Conlusion dinamica

Ultima actualizacion: 2026-04-25 10:00:03 -03:00
Tema activo: Collatz - Duodecima Ola cerrada

## Preguntas antes de la iteracion

```text
Estoy en algo virgen?
No en el marco general. Stopping times, modelos probabilisticos, vectores de paridad, bloques de Mersenne y heterogeneidad modular ya estan estudiados.

Puedo descubrir algo con esto?
Si, pero como mecanismo experimental: distinguir seleccion global de dependencia aritmetica residual.

Ya alguien estuvo buscando esto?
Si a nivel amplio. Campbell 2025 y Bonacorsi/Bordoni 2026 trabajan ideas cercanas de bloques, mezcla y estructura modular.

Que tan lejos estoy de descubrir algo?
Lejos de una prueba. Cerca de aislar una falla concreta del modelo independiente.
```

## Hallazgo principal

La duodecima ola comparo cadenas reales hasta `n <= 5000000` contra un modelo geometrico independiente con la misma cantidad de cadenas.

Resultado global:

| Posicion | tail=1 real | tail=1 modelo | Diff | IC95 |
| --- | ---: | ---: | ---: | --- |
| `only_block` | 0.70054800 | 0.70110213 | -0.00055413 | [-0.00150428, 0.00039602] |
| `interior_block` | 0.38646876 | 0.38606060 | 0.00040816 | [-0.00085247, 0.00166879] |
| `final_block` | 0.68311110 | 0.68213098 | 0.00098012 | [-0.00054502, 0.00250526] |

El modelo independiente explica casi perfectamente el sesgo global por posicion final/interior.

Pero queda un residuo:

| Condicion | tail=1 real | tail=1 modelo | Diff tail=1 | IC95 | Exp real | Exp modelo | Diff exp |
| --- | ---: | ---: | ---: | --- | ---: | ---: | ---: |
| `prev_exit_v2 = 5` + interior | 0.45271454 | 0.40614137 | 0.04657317 | [0.02320157, 0.06994477] | 0.40834793 | 0.44814600 | -0.03979807 |

## Preguntas despues de la iteracion

```text
La originalidad cambio?
Si. El sesgo global no es una novedad; el residuo interior condicionado por `prev_exit_v2 = 5` es la parte interesante.

La probabilidad de relevancia subio?
Subio un poco: no todo se explico por bloques finales/interiores.

Senal robusta o seleccion?
Ambas. La seleccion global queda explicada por el modelo, pero queda una senal residual localizada.

Que aprendimos?
La falla del modelo independiente no esta en la supervivencia global, sino en dependencias condicionadas mas finas.

Seguir o abandonar?
Seguir, pero quirurgicamente: descomponer solo `prev_exit_v2 = 5` + interior por residuos, profundidad y margen.
```

## Siguiente paso

Abrir M14:

```text
Analizar `prev_exit_v2 = 5` + `interior_block` por clases residuales y margen.
```

La pregunta minima:

```text
que variable explica el exceso de next_tail = 1 en esa subpoblacion?
```
