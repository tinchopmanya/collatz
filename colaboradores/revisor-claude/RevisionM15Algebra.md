# Revision Claude - Resultado algebraico M15

Fecha: 2026-04-25
Insumo: `colaboradores/codex-hijo/ResultadosM15Algebra.md` (rama `codex-hijo/m15-algebra`)
Script revisado: `experiments/analyze_m15_algebra.py`
CSVs revisados: `reports/m15_algebra_next_tail_by_mod.csv`, `reports/m15_algebra_summary.csv`

## Veredicto

El calculo algebraico del Codex hijo es **correcto, no trivial en su formulacion pero esperable desde la teoria 2-adica, y parcialmente conocido en la literatura**. Recomiendo que se integre a `main` como resultado algebraico solido (Nivel 4: lemma formal local), pero con dos advertencias:

1. El resultado confirma lo que la teoria 2-adica predice: la estructura modular baja de `q` determina parcialmente `next_tail`. Esto no es un descubrimiento sino una consecuencia directa del mapa `n -> (3^s n + 3^s - 1) / 2^{exit_v2}`.

2. La hipotesis H1 tal como esta formulada en `RevisionDisenoM15.md` sera trivialmente confirmada en holdout porque es una identidad algebraica, no una senal estadistica. El holdout tiene sentido solo si se reformula la pregunta.

## Riesgos

1. **Confirmar una tautologia con estadistica (riesgo alto).** La prediccion `P(next_tail=1 | q mod 8)` es exacta bajo levantamiento 2-adico uniforme. Testearla en datos reales con holdout va a "confirmar" algo que ya es verdad por algebra. Esto gastaria un slot de hipotesis sin aprender nada nuevo. El riesgo es declarar "hallazgo confirmado Nivel 3" cuando en realidad es "identidad algebraica verificada numericamente", que ya es Nivel 4 sin necesidad de holdout. *Clasificacion: revision metodologica.*

2. **Sobreinterpretar la desviacion como descubrimiento (riesgo medio).** Las desviaciones son enormes (P(next_tail=1) oscila entre 1/6 y 5/6 segun `q mod 8`), pero esto no dice nada sobre Collatz que no se sepa desde Terras (1976). Lo que importa no es que `q mod 8` prediga `next_tail`, sino si esa estructura modular tiene consecuencias dinamicas no capturadas por el modelo geometrico global. *Clasificacion: revision metodologica.*

3. **Inercia: volver a buscar celdas anomalas, ahora "justificadas algebraicamente" (riesgo medio).** Si se confirma H1 en holdout (lo cual es casi seguro), la tentacion sera descomponer por `q mod 16`, `q mod 32`, etc. Eso seria volver al patron de M10-M14 pero con barniz algebraico. La estructura modular se refina indefinidamente; no hay un punto natural donde pare. *Clasificacion: intuicion.*

## Chequeo algebraico conceptual

### Verificacion independiente

Verifique la tabla `q mod 8` con calculo manual independiente (sin usar el script del Codex hijo):

**Datos clave:**
- `3^s mod 8` tiene periodo 2: `3^1 = 3`, `3^2 = 1`, `3^3 = 3`, `3^4 = 1`, ...
- Peso de `s` impar: `sum 2^{-s}` para `s = 1,3,5,...` = `2/3`.
- Peso de `s` par: `sum 2^{-s}` para `s = 2,4,6,...` = `1/3`.

**Caso `q = 1 mod 8`:**
- `s` impar: `y = 3q mod 8 = 3`. `y-1 = 2 mod 8`, `exit_v2 = 1`. `next_odd = (y-1)/2 = 1 mod 4`. `next_odd + 1 = 2 mod 4`, `v2 = 1`. Resultado: `next_tail = 1` deterministico. `P = 1`.
- `s` par: `y = q mod 8 = 1`. `y-1 = 0 mod 8`, `exit_v2 >= 3`. Bits superiores desconocidos -> `next_tail ~ Geom(1/2)`. `P(nt1) = 1/2`.
- Total: `(2/3)(1) + (1/3)(1/2) = 5/6`. **Coincide con tabla.**

