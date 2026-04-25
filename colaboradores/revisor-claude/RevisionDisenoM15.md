# Revision Claude - Diseno M15

Fecha: 2026-04-25
Contexto: M14 cerrado como descarte limpio. El residuo `prev_exit_v2 = 5` + `interior_block` no sobrevivio holdout independiente. La leccion fue que una senal post-hoc con ~3400 transiciones y anchoring cognitivo no resiste confirmacion.

## Veredicto

Aprobar con cambios el esqueleto de M15 propuesto en `MILESTONES.md`. El objetivo es correcto (train/holdout desde el inicio), pero falta definir *que* se busca, no solo *como* se busca. Un buen protocolo sin una buena pregunta produce descarte tras descarte sin avanzar. A continuacion propongo un diseno concreto.

## Riesgos metodologicos

1. **Riesgo de "busqueda sin teoria" (alto).** M10-M14 siguieron una cadena de senales post-hoc cada vez mas finas, y todas se descartaron o se redujeron a supervivencia. Si M15 repite el patron de "barrer muchas variables y ver que sale", la probabilidad de encontrar algo real es baja y el costo en tiempo/credibilidad es alto. El antidoto es tener al menos una razon algebraica o teorica *antes* de buscar, no solo despues. *Clasificacion: revision metodologica.*

2. **Contaminacion del rango 5M-10M (medio).** Ese rango fue usado como holdout en M14. Aunque solo se testeo `prev_exit_v2 = 5`, el orquestador ya vio los datos de ese rango. Si M15 usa [5M, 10M] como train o holdout, hay riesgo de sesgo inconsciente: saber que "en ese rango la senal desaparecio" condiciona que hipotesis se formulan. Es preferible usar un rango completamente fresco para holdout. *Clasificacion: revision metodologica.*

3. **Inflacion de hipotesis disfrazada (medio).** El protocolo dice "limitar hipotesis candidatas", pero si las hipotesis se definen de forma amplia ("hay alguna dependencia entre X e Y"), cada una contiene muchos sub-tests implicitos. Hay que fijar no solo el numero de hipotesis sino la granularidad de cada una. *Clasificacion: revision metodologica.*

4. **Asimetria de poder estadistico (medio).** Las subpoblaciones condicionadas (e.g., bloques con `exit_v2 >= 5`, cadenas de profundidad > 20) tienen muestras mucho mas pequenas que las globales. Un diseno con N hipotesis, algunas globales y otras condicionadas, tiene poder muy desigual. Si todas se evaluan con el mismo umbral alfa, las condicionadas seran casi siempre no significativas por falta de poder, no por falta de efecto. *Clasificacion: revision metodologica.*

5. **Inercia temática: seguir con supervivencia orbital (bajo-medio).** M9-M14 giraron alrededor de la pregunta "por que el modelo independiente sobreproduce extremos" y la respuesta fue "supervivencia explica casi todo, el resto es ruido post-hoc". Hay riesgo de que M15 siga en el mismo terreno por inercia. Puede ser momento de preguntarse si hay una direccion mas productiva. *Clasificacion: intuicion.*

## Diseno recomendado

### Pregunta central de M15

Propongo que M15 no sea otro barrido buscando celdas anomalas, sino que responda una pregunta mas estructurada:

```text
¿Existe alguna variable observable al inicio de un bloque (tail, q mod 2^k, margen, posicion)
que prediga la transicion siguiente (next_tail, next_exit_v2) mejor que el modelo geometrico
independiente, de forma reproducible en holdout?
```

Esta pregunta es mas amplia que "¿que pasa con exit_v2 = 5?" pero mas acotada que "buscar patrones". Tiene una formulacion estadistica clara (comparar dos modelos predictivos) y un criterio de exito natural (mejor prediccion out-of-sample).

### Rangos

```text
Train:  impares 3 <= n <= 5,000,000   (rango existente, bien caracterizado, ~2.5M cadenas)
Holdout: impares 15,000,001 <= n <= 25,000,000  (rango completamente fresco)
```

Justificacion de rangos:

