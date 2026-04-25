# Investigacion sobre Collatz - Decimotercera Ola: prueba de destruccion M14

Fecha de cierre de esta ola: 2026-04-25 10:57:05 -03:00
Estado: decimotercera ola cerrada
Resumen asociado: [ResumenInvestigacionSobreCollatzDecimoterceraOla.md](ResumenInvestigacionSobreCollatzDecimoterceraOla.md)
Conclusion dinamica vigente: [Conlusion.md](Conlusion.md)
Ola anterior: [Duodecima](InvestigacionSobreCollatzDuodecimaOla.md)
Reporte tecnico: [reports/m14_residual_robustness.md](reports/m14_residual_robustness.md)

## 1. Preguntas antes de investigar

```text
1. Estoy en algo virgen?
Respuesta: no. Estamos en terreno conocido de modelos probabilisticos, stopping times, bloques Mersenne y seleccion por supervivencia.

2. Alguien ya busco esto?
Respuesta: si a nivel amplio. La celda `prev_exit_v2 = 5` + interior era una pista propia del repo, pero post-hoc.

3. Que parte exacta podria ser nueva?
Respuesta: solo si el residuo sobrevivia correccion por multiples comparaciones y holdout independiente.

4. Puedo descubrir algo con esto?
Respuesta: si: confirmar una dependencia fina o descartarla limpiamente.

5. Que tan lejos estoy de algo relevante?
Respuesta: lejos de una prueba. Cerca de mejorar el metodo de investigacion.

6. Que haria que sigamos?
Respuesta: supervivencia en bootstrap/permutacion, Bonferroni estricto y holdout.

7. Que haria que abandonemos?
Respuesta: desaparicion en holdout o p ajustado por encima del umbral.
```

## 2. Objetivo

Claude marco un riesgo metodologico fuerte:

```text
El residuo `prev_exit_v2 = 5` + interior fue encontrado despues de muchas comparaciones.
```

El objetivo de esta ola fue intentar destruir la senal antes de formalizarla.

## 3. Metodo

Se agrego:

```text
experiments/test_m14_residual_robustness.py
```

El script mide:

- diferencia real-modelo en la celda candidata;
- p crudo por aproximacion normal;
- Bonferroni sobre tests M13;
- Bonferroni conservador agregando tests exploratorios del Codex hijo;
- permutation test por cadenas con eventos objetivo;
- bootstrap por cadenas;
- holdout independiente `5000001 <= n <= 10000000`;
- chequeo algebraico local por clases modulo potencias de 2.

## 4. Resultado en rango original

| Medida | Valor |
| --- | ---: |
| Real | `1551 / 3426 = 0.45271454` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff | `0.04657317` |
| p crudo | `0.0000939371` |
| Bonferroni M13 | `0.01390268` |
| Bonferroni conservador | `0.06519232` |
| permutation p | `0.00009999` |
| bootstrap CI95 | `[0.02364649, 0.06933110]` |

La senal se sostiene en el rango original bajo bootstrap/permutacion, pero no pasa el umbral estricto `p ajustado < 0.01`.

## 5. Resultado en holdout

| Medida | Valor |
| --- | ---: |
| Rango | `5000001 <= n <= 10000000` |
| Real | `1380 / 3321 = 0.41553749` |
| Modelo | `1402 / 3452 = 0.40614137` |
| Diff | `0.00939612` |
| p crudo | `0.43201832` |
| permutation p | `0.42505749` |
| bootstrap CI95 | `[-0.01423070, 0.03272495]` |

El holdout independiente no confirma la diferencia.

## 6. Chequeo algebraico

La congruencia local:

```text
prev_exit_v2 = 5 <=> 3^s q = 33 mod 64
```

produce:

```text
P(next_tail = 1 | prev_exit_v2 = 5, local) = 0.5
```

No hay una ley local simple que prediga el residuo observado en la muestra exploratoria.

## 7. Preguntas despues de investigar

```text
1. La respuesta sobre originalidad cambio?
Respuesta: si, a la baja. La pista no se sostiene como hallazgo robusto.

2. La probabilidad de relevancia subio, bajo o quedo igual?
Respuesta: bajo. La senal no sobrevive el holdout.

3. Se encontro una senal robusta o solo seleccion?
Respuesta: la senal original queda como exploratoria no confirmada.

4. Que aprendimos que no sabiamos antes?
Respuesta: el repo necesita separar siempre descubrimiento y confirmacion; Claude aporto una correccion metodologica importante.

5. Conviene seguir, escalar, formalizar o abandonar?
Respuesta: abandonar `prev_exit_v2 = 5` + interior como pista principal.

6. Cual es la siguiente pregunta minima?
Respuesta: que nuevas busquedas pueden hacerse con train/holdout desde el inicio, o que lemma local puede formularse sin depender de barrido post-hoc.
```

## 8. Veredicto

M14 queda cerrado como descarte limpio.

La rama del Codex hijo:

```text
codex-hijo/m14-residuos
```

queda preservada como exploracion, pero no se integra como conclusion.

La forma correcta de avanzar no es insistir en `q_current mod 4`, sino adoptar busquedas pre-registradas con holdout.
