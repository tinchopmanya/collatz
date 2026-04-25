# Prueba de robustez M14: residuo `prev_exit_v2 = 5` + interior

Fecha: 2026-04-25
Script: [experiments/test_m14_residual_robustness.py](../experiments/test_m14_residual_robustness.py)

## Preguntas antes de iterar

```text
1. Estoy en algo virgen?
Respuesta: no. Estamos en modelos probabilisticos, stopping times, bloques Mersenne y condicionamiento por supervivencia, todos cercanos a literatura existente.

2. Alguien ya busco esto?
Respuesta: si a nivel amplio. Lo que era propio del repo era la celda post-hoc `prev_exit_v2 = 5` + interior.

3. Que parte exacta podria ser nueva?
Respuesta: si la diferencia real-modelo en esa celda sobreviviera correccion por multiples comparaciones y holdout, podria ser una dependencia fina.

4. Puedo descubrir algo con esto?
Respuesta: si, pero lo mas probable era descubrir si la senal era robusta o si debia descartarse.

5. Que evidencia haria que sigamos?
Respuesta: p ajustado fuerte, bootstrap/permutacion robustos y supervivencia en rango independiente.

6. Que evidencia haria que abandonemos?
Respuesta: falla bajo Bonferroni estricto o desaparicion en holdout independiente.
```

## Comandos

Rango exploratorio original:

```powershell
python experiments\test_m14_residual_robustness.py --limit 5000000 --max-blocks 256 --permutations 10000 --seed 20260425 --extra-tests 546 --out-dir reports --prefix m14_residual_robustness
```

Holdout independiente:

```powershell
python experiments\test_m14_residual_robustness.py --start 5000001 --limit 10000000 --max-blocks 256 --permutations 10000 --seed 20260425 --extra-tests 546 --out-dir reports --prefix m14_residual_robustness_holdout_5000001_10000000
```

## Salidas

- [m14_residual_robustness_summary.csv](m14_residual_robustness_summary.csv)
- [m14_residual_robustness_test_counts.csv](m14_residual_robustness_test_counts.csv)
- [m14_residual_robustness_permutation.csv](m14_residual_robustness_permutation.csv)
- [m14_residual_robustness_algebra.csv](m14_residual_robustness_algebra.csv)
- [m14_residual_robustness_holdout_5000001_10000000_summary.csv](m14_residual_robustness_holdout_5000001_10000000_summary.csv)
- [m14_residual_robustness_holdout_5000001_10000000_permutation.csv](m14_residual_robustness_holdout_5000001_10000000_permutation.csv)
- [m14_residual_robustness_holdout_5000001_10000000_algebra.csv](m14_residual_robustness_holdout_5000001_10000000_algebra.csv)

## Resultado en el rango original

| Medida | Valor |
| --- | ---: |
| Rango real | `3 <= n <= 5000000`, impares |
| Real | `1551 / 3426 = 0.45271454` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff real-modelo | `0.04657317` |
| p crudo dos colas | `0.0000939371` |
| tests M13 | `148` |
| tests conservadores M13 + Codex hijo | `694` |
| Bonferroni solo M13 | `0.01390268` |
| Bonferroni conservador | `0.06519232` |
| permutation p por cadena | `0.00009999` |
| bootstrap CI95 por cadena | `[0.02364649, 0.06933110]` |

Lectura:

- La senal original es real en el primer rango.
- Sobrevive bootstrap y permutacion por cadena.
- Pero no pasa el umbral estricto `p ajustado < 0.01` bajo Bonferroni, ni siquiera contando solo M13.
- Contando tambien la descomposicion exploratoria del Codex hijo, queda claramente por encima del umbral.

## Resultado en holdout independiente

| Medida | Valor |
| --- | ---: |
| Rango real | `5000001 <= n <= 10000000`, impares |
| Real | `1380 / 3321 = 0.41553749` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff real-modelo | `0.00939612` |
| p crudo dos colas | `0.43201832` |
| Bonferroni M13 | `1.0` |
| Bonferroni conservador | `1.0` |
| permutation p por cadena | `0.42505749` |
| bootstrap CI95 por cadena | `[-0.01423070, 0.03272495]` |

Lectura:

```text
El efecto real-modelo no se reproduce en holdout independiente.
```

Este es el resultado decisivo de la ola.

## Chequeo algebraico local

Para `prev_exit_v2 = 5`:

```text
3^s q = 33 mod 64
```

La enumeracion modular local da:

```text
P(next_tail = 1 | prev_exit_v2 = 5, sin supervivencia) = 0.5
```

Esto coincide con las olas previas: la congruencia local sola no produce el residuo. La senal dependia del condicionamiento orbital, no de una ley local estatica.

## Preguntas despues de iterar

```text
1. La originalidad cambio?
Respuesta: bajo. El candidato M14 no se sostiene como residuo real-modelo robusto.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: bajo. El holdout independiente destruye la lectura fuerte.

3. Se encontro senal robusta, ruido o descarte?
Respuesta: descarte para la afirmacion real-modelo original. La asociacion interna real puede existir, pero el modelo ya captura gran parte.

4. Que aprendimos?
Respuesta: una senal que parecia fuerte en el primer rango puede desaparecer en holdout. Claude tenia razon en exigir confirmacion.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: abandonar `prev_exit_v2 = 5` + interior como pista principal. No mergear la rama exploratoria del Codex hijo como conclusion.

6. Cual es la siguiente pregunta minima?
Respuesta: disenar nuevas busquedas con separacion train/holdout desde el inicio, o volver a una pregunta algebraica local mas formal.
```

## Veredicto

M14 queda cerrado como descarte limpio:

```text
El residuo `prev_exit_v2 = 5` + `interior_block` no sobrevive una prueba confirmatoria independiente.
```

La rama `codex-hijo/m14-residuos` se conserva como exploracion util, pero no debe integrarse a `main` como hallazgo.

## Mensaje operativo

La decision correcta no es forzar la pista. La decision correcta es subir el estandar:

```text
Desde ahora, toda senal encontrada exploratoriamente debe tener holdout o test pre-registrado antes de convertirse en milestone fuerte.
```