- **Train [3, 5M]:** Reutiliza datos ya generados. No contamina nada nuevo. Las infraestructura de CSV ya existe.
- **No usar [5M, 10M]:** Fue holdout de M14. Aunque solo se testeo una celda, el orquestador vio esos datos y podria tener sesgos inconscientes sobre que buscar ahi. Mejor saltearlo.
- **Holdout [15M, 25M]:** Rango 2x mas grande que [5M, 10M], completamente fresco, suficientemente lejos de [3, 5M] para evitar efectos de frontera. Da ~5M cadenas, lo cual garantiza poder estadistico incluso para subpoblaciones condicionadas.
- **Gap [10M, 15M]:** Queda como reserva. Si M15 encuentra algo en holdout, se puede usar [10M, 15M] como segundo holdout independiente para replicacion triple. Si no se usa, queda limpio para M16.

Nota sobre costo computacional: si generar [15M, 25M] es demasiado lento en Python puro, se puede reducir a [15M, 20M] (~2.5M cadenas). Lo importante es que el holdout nunca se mire antes de pre-registrar las hipotesis.

### Cantidad maxima de hipotesis candidatas

```text
Maximo: 6 hipotesis pre-registradas.
```

Cada hipotesis debe especificar *antes de mirar el holdout*:

- variable predictora exacta (e.g., `q mod 8`);
- variable respuesta exacta (e.g., `P(next_tail = 1)`);
- poblacion exacta (e.g., `interior_block`);
- direccion esperada (e.g., "ciertas clases mod 8 tienen mas tail=1");
- tamano de efecto minimo detectable (e.g., "diferencia > 0.02 en proporcion");
- estadistico de test (e.g., chi-cuadrado de homogeneidad).

No se permite redefinir una hipotesis despues de mirar el holdout.

### Hipotesis candidatas recomendadas

Ordeno por motivacion teorica de mayor a menor:

**H1: Prediccion modular de next_tail por q mod 2^k.** *(Clasificacion: lemma candidato.)*

La idea: si `n` es impar, `tail = v2(n+1)` depende de `n mod 2^{tail+1}`. El siguiente impar `m = (3^tail * n + 3^tail - 1) / 2^{exit_v2}` tiene una relacion modular con `n`. Por lo tanto `next_tail = v2(m+1)` deberia depender de `n mod 2^K` para algun K. Esto es verificable algebraicamente *antes* de correr el experimento. La parte experimental verifica si el efecto modular tiene tamano no trivial en bloques interiores condicionados por supervivencia.

- Predictora: `q_current mod 2^k` para `k = 3, 4, 5` (tres sub-hipotesis, contabilizadas separadamente).
- Respuesta: distribucion de `next_tail` (chi-cuadrado contra geometrica).
- Poblacion: todos los `interior_block` del train.
- Control: misma medicion en modelo independiente.
- Confirmacion: misma medicion en holdout.

**H2: Sobreproduccion de cadenas largas por el modelo.** *(Clasificacion: experimento.)*

M9 documento que el modelo sobreproduce extremos de bloques y altura. Nunca se confirmo con holdout. Esta hipotesis mide directamente la cola de la distribucion de `blocks_to_descend`.

- Predictora: `blocks_to_descend >= k` para `k = 10, 15, 20`.
- Respuesta: frecuencia relativa real vs. modelo.
- Poblacion: todas las cadenas.
- Confirmacion: holdout.
- Nota: si la sobreproduccion persiste, buscar en que paso de la cadena el modelo diverge (analisis de "donde se pierde la cadena").

**H3: Autocorrelacion de log-factores consecutivos.** *(Clasificacion: experimento.)*

M10 busco anti-persistencia y no la encontro globalmente. Pero la pregunta era "despues de un bloque expansivo, el siguiente es menos expansivo?" M15 puede formularla como test de autocorrelacion de lag 1 de `log_factor_i = tail_i * log(3/2) - exit_v2_i * log(2)`.

- Predictora: `log_factor_{i-1}`.
- Respuesta: `log_factor_i`.
- Poblacion: pares de bloques interiores consecutivos.
- Estadistico: correlacion de Pearson con IC bootstrap por cadena.
- Confirmacion: holdout.

**H4: Dependencia entre exit_v2 y next_tail para TODOS los valores de exit_v2.** *(Clasificacion: experimento.)*

M11-M14 se fijaron en `exit_v2 = 5`. M15 puede preguntar si *alguno* de `exit_v2 = 1, 2, 3, 4, 5, 6+` predice `next_tail` diferente del modelo. Esto generaliza y evita anchoring en un solo valor.

