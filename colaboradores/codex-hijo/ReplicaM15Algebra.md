# Replica M15 algebra

Fecha: 2026-04-25
Rama: `codex-hijo/m15-algebra-replica`

## Alcance

Replica independiente del calculo teorico de `P(next_tail | q mod 8)`.

No usa holdout, no usa rangos de datos, no busca variables nuevas y no afirma
ninguna prueba de Collatz.

Definiciones usadas:

```text
n = 2^s q - 1, con s = tail = v2(n + 1) y q impar
a = 3^s q
exit_v2 = v2(a - 1)
next_odd = (a - 1) / 2^exit_v2
next_tail = v2(next_odd + 1)
```

## Metodo

Para un impar `n` uniforme en sentido 2-adico:

```text
P(s = k) = 2^-k, k >= 1
P(s impar) = 2/3
P(s par) = 1/3
```

Condicionado por `q mod 8 = r`, la clase fuente
`a = 3^s q mod 8` es:

```text
s impar: a = 3r mod 8
s par:   a = r mod 8
```

Luego se enumera la clase fuente `a mod 8`:

| `a mod 8` | `P(next_tail = 1)` | geometrica |
| ---: | ---: | ---: |
| `1` | `1/2` | `1/2` |
| `3` | `1` | `1/2` |
| `5` | `1/2` | `1/2` |
| `7` | `0` | `1/2` |

Detalles:

- `a = 3 mod 8`: `exit_v2 = 1` y el odd part es `1 mod 4`, entonces `next_tail = 1` siempre.
- `a = 7 mod 8`: `exit_v2 = 1` y el odd part es `3 mod 4`, entonces `next_tail = 1` nunca.
- `a = 5 mod 8`: `exit_v2 = 2`; el odd part queda uniforme impar, por eso la ley es geometrica.
- `a = 1 mod 8`: se suma sobre `exit_v2 >= 3`; condicionado por cada salida exacta, el odd part queda uniforme impar, por eso la ley vuelve a ser geometrica.

## Resultado por `q mod 4`

Agrupar modulo 4 promedia las dos clases modulo 8 y cancela el sesgo.

| `q mod 4` | `P(next_tail = 1)` | `P(next_tail = 2)` | coincide con geometrica |
| ---: | ---: | ---: | :---: |
| `1` | `1/2` | `1/4` | `si` |
| `3` | `1/2` | `1/4` | `si` |

Conclusion: si, `q mod 4` coincide con la ley geometrica
`P(next_tail = t) = 2^-t`.

## Resultado por `q mod 8`

| `q mod 8` | `P(next_tail = 1)` | para `t >= 2` |
| ---: | ---: | ---: |
| `1` | `5/6` | `1/3 * 2^-t` |
| `3` | `2/3` | `2/3 * 2^-t` |
| `5` | `1/6` | `5/3 * 2^-t` |
| `7` | `1/3` | `4/3 * 2^-t` |

En particular:

```text
q = 1 mod 8 -> P(next_tail = 1) = 5/6
q = 3 mod 8 -> P(next_tail = 1) = 2/3
q = 5 mod 8 -> P(next_tail = 1) = 1/6
q = 7 mod 8 -> P(next_tail = 1) = 1/3
```

Las cuatro predicciones son correctas bajo este modelo 2-adico local.

## Interpretacion

`q mod 8` no coincide con la geometrica clase por clase. La desviacion no
requiere datos: sale de que `3^s mod 8` depende de la paridad de `s`, y esa
paridad no pesa `1/2`-`1/2`, sino `2/3`-`1/3`.

`q mod 4` si coincide con la geometrica porque mezcla pares de clases modulo 8:

```text
q = 1 mod 4: promedio de 5/6 y 1/6 = 1/2
q = 3 mod 4: promedio de 2/3 y 1/3 = 1/2
```

El CSV derivado esta en:

```text
reports/m15_algebra_replica_summary.csv
```

## Comparacion con Codex hijo 1

Despues de cerrar esta replica, inspeccione:

```text
origin/codex-hijo/m15-algebra:experiments/analyze_m15_algebra.py
origin/codex-hijo/m15-algebra:colaboradores/codex-hijo/ResultadosM15Algebra.md
origin/codex-hijo/m15-algebra:reports/m15_algebra_summary.csv
```

Coincidencias:

- `q mod 4`: Codex hijo 1 reporta `K = 2`, `classes_deviating_from_geometric = 0 / 2`. Esta replica obtiene ley geometrica exacta para las dos clases.
- `q mod 8`: Codex hijo 1 reporta desviacion en `4 / 4` clases, con maximo `1/3` en residuo `1`, `next_tail = 1`. Esta replica obtiene la misma tabla baja:

```text
q = 1 mod 8 -> P(next_tail = 1) = 5/6
q = 3 mod 8 -> P(next_tail = 1) = 2/3
q = 5 mod 8 -> P(next_tail = 1) = 1/6
q = 7 mod 8 -> P(next_tail = 1) = 1/3
```

No encontre discrepancia en el resultado `q mod 8`. La diferencia es de
alcance: Codex hijo 1 tambien explora refinamientos `q mod 16..64` y
`n mod 2^K`; esta replica se limita al calculo pedido para `q mod 4` y
`q mod 8`.
