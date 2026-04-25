# Resultados M15 - transicion `q mod 8`

Fecha: 2026-04-25
Rama: `codex-hijo/m15-qmod8-transition`

## Comando reproducible

```powershell
python experiments\analyze_m15_qmod8_transition.py --limit 5000000 --out-dir reports --prefix m15_qmod8_transition
```

Tambien se ejecuto:

```powershell
python -m py_compile experiments\analyze_m15_qmod8_transition.py
python experiments\analyze_m15_qmod8_transition.py --limit 10001 --out-dir reports --prefix m15_qmod8_transition_smoke
```

Los CSV de humo se borraron.

## Definicion usada

Use la convencion existente del proyecto:

```text
s_i = v2(n_i + 1)
q_i = (n_i + 1) / 2^s_i = AlternatingBlock.odd_factor
exit_v2_i = v2(3^s_i q_i - 1)
n_{i+1} = (3^s_i q_i - 1) / 2^exit_v2_i = AlternatingBlock.next_odd
q_{i+1} = (n_{i+1} + 1) / 2^v2(n_{i+1} + 1)
```

Poblacion exploratoria:

```text
impares 3 <= n <= 5000000
una transicion odd-to-odd por impar inicial
```

No es holdout y no mide supervivencia.

## Archivos

- `experiments/analyze_m15_qmod8_transition.py`
- `reports/m15_qmod8_transition_matrix.csv`
- `reports/m15_qmod8_transition_stationary.csv`
- `reports/m15_qmod8_transition_mixing.csv`
- `reports/m15_qmod8_transition_summary.csv`

## Matriz de transicion

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

La matriz es, a escala visible, uniforme fila por fila.

## Estacionaria y mezcla

Distribucion estacionaria estimada:

| `q mod 8` | estacionaria | diff vs uniforme |
| ---: | ---: | ---: |
| 1 | 0.250007700219 | +0.000007700219 |
| 3 | 0.250007300228 | +0.000007300228 |
| 5 | 0.249994499954 | -0.000005500046 |
| 7 | 0.249990499599 | -0.000009500401 |

Medida de mezcla usada: distancia total variation maxima de las filas contra uniforme.

| pasos | max TV contra uniforme |
| ---: | ---: |
| 1 | 0.000060799805 |
| 2 | 0.000015002180 |
| 3 | 0.000015000447 |
| 4 | 0.000015000447 |

No calcule autovalores; use esta medida simple de mezcla. A los 2-3 pasos todas las filas son indistinguibles entre si en esta escala; el resto es el pequeno desbalance estacionario producido por bordes finitos del rango.

## Parte algebraica

No incluyo una demostracion exacta nueva. La evidencia empirica es compatible con la heuristica 2-adica esperada: aunque `q mod 8` predice `next_tail` localmente, el siguiente `q mod 8` queda remezclado casi uniformemente por los bits no fijados de `q`, `tail` y `exit_v2`.

Lectura prudente:

```text
q mod 8 tiene informacion local sobre next_tail, pero no muestra memoria marginal apreciable como estado entre bloques consecutivos.
```

## Recomendacion

Recomiendo enfriar M15 antes de gastar holdout fresco en esta H1 modular, al menos en la forma:

```text
q mod 8 como estado de memoria para supervivencia orbital
```

La razon es operacional: la matriz `q_{i+1} mod 8 | q_i mod 8` mezcla practicamente a uniforme en un paso. Si el estado modular se reinicia asi de rapido, la ventaja local para predecir `next_tail` no parece tener memoria suficiente para propagarse a cadenas completas.

## Que no deberiamos concluir

- No concluir una prueba ni un resultado global sobre Collatz.
- No concluir que todo modulo superior carece de memoria; no se abrio `q mod 16`.
- No concluir nada sobre holdout `15000001..25000000`; no se miro.
- No concluir que `q mod 8` no predice `next_tail`; si lo predice, pero eso ya era algebra local conocida.
- No concluir que no existe ningun efecto de supervivencia; solo que esta H1 marginal de memoria `q mod 8` parece demasiado fria para justificar el siguiente gasto computacional sin reformulacion.