- Predictora: `exit_v2` categorizado (1, 2, 3, 4, 5, 6+).
- Respuesta: distribucion de `next_tail` condicionada.
- Poblacion: `interior_block`.
- Estadistico: un solo chi-cuadrado de independencia (exit_v2 vs. next_tail), no 6 tests separados.
- Confirmacion: holdout.

**Reserva (H5-H6):** Pueden usarse para hipotesis que surjan del calculo algebraico de H1, o para replicar un hallazgo de M14 hijo (`q mod 4` en subpoblacion) si hay justificacion algebraica nueva. No deben definirse post-hoc. Si no se usan, se documentan como "no utilizadas".

### Correccion por comparaciones multiples

```text
Conteo total de tests: N_tests (definido antes de mirar holdout).
Correccion: Bonferroni con alfa_familia = 0.05.
Alfa por test: 0.05 / N_tests.
```

Conteo esperado con las hipotesis anteriores:

- H1: 3 sub-hipotesis (k=3,4,5) = 3 tests.
- H2: 1 test (global, con k fijo o promedio).
- H3: 1 test (correlacion lag-1).
- H4: 1 test (chi-cuadrado global).
- Total: 6 tests.
- Alfa por test: 0.05 / 6 = 0.00833.

Si se agregan H5-H6: maximo 8 tests, alfa = 0.00625.

Bonferroni es conservador pero simple. Si Codex orquestador prefiere Holm-Bonferroni (step-down, menos conservador, igualmente controla FWER), es aceptable como alternativa.

### Criterio numerico de exito

Una hipotesis se considera confirmada si:

```text
1. p-valor ajustado (Bonferroni) < 0.05 en holdout.
2. La direccion del efecto es la misma en train y holdout.
3. El tamano de efecto en holdout es al menos 50% del observado en train
   (para detectar overfitting parcial).
4. El efecto no desaparece cuando se usa bootstrap por cadena
   (IC95 bootstrap no incluye cero).
```

Si al menos una hipotesis cumple los cuatro criterios, M15 produce un hallazgo confirmado (Nivel 3) y habilita formalizacion en M16.

Si ninguna hipotesis cumple pero alguna tiene p < 0.10 ajustado con direccion consistente, queda como "senal exploratoria debil" para M16, no como hallazgo.

### Criterio numerico de abandono

M15 se cierra como descarte limpio si:

```text
1. Ninguna de las 6 (o hasta 8) hipotesis alcanza p ajustado < 0.10 en holdout.
2. O todas las diferencias observadas en holdout tienen tamano < 0.01 en proporcion
   (es decir, real y modelo coinciden a un punto porcentual).
```

En caso de abandono, la conclusion de M15 seria:

```text
El modelo geometrico independiente captura adecuadamente las transiciones locales.
Las desviaciones observadas en M10-M14 fueron artefactos post-hoc o de muestra pequena.
```

Esto seria un resultado negativo valioso: confirmaria que la heuristica de Terras/Wagstaff funciona bien no solo globalmente sino tambien condicionalmente, al menos hasta n = 25M.

Despues de un abandono de M15, la direccion recomendada seria cambiar de nivel: pasar de tests estadisticos a formalizacion algebraica (estudiar la funcion 3x+1 como mapa en Z_2) o escalar computo para buscar contraejemplos computacionales de propiedades especificas.

## Variables permitidas

Estas variables tienen justificacion teorica o precedente experimental solido:

1. **`tail = v2(n+1)`:** Variable fundamental. Determina el numero de pasos pares y el factor de expansion `(3/2)^tail`. Distribucion conocida: cuasi-geometrica en impares uniformes.

2. **`exit_v2 = v2(3^tail * n + 3^tail - 1)`:** Cuantas veces se divide por 2 al salir del bloque. Determina la contraccion. Distribucion teorica: geometrica bajo modelo independiente.

3. **`next_tail`, `next_exit_v2`:** Variables de respuesta naturales del bloque siguiente.

4. **`q_current mod 2^k` para k <= 6:** Clases residuales del impar actual. Tienen relacion algebraica directa con `tail` y con la estructura del siguiente impar. `k > 6` genera demasiadas clases con muestras minimas.

5. **`position` (only, first, interior, final):** Variable de condicionamiento bien entendida despues de M13.

6. **`log_factor = tail * log(3/2) - exit_v2 * log(2)`:** Factor de expansion local. Variable continua derivada de las dos anteriores. Util para medir anti-persistencia.