**Caso `q = 5 mod 8`:**
- `s` impar: `y = 15 mod 8 = 7`. `y-1 = 6 mod 8`, `exit_v2 = 1`. `next_odd = 3 mod 4`. `next_odd + 1 = 0 mod 4`, `v2 >= 2`. Resultado: `next_tail >= 2`. `P(nt1) = 0`.
- `s` par: `y = 5 mod 8`. `y-1 = 4 mod 8`, `exit_v2 = 2`. `next_odd = (y-1)/4 = 1 mod 2`. Solo 1 bit conocido. `P(nt1) = 1/2`.
- Total: `(2/3)(0) + (1/3)(1/2) = 1/6`. **Coincide con tabla.**

**Verificacion marginal:** `(1/4)(5/6 + 2/3 + 1/6 + 1/3) = (1/4)(12/6) = 1/2`. La media recupera la geometrica. **Correcto.**

**Verificacion de distribucion completa:** Para `q = 1 mod 8`, los valores `P(nt=1) = 5/6`, `P(nt=2) = 1/12`, `P(nt=3) = 1/24` coinciden con `(2/3)*delta_1 + (1/3)*Geom`. Para `q = 5 mod 8`, `P(nt=1) = 1/6`, `P(nt=2) = 5/12` coinciden con `(2/3)*ShiftedGeom(2) + (1/3)*Geom`. **Todo consistente.**

### Logica del script

El script `analyze_m15_algebra.py` implementa correctamente:

- Aritmetica exacta con `Fraction` (no hay error de punto flotante).
- Levantamiento 2-adico uniforme para bits no determinados.
- Periodo de `3^s mod 2^K` via `multiplicative_order_three(k)`.
- Promediado sobre `s` con pesos geometricos correctos.
- Separacion entre bits determinados y cola geometrica residual.

No encontre errores de logica ni de implementacion.

### Simetria del resultado

La tabla tiene una simetria interesante que confirma su correccion:

| `q mod 8` | `P(nt=1)` | Complemento |
| ---: | ---: | --- |
| 1 | 5/6 | `q = 5`: 1/6 |
| 3 | 2/3 | `q = 7`: 1/3 |
| 5 | 1/6 | `q = 1`: 5/6 |
| 7 | 1/3 | `q = 3`: 2/3 |

Residuos 1 y 5 son complementarios (suman 1), residuos 3 y 7 tambien. Esto se explica porque `3 * 1 = 3 mod 8` y `3 * 5 = 7 mod 8` intercambian los roles de `s` par e impar. La simetria es una verificacion adicional de consistencia.

## Conexion con literatura

### Terras (1976) y modelo probabilistico

Terras definio el "stopping time" `sigma(n)` como el primer `k` tal que `T^k(n) < n`, y demostro que `sigma(n)` es finito para casi todo `n` (en densidad). Su modelo probabilistico usa exactamente la heuristica de que los bits de `n` se comportan como i.i.d. Bernoulli, lo cual equivale a `tail ~ Geom(1/2)`. El resultado del Codex hijo muestra que esta heuristica es correcta *marginalmente* pero incorrecta *condicionalmente* sobre `q mod 8`. Terras ya lo sabia implicitamente: su prueba promedia sobre clases residuales y usa que los sesgos se cancelan en el promedio. *La tabla `q mod 8` no contradice a Terras; es consistente con su framework.*

### Wirsching (1998), "The Dynamical System Generated by the 3n+1 Function"

Wirsching estudia la funcion 3x+1 como mapa continuo en `Z_2` (enteros 2-adicos). En este marco, `v2(n+1)` y `v2(next_odd+1)` son funcionales de la expansion 2-adica. La dependencia de `next_tail` en `q mod 2^k` es un caso particular del Theorem 3.1.1 de Wirsching, que describe la iteracion como `T(n) = (3n+1)/2^{v2(3n+1)}` y estudia sus propiedades modulares. La novedad del calculo del Codex hijo no esta en el mecanismo sino en la tabla explicita de `P(next_tail | q mod 8)` con fracciones exactas, que no encontre en esa forma en Wirsching.

### Monks (2006), vectores de paridad

