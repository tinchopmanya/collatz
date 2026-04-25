# Resultados M15 Algebra - next_tail por clases modulares

Fecha: 2026-04-25
Rama: `codex-hijo/m15-algebra`

## Comandos usados

```powershell
git status --short --branch
git switch main
git pull
git switch -c codex-hijo/m15-algebra
python -m py_compile experiments\analyze_m15_algebra.py
python experiments\analyze_m15_algebra.py --min-k 2 --max-k 6 --max-next-tail 10 --out-dir reports
```

No se corrio holdout, no se uso el rango `15M..25M`, y no se hizo barrido estadistico sobre enteros grandes. El calculo enumera clases residuales finitas y usa levantamiento 2-adico uniforme para los bits no fijados.

## Salidas

- `reports/m15_algebra_next_tail_by_mod.csv`
- `reports/m15_algebra_summary.csv`

## Formulacion algebraica usada

Para `n = 2^s q - 1`, con `q` impar:

```text
y = 3^s q
exit_v2 = v2(y - 1)
next_odd = (y - 1) / 2^exit_v2
next_tail = v2(next_odd + 1)
```

Fijados `s` y `q mod 2^K`, se calcula `y mod 2^K`.

- Si `y = 1 mod 2^K`, entonces `exit_v2 >= K` y los bits restantes dejan `next_tail` geometrico.
- Si `y != 1 mod 2^K`, entonces `exit_v2 < K` queda determinado.
- Despues de dividir por `2^exit_v2`, si `next_odd + 1` ya queda decidido modulo los bits conocidos, `next_tail` es deterministico.
- Si no queda decidido, queda una cola geometrica desplazada desde el primer bit no conocido.

Para `q mod 2^K`, se promedia sobre `s` con `P(s) = 2^-s`. Como `3^s mod 2^K` es periodico, la suma infinita se reduce a una suma finita por clases de `s`.

## Resumen teorico

| Predictor | K | Modulo | Clases que difieren | Max abs diff | Residuo | next_tail |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| `q mod 2^K` | 2 | 4 | 0 / 2 | 0.000000000000 | 1 | 1 |
| `q mod 2^K` | 3 | 8 | 4 / 4 | 0.333333333333 | 1 | 1 |
| `q mod 2^K` | 4 | 16 | 8 / 8 | 0.433333333333 | 5 | 1 |
| `q mod 2^K` | 5 | 32 | 16 / 16 | 0.518627450980 | 15 | 2 |
| `q mod 2^K` | 6 | 64 | 32 / 32 | 0.518627450980 | 15 | 2 |
| `n mod 2^K` | 2 | 4 | 0 / 2 | 0.000000000000 | 1 | 1 |
| `n mod 2^K` | 3 | 8 | 0 / 4 | 0.000000000000 | 1 | 1 |
| `n mod 2^K` | 4 | 16 | 2 / 8 | 0.500000000000 | 1 | 1 |
| `n mod 2^K` | 5 | 32 | 8 / 16 | 0.750000000000 | 25 | 2 |
| `n mod 2^K` | 6 | 64 | 22 / 32 | 0.875000000000 | 9 | 3 |

## Clases bajas mas claras para `q mod 8`

La primera desviacion aparece ya en `q mod 8`.

| `q mod 8` | P(next_tail=1) | Geometrica | Diff |
| ---: | ---: | ---: | ---: |
| 1 | 5/6 = 0.833333333333 | 1/2 | +0.333333333333 |
| 3 | 2/3 = 0.666666666667 | 1/2 | +0.166666666667 |
| 5 | 1/6 = 0.166666666667 | 1/2 | -0.333333333333 |
| 7 | 1/3 = 0.333333333333 | 1/2 | -0.166666666667 |

Esto no es un hallazgo empirico; es una consecuencia directa del mapa modular.

## Respuestas pedidas

1. La distribucion `P(next_tail | clase modular)` no coincide siempre con la geometrica. Para `q mod 4` si coincide; para `q mod 8` ya difiere en todas las clases. Para `n mod 2^K`, la desviacion aparece desde `n mod 16`.

2. Si hay clases con desviacion teorica clara. La mas simple es `q mod 8`: residuos `1,3` elevan `P(next_tail=1)` y residuos `5,7` la bajan. En modulos mayores hay refinamientos, pero no hace falta subir de `2^3` para ver el efecto.

3. La desviacion aparece en modulo bajo. Para `q`, aparece en `2^3`; para `n`, aparece en `2^4`. En `2^5` y `2^6` el efecto se refina y puede ser mas extremo, pero eso tambien aumenta clases y riesgo de sobreajuste experimental.

4. Si vale la pena correr train/holdout: si, pero solo para una H1 pre-registrada minima y no para buscar clases. La algebra ya dice que `q mod 8` predice `next_tail` bajo levantamiento 2-adico uniforme. El experimento train/holdout deberia preguntar si esta prediccion sigue siendo util en la poblacion condicionada que interese, por ejemplo `interior_block`, y si mejora al modelo geometrico independiente.

5. Hipotesis pre-registrada recomendada para H1:

```text
H1: En bloques interiores, la distribucion de next_tail depende de q_current mod 8 en la direccion predicha algebraicamente:
q = 1,3 mod 8 tienen P(next_tail=1) mayor que 1/2;
q = 5,7 mod 8 tienen P(next_tail=1) menor que 1/2.
```

Test recomendado: un solo chi-cuadrado de homogeneidad/independencia para `q_current mod 8` contra una respuesta truncada de `next_tail` (`1`, `2`, `3`, `4+`), con direccion secundaria pre-registrada para `P(next_tail=1)`.

## Recomendacion

```text
H1 merece experimento train/holdout, pero solo con q_current mod 8 como hipotesis minima.
```

No recomendaria gastar tests en `q mod 16`, `q mod 32` o `n mod 64` todavia. La algebra ya muestra el efecto en `q mod 8`; subir el modulo antes del holdout seria volver a una busqueda de celdas.

## Que descartar

- Descartar `q mod 4`: algebraicamente coincide con geometrica.
- Descartar una busqueda exploratoria por todos los residuos hasta `2^6`: seria redundante y aumenta multiplicidad.
- Descartar `prev_exit_v2 = 5` como foco de H1: no es necesario para explicar la dependencia modular baja.
- No interpretar esto como prueba de Collatz ni como senal global de supervivencia. Es una dependencia local modular exacta bajo una medida teorica.