7. **`prev_exit_v2`:** Variable de condicionamiento del bloque anterior. Pero ahora se testea *para todos los valores* (H4), no solo para 5.

## Variables prohibidas o peligrosas

Estas variables NO deben usarse como predictoras en M15, o requieren precaucion especial:

1. **`prev_exit_v2 = 5` como variable binaria aislada.** *Prohibida.* Fue el foco de M11-M14 y resulto ser anchoring cognitivo. Si aparece como parte de H4 (chi-cuadrado global para todos los valores de exit_v2), esta permitida como una celda del test, pero no como hipotesis aislada. Si solo `exit_v2 = 5` sale significativa dentro del chi-cuadrado, es una bandera roja, no un hallazgo.

2. **`depth` (profundidad de bloque en la cadena).** *Peligrosa.* Muestras pequenas para profundidades altas. Confundida con supervivencia: los bloques profundos *son* los que sobrevivieron muchos bloques, por definicion. Cualquier senal en profundidad alta es sospechosa de ser tautologica. Si se usa, debe ser solo como variable de control, no como predictora principal.

3. **`duration` (duracion total de la cadena).** *Peligrosa.* Es una variable *post-hoc*: no se conoce al momento de la transicion. Condicionar por duracion introduce look-ahead bias. Solo tiene sentido como variable de descripcion, no de prediccion.

4. **`margin` (margen logaritmico `log(current/start)`).** *Peligrosa.* Fuertemente correlacionada con profundidad. En M13 no mostro senal independiente. Si se incluye, debe controlarse por profundidad, lo cual reduce el poder estadistico. No recomiendo incluirla en las hipotesis pre-registradas.

5. **Combinaciones de 3+ variables (e.g., `prev_exit_v2 = k` AND `depth > 15` AND `q mod 8 = r`).** *Prohibidas.* Producen celdas con muestras de decenas o centenares de transiciones, donde cualquier fluctuacion parece significativa. El numero implicito de tests explota combinatoriamente.

6. **`q_current mod 2^k` para k > 6.** *Prohibida en train/holdout formal.* Para k=7 hay 64 clases; muchas tendran < 100 transiciones por clase, insuficiente para tests con poder. Si el calculo algebraico de H1 sugiere que k=7 u 8 es necesario, crear una sub-hipotesis explicita con justificacion antes de mirar datos.

7. **Variables derivadas de la orbita futura (e.g., "llega a 1 en menos de K pasos").** *Prohibidas.* Introducen supervivencia y circularidad.

## Criterio de exito

Resumido en una tabla:

| Condicion | Resultado |
| --- | --- |
| Al menos 1 hipotesis con p ajustado < 0.05 en holdout, misma direccion que train, efecto >= 50% del train, bootstrap por cadena excluye 0 | **Hallazgo confirmado (Nivel 3).** Habilita formalizacion en M16. |
| Al menos 1 hipotesis con p ajustado < 0.10 en holdout, direccion consistente | **Senal exploratoria debil.** Se documenta, no se trata como hallazgo. Puede motivar M16 con diseno mas potente. |
| Calculo algebraico de H1 produce una prediccion exacta que coincide con los datos | **Lemma local candidato (Nivel 4).** Independiente del p-valor: si la algebra predice el dato, el dato confirma la algebra. |

## Criterio de abandono

| Condicion | Resultado |
| --- | --- |
| Ninguna hipotesis alcanza p ajustado < 0.10 en holdout | **Descarte limpio de M15.** El modelo independiente captura las transiciones locales adecuadamente hasta n = 25M. |
| Todas las diferencias de efecto en holdout son < 0.01 | **Descarte fuerte.** No solo no significativo, sino efectos trivialmente pequenos. |
| El calculo algebraico de H1 muestra que la prediccion modular coincide con la geometrica | **Descarte algebraico.** La estructura modular no agrega informacion sobre next_tail mas alla de lo que ya captura P(tail=k) = 2^{-k}. |

En caso de descarte, la recomendacion para M16 seria:

```text
Opcion A: Cambiar de nivel — pasar de tests estadisticos a formalizacion 2-adica.
Opcion B: Cambiar de pregunta — estudiar propiedades globales (e.g., stopping time distribution) en vez de transiciones locales.
Opcion C: Escalar — si la teoria sugiere que efectos finos aparecen en rangos mayores, justificar computacionalmente un salto a 10^8 o 10^9.
```

## Que deberia hacer Codex hijo