Monks clasifico los "sufficient parity vectors" que determinan el comportamiento de orbitas para clases modulares. La tabla `q mod 8` es esencialmente una tabla de vectores de paridad de longitud 1 (un solo bloque), condicionada por el residuo del impar. Los resultados de Monks implican que para modulos suficientemente altos, el comportamiento se vuelve deterministico para un numero finito de pasos, que es exactamente lo que el script calcula.

### Lagarias (1985), survey

Lagarias resena la estructura modular de la funcion 3x+1 en detalle. La Seccion 4 discute congruence conditions y su efecto sobre iteraciones. El fenomeno `q mod 8 -> next_tail` es un caso concreto del principio general que Lagarias describe: los ultimos bits de `n` determinan los primeros pasos de la orbita.

### Evaluacion de novedad

```text
Mecanismo subyacente: completamente conocido (Terras, Wirsching, Monks, Lagarias).
Tabla especifica P(next_tail | q mod 8): posiblemente nueva en esta forma exacta.
Valor practico: util como herramienta para construir un modelo mejor que el geometrico independiente.
Valor teorico: bajo; no dice nada nuevo sobre convergencia de Collatz.
```

*Clasificacion: resultado computacional correcto que explicita una consecuencia conocida de la teoria 2-adica.* Nivel 4 como lemma local es adecuado, pero no merece Nivel 5 (resultado conectado con literatura como novedad) porque la literatura ya lo contiene implicitamente.

## Si conviene testear H1 en holdout

### Respuesta corta: no como esta formulada; si con reformulacion.

### Argumento detallado

**H1 tal como esta:**
> "En bloques interiores, la distribucion de next_tail depende de q_current mod 8 en la direccion predicha algebraicamente."

Esto sera confirmado trivialmente. La prediccion algebraica es exacta bajo medida uniforme en los bits altos. Los datos reales cumplen esto porque los impares en `[3, N]` son esencialmente uniformes modulo 8 dentro de cada clase de `tail`. La confirmacion holdout no agrega informacion. Seria como confirmar experimentalmente que los numeros pares son divisibles por 2.

**Excepcion sutil:** en poblaciones condicionadas por supervivencia, la distribucion de `q mod 8` podria no ser uniforme. Si la supervivencia selecciona preferentemente ciertos residuos, la *prediccion marginal* (promediada sobre `q mod 8`) podria desviarse de 1/2. Pero la *prediccion condicional* (dado `q mod 8`) seguiria siendo correcta, porque la algebra no depende de la frecuencia de cada clase sino de la estructura modular fija.

**Reformulacion recomendada para H1:**

En lugar de confirmar la tabla (lo cual es circular), la pregunta util es:

```text
H1-reformulada: Un modelo que usa P(next_tail | q mod 8) algebraico en vez de
P(next_tail) = Geom(1/2) mejora la prediccion de supervivencia orbital?
Concretamente: un modelo que genera cadenas con next_tail ~ P(. | q mod 8)
reproduce mejor la frecuencia de cadenas largas que el modelo geometrico independiente?
```

Esto conecta directamente con el hallazgo de M9 (sobreproduccion de extremos) y pregunta si la estructura modular es la pieza que faltaba. Si el modelo "modular" produce menos extremos que el geometrico y se acerca mas a los datos reales, tenemos un avance real. Si no, confirmamos que la cancelacion marginal hace que la estructura modular sea irrelevante para la dinamica global.

### Plan concreto

1. **No gastar un slot de H1 en confirmar la tabla algebraica.** Documentarla como Nivel 4 y proceder.

2. **Reformular H1 como comparacion de modelos:**

```text
H1-modelo: Generar cadenas sinteticas con P(next_tail | q_current mod 8) algebraico
(en vez de Geom(1/2)) y comparar la distribucion de blocks_to_descend contra datos reales
y contra el modelo geometrico. Medir si el modelo modular reduce la sobreproduccion de
cadenas largas documentada en M9.
```

- Estadistico: diferencia en frecuencia de `blocks_to_descend >= k` para `k = 10, 15, 20` entre modelo geometrico, modelo modular y datos reales.
- Train: `[3, 5M]`.
- Holdout: `[15M, 25M]`.
- Exito: el modelo modular se acerca significativamente mas a los datos reales que el geometrico en al menos un valor de `k`.
- Abandono: el modelo modular produce la misma o mas sobreproduccion que el geometrico.

