# Resultados M14 - descomposicion inicial del residuo

Fecha: 2026-04-25
Rama: `codex-hijo/m14-residuos`

## Comandos usados

```powershell
python -m py_compile experiments\analyze_m14_residue.py
python experiments\analyze_m14_residue.py --limit 10000 --max-blocks 64 --seed 20260425 --out-dir reports --prefix m14_residue_smoke
python experiments\analyze_m14_residue.py --limit 5000000 --max-blocks 256 --seed 20260425 --mod-ks 2,3,4,5,6,7,8 --out-dir reports --prefix m14_residue
```

Los CSV de humo se borraron. La corrida final genero:

- `reports/m14_residue_summary.csv`
- `reports/m14_residue_by_depth.csv`
- `reports/m14_residue_by_margin.csv`
- `reports/m14_residue_by_prev_tail.csv`
- `reports/m14_residue_by_q_mod.csv`
- `reports/m14_residue_by_current_mod.csv`

## Nota metodologica

Filtro usado:

```text
prev_exit_v2 = 5
current_position = interior_block
comparar current tail = 1 como next_tail = 1 respecto del bloque previo
```

El total reproduce la fila vigente:

| real count | model count | real P(next_tail=1) | model P(next_tail=1) | diff | IC95 |
| ---: | ---: | ---: | ---: | ---: | --- |
| 3426 | 3452 | 0.45271454 | 0.40614137 | 0.04657317 | [0.02320157, 0.06994477] |

Para el modelo, `tail` y `exit_v2` se generan igual que en M13. Como ese modelo no tiene un impar real, los residuos de `q` son sinteticos: `q` impar uniforme modulo `2^max_k`, independiente de `tail/exit_v2`, y `current_mod` se calcula como `2^tail q - 1`. Por eso los cortes modulares son una comparacion contra un nulo modular, no una orbita modelada modulo potencias de 2.

## Cinco buckets mas desviados

Ranking por `abs(tail_one_success_share_diff)` con al menos 50 muestras reales y modeladas. Los cortes `q_mod_2^2`, `q_mod_2^3`, etc. son anidados; no deben leerse como cinco pruebas independientes.

| Particion | Bucket | Real/Modelo | P real | P modelo | Diff | IC95 | Aporte al exceso |
| --- | ---: | ---: | ---: | ---: | ---: | --- | ---: |
| `q mod 4` | 1 | 1985 / 1743 | 0.58287154 | 0.40504877 | 0.17782277 | [0.14617359, 0.20947195] | 0.1331924977 |
| `q mod 4` | 3 | 1441 / 1709 | 0.27342124 | 0.40725571 | -0.13383447 | [-0.16657969, -0.10108925] | -0.0866193291 |
| `q mod 8` | 3 | 587 / 875 | 0.20442930 | 0.41257143 | -0.20814213 | [-0.25427692, -0.16200733] | -0.0695507871 |
| `q mod 8` | 1 | 981 / 859 | 0.57594292 | 0.39348079 | 0.18246212 | [0.13747638, 0.22744787] | 0.0670011006 |
| `q mod 8` | 5 | 1004 / 884 | 0.58964143 | 0.41628959 | 0.17335184 | [0.12883443, 0.21786926] | 0.0661913971 |

## Lectura conservadora

La senal no parece venir de profundidad sola. El maximo aporte por profundidad es `0.010203312` y varios intervalos cruzan cero; hay ruido de cola en profundidades altas.

El margen logaritmico muestra una tendencia compatible con mezcla de supervivencia, pero no concentra el residuo: `margin_2_4` aporta `0.0135134907` y `margin_4_plus` `0.0117809485`, con muestras menores.

`prev_tail` explica parte de la mezcla: `prev_tail_01` aporta `0.033405679` y `prev_tail_02` aporta `0.0271551675`. Aun asi, el corte mas limpio es modular.

El hallazgo fuerte es `q_current mod 4`. En esta subpoblacion, `q_current = 1 mod 4` tiene mucho mas `next_tail = 1` que el modelo, mientras `q_current = 3 mod 4` tiene mucho menos. Al refinar a modulo 8/16 la estructura se reparte, pero no aparece una clase fina unica que absorba todo el efecto.

`current_mod` no debe venderse como causa: para impares, `current_mod mod 4 = 1` equivale a `tail = 1`, asi que ese corte solo reexpresa el evento que estamos midiendo.

## Veredicto operativo

La evidencia favorece una causa modular gruesa o una mezcla condicionada por una variable modular gruesa, no una concentracion por profundidad ni por margen puro. La formulacion mas prudente es:

```text
Dentro de prev_exit_v2 = 5 + interior_block, el exceso de next_tail = 1 se separa fuertemente por q_current mod 4.
```

Esto no prueba nada global sobre Collatz y no alcanza como lemma. Si es real, el siguiente paso debe explicar por que el condicionamiento de supervivencia despues de `prev_exit_v2 = 5` selecciona distinto los dos valores de `q_current mod 4`.

## Experimento recomendado despues

Hacer un corte cruzado pequeno:

```text
(q_current mod 4) x (prev_tail) x (margin bucket)
```

con los mismos campos de comparacion. El objetivo no seria sumar mas buckets, sino decidir si `prev_tail` y margen desaparecen al fijar `q_current mod 4`, o si el efecto modular es una etiqueta de otra mezcla.

Tambien conviene derivar la congruencia exacta desde el bloque previo:

```text
prev n = 2^s q - 1
prev_exit_v2 = 5
current = (3^s q - 1) / 32
q_current = (current + 1) / 2^tail_current
```

y ver que condicion impone sobre `q_current mod 4`.

## Que descartaria por ahora

- Profundidad como explicacion unica.
- Margen logaritmico como explicacion unica.
- `current_mod` como causa independiente, porque es tautologico respecto de `tail`.
- Perseguir residuos modulo `2^8` antes de validar la particion gruesa `q_current mod 4`.
- Cualquier lectura de esto como prueba o como novedad matematica fuerte.