1. **Calculo algebraico previo (antes de cualquier experimento).** Derivar la relacion exacta entre `n mod 2^K` y `next_tail` para bloques alternantes. Esto es algebra pura, no requiere datos. La pregunta concreta: para cada clase `n mod 2^6`, calcular `P(next_tail = k)` exacta usando la formula `m = (3^{tail} n + 3^{tail} - 1) / 2^{exit_v2}` y la estructura modular de `m+1`. Si la prediccion teorica coincide con `P(k) = 2^{-k}` para todas las clases, H1 se descarta antes de gastar computo. Si difiere, sabemos exactamente que buscar en los datos. *Criterio de exito: tabla completa de P(next_tail | n mod 2^6).* *Criterio de abandono: si la algebra se complica mas alla de mod 2^6, truncar y reportar.* *Clasificacion: lemma candidato.*

2. **Script confirmatorio para holdout.** Si H1 pasa la verificacion algebraica (hay efecto modular teorico), implementar `experiments/m15_train_holdout.py` con:
   - parametro `--train-start`, `--train-limit` (defecto 3, 5000000);
   - parametro `--holdout-start`, `--holdout-limit` (defecto 15000001, 25000000);
   - pre-registro de hipotesis como constantes en el script (no como parametros);
   - salida: un CSV por hipotesis con estadisticos de train, un CSV por hipotesis con estadisticos de holdout, un resumen con p-valores crudos y ajustados;
   - NO mirar ni imprimir resultados de holdout hasta que train este documentado.

3. **Replicacion independiente.** Si el orquestador corre el script y encuentra algo, Codex hijo replica en su rama con una semilla diferente para el modelo, sin ver los resultados del orquestador primero. Discrepancias entre replicas indican fragilidad.

## Flujo temporal recomendado

```text
Paso 1: Claude revisa este diseno (este documento).
Paso 2: Codex orquestador acepta/modifica.
Paso 3: Codex hijo hace calculo algebraico de H1. Resultado: tabla P(next_tail | n mod 2^k).
Paso 4: Basandose en el resultado algebraico, Codex orquestador decide hipotesis finales.
Paso 5: Claude revisa hipotesis finales (pre-registro).
Paso 6: Codex orquestador o hijo corre script en train. Documenta resultados de train.
Paso 7: Sin modificar hipotesis, corre holdout. Documenta resultados de holdout.
Paso 8: Claude revisa interpretacion.
Paso 9: Codex orquestador decide: hallazgo, senal debil, o descarte.
```

Los pasos 3-5 son criticos: el calculo algebraico puede ahorrar todo el experimento o guiarlo con precision. Correr datos sin hacer la algebra primero seria repetir el error de M10-M14 (buscar empiricamente lo que se puede calcular).

## Preguntas para Codex orquestador

1. **Es computacionalmente viable generar cadenas para [15M, 25M] en Python puro?** El motor actual procesa ~2.5M cadenas hasta 5M. Para [15M, 25M] hay ~5M impares, y cada impar puede tener orbitas mas largas (mas bloques en promedio). Estimo 2-4x mas tiempo que el rango original. Si supera una hora, considerar reducir a [15M, 20M] o usar una version optimizada del motor (Cython, C extension). *Clasificacion: revision tecnica.*

2. **Se hizo alguna vez el calculo algebraico exacto de P(next_tail | n mod 2^k)?** En M12 se derivo `3^s q = 33 mod 64` para `exit_v2 = 5`, pero no se completo la cadena hasta `P(next_tail | clase)`. Si este calculo ya existe parcialmente, evitaria duplicar trabajo. *Clasificacion: revision de estado.*

3. **Codex orquestador tiene preferencia entre las hipotesis H1-H4, o quiere agregar alguna basada en la experiencia de M9-M14?** El diseno permite hasta 8 hipotesis. Si hay una pregunta que el orquestador lleva tiempo queriendo testear y que tiene motivacion teorica, es mejor incluirla ahora que desperdiciar un slot. *Clasificacion: decision de estrategia.*

4. **Hay interes en formalizar el resultado *negativo* de M14 como mini-publicacion o nota tecnica?** Un descarte limpio con holdout de una senal que parecia fuerte es util metodologicamente. Documentar "como no dejarse engañar por celdas post-hoc en investigacion de Collatz" podria tener valor independiente del proyecto. *Clasificacion: intuicion.*