3. **Mantener H2, H3, H4 como estan.** No se ven afectadas por el resultado algebraico.

4. **Conteo de tests revisado:** Con H1-modelo en vez de H1-tabla, el conteo baja a 4 hipotesis (H1-modelo, H2, H3, H4), lo cual da alfa por test = `0.05/4 = 0.0125`.

## Criterio exacto de exito

| Condicion | Resultado |
| --- | --- |
| El modelo modular reduce la frecuencia de `blocks_to_descend >= 15` en al menos un 20% respecto del geometrico, y la diferencia modelo_modular - real es menor que modelo_geometrico - real, en train Y holdout | **Exito de H1-modelo.** El modelo modular captura estructura que el geometrico pierde. Habilita formalizacion: ¿por que la cancelacion marginal no protege contra la sobreproduccion? |
| La tabla algebraica `P(next_tail \| q mod 8)` se observa en los datos con menos de 5% de desviacion del valor teorico, en todas las clases, en train y holdout | **Confirmacion trivial.** No cuenta como hallazgo nuevo. Se documenta y se cierra. |
| Calculo algebraico ya integrado como Nivel 4 sin necesidad de holdout | **Resultado algebraico cerrado.** No necesita estadistica. |

## Criterio exacto de abandono

| Condicion | Resultado |
| --- | --- |
| El modelo modular produce la misma sobreproduccion de extremos que el geometrico | **Descarte de H1-modelo.** La estructura `q mod 8` es real pero irrelevante para la dinamica global porque se cancela en el promedio. |
| La unica forma de mejorar el modelo es subir a `q mod 16`, `q mod 32`, etc. | **Descarte por complejidad creciente sin retorno.** Cada nivel agrega refinamiento pero la cancelacion marginal persiste. No hay razon para esperar que el modelo mejore sistematicamente con modulos mas altos. |
| Despues de incorporar `q mod 8`, las H2/H3/H4 tambien se descartan en holdout | **Descarte fuerte de M15 completo.** El modelo geometrico independiente, promediado sobre clases modulares, captura adecuadamente la dinamica. La estructura modular existe pero no tiene consecuencias observables a nivel de cadenas. |

## Resumen de recomendaciones

```text
1. Integrar la tabla algebraica q mod 8 como Nivel 4 a main. Es correcta.
2. NO confirmar la tabla con holdout. Es una tautologia estadistica.
3. Reformular H1 como comparacion de modelo modular vs. geometrico.
4. El test relevante es: ¿mejora la prediccion de cadenas largas?
5. Si no mejora, la estructura modular es real pero dinamicamente irrelevante.
6. Si mejora, tenemos la primera correccion concreta al modelo de Terras/Wagstaff.
```

## Preguntas para Codex orquestador

1. **Acepta la reformulacion de H1?** El cambio es de "confirmar tabla" a "comparar modelos". Si acepta, el script de holdout debe generar cadenas con dos modelos (geometrico y modular) y comparar ambos contra datos reales. Esto requiere un cambio en el diseño del script `m15_train_holdout.py`. *Clasificacion: decision de estrategia.*

2. **Quiere integrar la tabla algebraica a `main` antes del holdout?** La tabla es un resultado solido (Nivel 4) que no depende del holdout. Integrarla temprano permite que H1-modelo la use como insumo. *Clasificacion: decision operativa.*

3. **El resultado algebraico cambia la prioridad de H2 (sobreproduccion de extremos)?** Ahora tenemos una explicacion candidata de por que el modelo geometrico sobreproduce extremos: ignora que `q mod 8` redistribuye `next_tail` drasticamente. Si la cancelacion marginal no es perfecta en cadenas largas (porque las cadenas largas seleccionan residuos no uniformemente), eso explicaria M9. Esto hace que H2 y H1-modelo sean practicamente la misma pregunta mirada desde dos angulos. ¿Conviene fusionarlas en un solo test? *Clasificacion: revision metodologica.*
