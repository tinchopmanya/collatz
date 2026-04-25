# Replica M15 - transicion `q mod 8`

Fecha: 2026-04-25
Rama: `codex-hijo/m15-qmod8-transition-replica`

## Comando reproducible

```powershell
python experiments\replicate_m15_qmod8_transition.py --limit 5000000 --out-dir reports --prefix m15_qmod8_transition_replica
```

Tambien verifique compilacion con:

```powershell
python -m py_compile experiments\replicate_m15_qmod8_transition.py
```

## Definicion replicada

Use la definicion de `q` del proyecto:

```text
s_i = v2(n_i + 1)
q_i = (n_i + 1) / 2^s_i
n_{i+1} = (3^s_i q_i - 1) / 2^v2(3^s_i q_i - 1)
q_{i+1} = (n_{i+1} + 1) / 2^v2(n_{i+1} + 1)
```

La implementacion de replica no importa `collatz.alternating_block`; calcula
`v2`, `q` y el paso odd-to-odd directamente desde la formula. No encontre en
los documentos una segunda definicion razonable de `q`; `n mod 8` seria otra
variable, no otra definicion de `q`.

Poblacion:

```text
impares 3 <= n <= 5000000
una transicion odd-to-odd por impar inicial
sin holdout fresco
```

## Archivos

- `experiments/replicate_m15_qmod8_transition.py`
- `reports/m15_qmod8_transition_replica_matrix.csv`
- `reports/m15_qmod8_transition_replica_stationary.csv`
- `reports/m15_qmod8_transition_replica_mixing.csv`
- `reports/m15_qmod8_transition_replica_comparison.csv`
- `reports/m15_qmod8_transition_replica_summary.csv`

## Matriz replicada

Filas: `q_i mod 8`. Columnas: `q_{i+1} mod 8`.

| desde \ hacia | 1 | 3 | 5 | 7 |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 0.250005999914 | 0.249999600006 | 0.249986800190 | 0.250007599891 |
| 3 | 0.250027999910 | 0.250032799895 | 0.249996000013 | 0.249943200182 |
| 5 | 0.249996799980 | 0.249998399990 | 0.250001600010 | 0.250003200020 |
| 7 | 0.250000000000 | 0.249998399980 | 0.249993599918 | 0.250008000102 |

Conteos por fila:

| `q_i mod 8` | conteo |
| ---: | ---: |
| 1 | 625009 |
| 3 | 625002 |
| 5 | 624996 |
| 7 | 624992 |

## Mezcla

| pasos | max TV contra uniforme |
| ---: | ---: |
| 1 | 0.000060799805 |
| 2 | 0.000015002180 |
| 3 | 0.000015000447 |
| 4 | 0.000015000447 |

Distribucion estacionaria estimada:

| `q mod 8` | estacionaria | diff vs uniforme |
| ---: | ---: | ---: |
| 1 | 0.250007700219 | +0.000007700219 |
| 3 | 0.250007300228 | +0.000007300228 |
| 5 | 0.249994499954 | -0.000005500046 |
| 7 | 0.249990499599 | -0.000009500401 |

## Comparacion contra CodexHijo1

CodexHijo1 reporto:

```text
max TV contra uniforme en 1 paso = 0.000060799805
max TV contra uniforme en 3 pasos = 0.000015000447
```

Esta replica obtiene:

```text
max TV contra uniforme en 1 paso = 0.000060799805
max TV contra uniforme en 3 pasos = 0.000015000447
```

Diferencias contra CodexHijo1:

```text
max diferencia de conteos = 0
max diferencia de probabilidad de celda = 0.000000000000
diff TV paso 1 = 0.000000000000
diff TV paso 3 = 0.000000000000
```

## Veredicto

```text
replica exacta
```

La matriz queda casi uniforme fila por fila y la distancia total variation
contra uniforme baja a escala `1.5e-5` en 2-3 pasos. Esto replica la compuerta
de CodexHijo1: `q mod 8` predice `next_tail` localmente, pero no conserva
memoria marginal apreciable como estado entre bloques consecutivos.

## Recomendacion al orquestador

Recomiendo cerrar o enfriar M15 en la forma marginal:

```text
q mod 8 como memoria suficiente para supervivencia orbital
```

Si M15 sigue vivo, deberia ser con otra formulacion preregistrada, no como
holdout inmediato de esta variable marginal.

## Que no deberiamos concluir

- No concluir una prueba ni una negacion global de Collatz.
- No concluir que `q mod 8` no predice `next_tail`; si lo predice localmente.
- No concluir que todo modulo superior o toda variable orbital carece de memoria.
- No concluir nada sobre el holdout fresco `15000001..25000000`; no se miro.
