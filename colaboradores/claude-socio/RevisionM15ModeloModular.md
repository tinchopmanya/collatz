# Plantilla de revision ClaudeSocioCritico

Fecha: 2026-04-25
Tema: M15 - modelo modular `P(next_tail | q mod 8)` vs modelo geometrico independiente para predecir supervivencia orbital
Material revisado:
- `MILESTONES.md` (M0-M15)
- `colaboradores/orquestador/ArquitecturaTrabajoMultiagenteCollatz.md`
- `colaboradores/orquestador/PromptsM15Ronda1.md`
- `colaboradores/orquestador/DecisionM15TrasAlgebraReplicaYClaude.md`
- `colaboradores/orquestador/DecisionM15TrasInformeInvestigadorWeb.md`
- `colaboradores/investigador-web/InformeM15ModeloModularLiteratura.md`
- `colaboradores/codex-hijo/ResultadosM15Algebra.md`
- `colaboradores/codex-hijo/ReplicaM15Algebra.md`

## Veredicto

Aprobar con cambios.

La pregunta tiene sustancia cientifica, pero el experimento propuesto necesita reformulacion para evitar un resultado trivialmente positivo que no aporte informacion util.

## Critica central

Punto mas debil:

El modelo modular `P(next_tail | q mod 8)` va a ganar contra el geometrico independiente en prediccion local de `next_tail` por construccion algebraica. Ya sabemos que las probabilidades difieren clase por clase (5/6, 2/3, 1/6, 1/3 vs 1/2 uniforme). Medir eso en train/holdout seria confirmar una identidad, no un descubrimiento. El riesgo es declarar "el modelo modular gana" cuando el resultado estaba garantizado desde el algebra.

La pregunta real, que todavia no esta bien formulada, es si esa ventaja local en `next_tail` se propaga a metricas de cadena completa (`blocks_to_descend`, stopping time, supervivencia orbital). Esa propagacion no es obvia: depende de si `q mod 8` tiene memoria entre bloques consecutivos o si se re-mezcla rapidamente. El orquestador lo identifico correctamente en `DecisionM15TrasAlgebraReplicaYClaude.md` ("la pregunta crucial es si las cadenas largas seleccionan residuos `q mod 8` de manera no uniforme"), pero la formulacion operacional de H1 todavia no incorpora esa distincion con suficiente precision.

Punto mas fuerte:

El proyecto ha construido un pipeline limpio de descarte: M12 descarto `exit_v2 = 5` como lemma, M14 descarto el residuo `prev_exit_v2 = 5 + interior_block` via holdout independiente. La disciplina de abandonar pistas es rara y valiosa. M15 hereda esa disciplina si se ejecuta bien.

Riesgo de autoengano:

Medio-alto. El mecanismo de autoengano especifico seria: medir la mejora del modelo modular en `next_tail` bloque a bloque (que esta garantizada algebraicamente), reportar un delta positivo en holdout, y concluir que el modelo modular "mejora la prediccion de supervivencia orbital" cuando en realidad solo se confirmo una identidad local sin demostrar propagacion a metricas de cadena.

## Revision de novedad

La idea parece:

- Conocida: la dependencia de `next_tail` respecto de `q mod 8` es una consecuencia directa de la aritmetica modular del mapa acelerado. Terras (1976), Lagarias (1985), Kontorovich-Lagarias (2009) establecen el marco. La tabla exacta `5/6, 2/3, 1/6, 1/3` puede no estar tabulada explicitamente, pero es derivable en una pagina de algebra.
- Implicita: la comparacion entre un modelo condicionado por residuos 2-adicos y el baseline geometrico esta implicita en toda la literatura de modelos estocasticos para Collatz. Kontorovich-Lagarias muestran que las o-sequences tienen distribucion geometrica en densidad natural; condicionar por un cilindro 2-adico bajo cambia esa distribucion localmente, pero el promedio marginal cancela.
- Reformulacion util: si, como ablation experimental interna. La pregunta "cuanta informacion predictiva sobre supervivencia orbital contiene `q mod 8` mas alla de lo que da el geometrico?" es una formulacion limpia que no encontro el InvestigadorWeb en la literatura exacta.
- Potencialmente nueva: no como matematica. Posiblemente como experimento computacional si se mide propagacion a cadena, no solo el primer bloque.

## Revision tecnica

Errores posibles:

1. Confundir mejora local (prediccion de `next_tail` bloque a bloque) con mejora global (prediccion de supervivencia orbital o stopping time). La primera esta garantizada; la segunda no. El experimento debe medir exclusivamente la segunda.

2. El modelo modular necesita una regla de transicion de estado. Si `q_i mod 8` se trata como i.i.d. uniforme entre bloques, el modelo colapsa al geometrico en el margen porque `(1/4)(5/6 + 2/3 + 1/6 + 1/3) = 1/2`. Si se usa la transicion real `q_{i+1} mod 8 = f(q_i mod 8, tail_i, exit_v2_i)`, el modelo se vuelve un automata finito acoplado y el experimento mide algo distinto: la estructura de la cadena de Markov modular. Esa segunda opcion es mas interesante pero tambien mas compleja y con mas grados de libertad.

3. La poblacion condicionada importa. Kontorovich-Lagarias demuestran propiedades en densidad natural (promedios sobre todos los enteros). Las cadenas que sobreviven muchos bloques sin descender son una subpoblacion sesgada. La mejora del modelo modular podria aparecer o desaparecer segun como se defina la poblacion. El diseño debe especificar esto antes de correr datos.

Tautologias:

La hipotesis "el modelo modular predice `next_tail` mejor que el geometrico" es tautologica. Ya lo sabemos por algebra. La hipotesis operacional debe ser estrictamente sobre metricas de cadena: `blocks_to_descend`, stopping time, o probabilidad de supervivencia a profundidad `d`.

Contaminacion train/holdout:

El diseño actual es correcto en principio: el rango `n <= 5000000` esta quemado como exploratorio, `5000001-10000000` fue holdout de M14, y se propone `15000001-25000000` como holdout fresco. Sin embargo, hay un riesgo sutil: si el modelo modular se calibra en train y luego se evalua en holdout midiendo `next_tail`, la mejora en holdout esta pre-garantizada por algebra y no consume grados de libertad reales. El holdout solo tiene valor si la metrica es de cadena completa, no de bloque individual.

Comparaciones multiples:

Bajo si se mantiene la disciplina de una sola H1 pre-registrada. El riesgo sube si despues del primer resultado se agregan comparaciones por `q mod 16`, por profundidad, por margen, etc. La regla de maximo 6 tests del diseño M15 en MILESTONES es razonable pero debe incluir un presupuesto de alfa explicito (e.g., Bonferroni con alfa = 0.05/6 por test).

Variables prohibidas o peligrosas:

- `next_tail` como metrica objetivo del holdout: peligrosa porque la mejora es tautologica. Usar solo como variable intermedia, no como criterio de exito.
- `q mod 16` o superior: peligrosa por multiplicidad. No abrir hasta que `q mod 8` muestre o no muestre propagacion a cadena.
- Cualquier variable derivada de la cadena futura (e.g., "max_height" o "total_steps") como feature de entrada: contaminacion temporal.

## Recomendacion

Que haria ahora:

1. Reformular H1 explicitamente como hipotesis de propagacion a cadena. No "el modelo modular predice `next_tail` mejor" (eso es algebra), sino: "el modelo modular con transicion de estado `q mod 8` predice `P(blocks_to_descend >= d)` mejor que el geometrico independiente para `d >= 3`." Esa es la pregunta no trivial.

2. Antes de tocar datos, calcular algebraicamente la matriz de transicion `q_{i+1} mod 8` dado `q_i mod 8`. Si esa matriz es (o converge rapidamente a) la uniforme `(1/4, 1/4, 1/4, 1/4)`, entonces el modelo modular colapsa al geometrico despues de pocos bloques y M15 se puede descartar sin holdout. Esa es la pregunta algebraica que mata o valida el experimento.

3. Si la matriz de transicion tiene autovalores no triviales (i.e., la mezcla es lenta), entonces si tiene sentido un experimento train/holdout. En ese caso, definir: train = `n in [1, 5000000]` para calibrar la transicion, holdout = `n in [15000001, 25000000]` para medir mejora en `blocks_to_descend` o stopping time. Metrica: log-likelihood ratio del modelo modular vs geometrico sobre las cadenas holdout completas.

4. No activar CodexHijo1 para implementar el script de comparacion todavia. Activarlo solo para calcular la matriz de transicion `q mod 8` entre bloques consecutivos. Eso es una tarea algebraica/computacional pequena, verificable, y con criterio de abandono claro.

Que no haria:

1. No correria holdout midiendo solo `next_tail` bloque a bloque. Eso confirma una identidad, no un descubrimiento.
2. No abriria `q mod 16` ni `q mod 32` antes de resolver la pregunta de mezcla en `q mod 8`.
3. No declararia mejora predictiva sin haber verificado que la transicion de estado tiene memoria suficiente para propagarse a cadena.
4. No presentaria ningun resultado de M15 como "novedad matematica". Nivel maximo honesto: Nivel 2 (conocido pero util para el modelo interno) o Nivel 3 (formulacion experimental propia de algo implicito).

Criterio de exito:

El experimento M15 tiene exito si: (a) la matriz de transicion `q mod 8` tiene mezcla lenta (autovalor subdominante > 0.3); (b) el modelo modular mejora el log-likelihood sobre cadenas holdout completas con p < 0.01 tras correccion; (c) la mejora tiene la misma direccion en train y holdout; (d) la mejora persiste al controlar por longitud de bloque previo.

Criterio de abandono:

Abandonar M15 si: (a) la matriz de transicion converge a la uniforme en 2-3 pasos (mezcla rapida), porque implica que `q mod 8` no tiene memoria suficiente para afectar cadenas; (b) el modelo modular no mejora en holdout; (c) la mejora solo aparece al subir a modulos mas altos sin principio de parada; (d) se necesitan mas de 6 tests para encontrar una senal.

## Preguntas para el orquestador

1. La matriz de transicion `q_{i+1} mod 8 | q_i mod 8` ya fue calculada en alguna parte del proyecto? No la encontre en los archivos revisados. Si no existe, esa es la tarea que deberia preceder a cualquier diseño experimental. Es computable algebraicamente (no requiere datos grandes) y su resultado determina si M15 tiene sentido o se puede descartar en frio.

2. Cuando se dice "supervivencia orbital" como metrica objetivo, se refiere a `P(blocks_to_descend >= d)` para un `d` fijo, o a la distribucion completa de `blocks_to_descend`? La eleccion importa para la potencia estadistica del test y para evitar comparaciones multiples implícitas sobre distintos umbrales `d`.

3. Existe un inventario explicito de cuantos tests/comparaciones se hicieron en M13 y en la exploracion del Codex hijo que genero la pista original? El conteo conservador de M14 fue 10-15, pero no vi un listado exhaustivo. Ese inventario importa porque M15 hereda el contexto de que estamos buscando en una region sugerida por exploracion previa, no por teoria pura.
