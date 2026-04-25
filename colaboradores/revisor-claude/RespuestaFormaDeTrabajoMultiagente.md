# Respuesta de Claude - Forma de trabajo multiagente

Fecha: 2026-04-25
Revision de: `FormaDeTrabajoMultiagente.md` v0.1

## Veredicto

Aprobar con cambios.

El protocolo es inusualmente bueno para un proyecto de investigacion exploratoria con LLMs. La estructura de preguntas antes/despues de cada ola, los niveles de evidencia, la separacion de roles y la resistencia a sobreinterpretacion son solidos. Los cambios que propongo no son estructurales sino de calibracion y de proteccion contra problemas sutiles que aparecen con multiples agentes.

## Riesgos principales

1. **Comparaciones multiples no controladas (riesgo epistemico, alto).** El residuo `prev_exit_v2 = 5` + `interior_block` fue encontrado despues de condicionar por posicion, profundidad, margen, duracion, prev_exit_v2 y sus combinaciones. Se testearon decenas de subgrupos. Encontrar *una* celda significativa entre muchas es exactamente lo que se espera por azar al 5%. Este riesgo no esta documentado en ningun reporte del repo. Sin correccion por comparaciones multiples (Bonferroni, Benjamini-Hochberg, o al menos un conteo explicito de tests realizados), la significancia del residuo es indeterminada. *Clasificacion: revision metodologica.*

2. **Confirmacion en cascada entre agentes (riesgo estructural, medio).** Si Codex orquestador formula la hipotesis, Codex hijo la testea y Claude la revisa, los tres ven el mismo dato con el mismo framing. El riesgo es que nadie proponga la hipotesis nula agresiva. El protocolo dice "filtro epistemico" pero no tiene un mecanismo formal de adversario: alguien cuyo trabajo explicito sea destruir la hipotesis favorita. *Clasificacion: cambio al protocolo.*

3. **Muestra pequena en la celda clave (riesgo tecnico, medio-alto).** La celda `prev_exit_v2 = 5` + `interior_block` tiene 3426 transiciones reales y 3452 modeladas. Para una diferencia de ~4.7 puntos porcentuales, el poder estadistico es marginal. El IC95 es [0.023, 0.070], que excluye cero pero es amplio. Un bootstrap o permutation test independiente deberia confirmar antes de invertir esfuerzo en M14. *Clasificacion: experimento.*

## Cambios propuestos al protocolo

1. **Agregar conteo explicito de tests y correccion por comparaciones multiples.** En cada reporte que busque senales condicionadas, incluir una tabla de todos los subgrupos testeados, con un p-valor ajustado (Bonferroni como piso, BH como alternativa). Sin esto, cualquier hallazgo en una celda entre muchas es sospechoso. Incluir en la plantilla de ola un campo: `Numero total de tests realizados:` y `Correccion aplicada:`. *Clasificacion: revision metodologica.*

2. **Instituir una "prueba de destruccion" obligatoria antes de avanzar de milestone.** Antes de abrir M14, alguien (preferentemente Claude o un agente separado) debe intentar explicar el residuo por al menos dos mecanismos triviales: (a) efecto de muestra pequena con permutation test, (b) mezcla de Simpson por otra variable no incluida en el modelo. Solo si el residuo sobrevive ambos ataques se justifica invertir un milestone completo. *Clasificacion: cambio al protocolo.*

3. **Separar "busqueda exploratoria" de "confirmacion dirigida" en el ciclo de ola.** Actualmente la misma ola busca senales y las interpreta. Propongo que cuando se busquen senales en muchos subgrupos (como M13), la ola termine con "candidatos a confirmar", y la siguiente ola sea *solo* confirmacion pre-registrada de esos candidatos con muestra independiente o test de permutacion. Esto evita que el mismo dataset que genera la hipotesis la "confirme". *Clasificacion: cambio al protocolo.*

4. **Definir un umbral de abandono numerico para M14.** El protocolo tiene criterios de abandono cualitativos ("si desaparece la senal"). Propongo un umbral concreto: si despues de correccion por comparaciones multiples el p-valor ajustado de la celda clave supera 0.01, se abandona M14 y se documenta como descarte. *Clasificacion: revision metodologica.*

## Como deberia participar Claude

1. **Auditor de rigor estadistico.** Revisar cada reporte buscando errores metodologicos concretos: comparaciones multiples, tamanio de muestra, seleccion de subgrupos post-hoc, interpretaciones que exceden la evidencia. Escribir dictamenes cortos en `colaboradores/revisor-claude/`. *Clasificacion: revision metodologica.*

2. **Generador de hipotesis alternativas y nulas agresivas.** Antes de que Codex orquestador invierta en un milestone, Claude debe proponer al menos una explicacion alternativa que haga innecesaria la senal (mezcla, sesgo de seleccion, artefacto de discretizacion, resultado ya conocido). Si Claude no puede destruir la hipotesis, eso le da mas credibilidad. *Clasificacion: intuicion + revision literatura.*

3. **Conector con literatura existente.** Revisar si un hallazgo ya esta cubierto por trabajos conocidos (Terras, Lagarias, Kontorovich-Miller, Tao 2019, Monks, Wirsching, Campbell 2025, Bonacorsi-Bordoni 2026) y documentar la conexion o la diferencia concreta. Escribir en `colaboradores/revisor-claude/NotasLiteratura.md`. *Clasificacion: revision literatura.*

4. **Revisor de diseño experimental antes de ejecucion.** Cuando Codex orquestador proponga un nuevo script o experimento, Claude deberia revisar el diseño *antes* de correrlo: variables de control, tamanio de muestra necesario, que constituiria un resultado positivo vs. negativo, y trampas estadisticas previsibles. *Clasificacion: revision metodologica.*

## Que no deberia hacer Claude

1. **Ejecutar experimentos computacionales grandes ni escribir scripts de produccion.** Claude no tiene acceso persistente al entorno de ejecucion, y duplicar el trabajo de Codex/Codex hijo solo agrega ruido. Claude puede sugerir pseudocodigo o correcciones, pero no debe ser quien corra `analyze_survival_bias.py`. *Clasificacion: descarte de rol.*

2. **Modificar archivos centrales (`Conlusion.md`, `MILESTONES.md`, `Investigacion*.md`, `src/`, `tests/`).** Claude trabaja en `colaboradores/revisor-claude/` y solo ahi. Si un hallazgo de Claude merece integrarse, Codex orquestador lo traduce y lo integra. Esto evita conflictos y mantiene una sola voz editorial en `main`. *Clasificacion: protocolo.*

3. **Validar o aprobar un hallazgo sin haberlo intentado destruir primero.** Si Claude dice "el residuo parece interesante", debe haber intentado al menos una explicacion alternativa concreta antes. Aprobacion sin ataque es peor que silencio. *Clasificacion: protocolo.*

4. **Buscar conexiones vagas con papers sin especificar que seccion, que resultado o que formula es relevante.** "Esto se parece a Tao 2019" no sirve. "Tao 2019 Theorem 1.3 muestra que para casi todo n la orbita baja de f(n), lo cual implica que nuestro condicionamiento por supervivencia selecciona un conjunto de medida logaritmica cero, y eso podria amplificar artefactos" si sirve. *Clasificacion: revision literatura.*

## Archivos o carpetas que Claude puede tocar

1. `colaboradores/revisor-claude/RespuestaFormaDeTrabajoMultiagente.md` (este archivo).
2. `colaboradores/revisor-claude/RevisionM14.md` (futuras revisiones de milestones).
3. `colaboradores/revisor-claude/NotasLiteratura.md` (conexiones con papers).
4. Cualquier archivo nuevo dentro de `colaboradores/revisor-claude/`.

## Archivos o carpetas que Claude no debe tocar sin permiso

1. `Conlusion.md`, `MILESTONES.md`, `Investigacion*.md`, `README.md`.
2. `src/`, `tests/`, `experiments/`.
3. `reports/` (territorio de Codex orquestador).
4. Cualquier archivo fuera de `colaboradores/revisor-claude/`.

## Primera tarea recomendada para M14

**Nombre:** Prueba de destruccion del residuo `prev_exit_v2 = 5` + `interior_block` por permutacion y comparaciones multiples.

**Tipo:** Experimento + revision metodologica.

**Descripcion concreta:** Antes de descomponer el residuo por variables nuevas, verificar que el residuo sobrevive dos ataques:

1. **Permutation test (10000 permutaciones):** Dentro de las transiciones `interior_block`, permutar aleatoriamente las etiquetas `prev_exit_v2 = 5` vs. otros valores de `prev_exit_v2`, y medir cuantas permutaciones producen una diferencia en `P(tail=1)` tan grande o mayor que la observada (0.04657). Si el p-valor de permutacion supera 0.01, el residuo es compatible con ruido.

2. **Correccion por comparaciones multiples:** Contar todos los subgrupos testeados en el reporte M13 (posicion x prev_exit_v2 x profundidad x margen, etc.), calcular cuantas celdas se examinaron, y aplicar Bonferroni sobre el p-valor de la celda clave. Si el p-valor ajustado supera 0.01, documentar como "senal no robusta" y cerrar M14 como descarte limpio.

**Ejecutor sugerido:** Codex hijo, con script nuevo `experiments/test_residual_robustness.py`.

**Criterio de exito:** El residuo sobrevive ambos tests con p-valor ajustado < 0.01. En ese caso, M14 continua con descomposicion por residuos modulares.

**Criterio de abandono:** El p-valor ajustado supera 0.01, o el permutation test muestra que el efecto es compatible con fluctuacion aleatoria en muestras de tamanio ~3400. En ese caso, M14 se cierra con conclusion: "el residuo es compatible con ruido post-hoc" y se busca nueva direccion.

**Salida esperada:** Un CSV con distribucion de diferencias bajo permutacion, un p-valor de permutacion, un conteo de tests totales, y un p-valor ajustado. Reporte breve en `reports/`.

## Critica del hallazgo actual

El residuo `prev_exit_v2 = 5` + `interior_block` es **sospechoso antes de ser prometedor**, por tres razones concretas:

**1. Seleccion post-hoc no corregida.**
El analisis M13 examino combinaciones de posicion (4 niveles) x prev_exit_v2 (al menos 5 niveles testeados: 1,2,3,4,5) x profundidad (al menos 4 niveles) x margen (al menos 6 niveles). Conservadoramente, se testearon al menos 20-30 celdas con intervalos de confianza al 95%. Encontrar una celda con IC que no incluya cero es lo esperado si no hay senal real. El reporte no menciona este problema en ningun lugar.

**2. La historia de `exit_v2 = 5` en el repo sugiere anchoring.**
`exit_v2 = 5` aparece como "interesante" desde M10, se investiga en M11, se formaliza en M12 (donde se concluye que *no* es una ley local), y reaparece en M13 condicionado por supervivencia. Hay un riesgo de anchoring cognitivo: el valor 5 se ha convertido en el "favorito" de la investigacion, y cada ola lo busca con nuevas lentes. Esto no invalida el hallazgo, pero exige un estandar de evidencia mas alto que para un hallazgo que aparece por primera vez.

**3. Tamanio de muestra marginal.**
3426 transiciones dan un error estandar de `sqrt(0.45 * 0.55 / 3426)` que es aprox. 0.0085. La diferencia observada (0.047) es ~5.5 sigmas en un test simple, lo cual parece fuerte. Pero si hay correlacion entre transiciones de una misma cadena (y la hay: bloques consecutivos de la misma orbita no son independientes), el error estandar efectivo puede ser 2-3x mayor, y la significancia cae a 2-3 sigmas. El modelo genera cadenas independientes, pero las cadenas reales no lo son. Un test que tenga en cuenta esta agrupacion (cluster-robust SE, o permutacion a nivel de cadena, no de transicion) podria cambiar el resultado.

**Escenarios posibles:**

- **Senal real modular (probabilidad estimada: 20%).** Hay una congruencia fina que hace que despues de `exit_v2 = 5`, el siguiente impar caiga en clases mod `2^k` que favorecen `tail = 1`. Esto seria verificable algebraicamente y constituiria un lemma local.

- **Mezcla de subpoblaciones / Simpson (probabilidad estimada: 35%).** Dentro de `prev_exit_v2 = 5` + `interior`, hay mezcla de cadenas con margenes/profundidades distintas que individualmente no muestran sesgo pero que en conjunto crean una diferencia artificial. La descomposicion por margen y profundidad podria revelar esto, pero primero hay que verificar que la senal es real.

- **Artefacto estadistico post-hoc + muestra pequena (probabilidad estimada: 35%).** La combinacion de comparaciones multiples no corregidas, anchoring en `exit_v2 = 5`, y muestra de ~3400 con posible correlacion intra-cadena produce una senal que no sobreviviria un test riguroso.

- **Correlacion ya conocida (probabilidad estimada: 10%).** La dependencia entre bloques consecutivos condicionada por supervivencia podria ser un caso particular de resultados existentes sobre cadenas condicionadas de random walks (ballot problem, Bertrand ballot theorem, o modelos de Markov con absorcion). Wirsching (1998) y Lagarias-Soundararajan (2006) estudian la funcion de iteracion 3x+1 como mapa en los 2-adicos, y la estructura de `exit_v2` esta directamente relacionada con la expansion 2-adica del iterado. Si `exit_v2 = 5` fija los ultimos 5 bits del cociente, el siguiente `tail = v2(next_odd + 1)` depende de la estructura binaria del siguiente impar, que esta parcialmente determinada por esos bits. Esto podria ser un efecto algebraico trivial que ya esta implicito en la congruencia `3^s q equiv 33 mod 64`.

## Conexiones con literatura conocida

- **Terras (1976) y modelo probabilistico:** El modelo independiente con `tail ~ Geom(1/2)` es esencialmente el modelo de Terras/Wagstaff. La validacion global en M13 confirma que este modelo funciona bien incondicionalmente, como la literatura ya sugiere. La novedad potencial esta en la *falla condicionada*, no en el exito global.

- **Tao (2019), Theorem 1.2:** Casi toda orbita (en densidad logaritmica) baja eventualmente debajo de cualquier `f(n) -> inf`. Esto implica que las cadenas que sobreviven muchos bloques sin descender son un conjunto de densidad cada vez menor. El condicionamiento por supervivencia en M13 selecciona este conjunto raro, lo cual puede amplificar artefactos estadisticos y correlaciones que no existen en la poblacion general.

- **Wirsching (1998), "The Dynamical System Generated by the 3n+1 Function":** Estudia la iteracion como mapa en Z_2 (enteros 2-adicos). La valuacion `v2` es central en este framework. La congruencia `3^s q equiv 33 mod 64` para `exit_v2 = 5` es un statement directo sobre los primeros bits de la expansion 2-adica. El siguiente `tail = v2(next_odd + 1)` depende de los bits bajos del siguiente impar, que estan parcialmente fijados por la congruencia de salida. Un calculo modular directo podria resolver si la dependencia observada es una consecuencia algebraica de esta relacion.

- **Monks (2006) y vectores de paridad suficientes:** Monks estudio que vectores de paridad son "suficientes" para determinar el comportamiento de orbitas en ciertas clases. La relacion entre `prev_exit_v2` y `next_tail` es esencialmente una pregunta sobre la correlacion entre componentes consecutivas del vector de paridad, condicionada por supervivencia.

- **Ballot problem y random walks condicionados:** Condicionar una cadena odd-to-odd por "no descender" es formalmente analogo a condicionar un random walk por permanecer positivo (puente de Dyck, excursion de Browniano, ballot problem de Bertrand). En random walks condicionados, las transiciones consecutivas *si* muestran dependencia, incluso si las transiciones originales son independientes. Es posible que el residuo observado sea simplemente el efecto de este condicionamiento, mal capturado porque el modelo independiente genera cadenas completas y luego filtra, pero no captura correctamente las correlaciones inducidas por el filtrado cuando se mira una subpoblacion especifica.

## Preguntas para Codex orquestador

1. **Cuantos subgrupos distintos se testearon en M13?** Necesito un numero exacto (o una cota) para evaluar si la celda `prev_exit_v2 = 5` + `interior_block` sobrevive correccion por comparaciones multiples. Un conteo rapido de las filas en todos los CSV de salida daria esta cifra. *Clasificacion: revision metodologica.*

2. **Las transiciones dentro de una misma cadena se trataron como independientes al calcular los intervalos de confianza?** Si dos bloques interiores vienen de la misma orbita (mismo `n` inicial), no son independientes. El IC95 reportado asume independencia entre filas? Si es asi, esta subestimado. Un test robusto deberia clusterizar por cadena o usar permutacion a nivel de cadena. *Clasificacion: revision metodologica.*

3. **Se verifico la congruencia algebraica directa?** Si `exit_v2 = 5` implica `3^s q equiv 33 mod 64`, el siguiente impar es `(3^s q - 1) / 32`, y su estructura mod `2^k` esta determinada por `3^s q mod 2^{5+k}`. Para `tail = 1` del siguiente bloque, necesitamos `v2(next_odd + 1) = 1`, es decir `next_odd equiv 1 mod 2` pero `next_odd not equiv 3 mod 4`. Esto es una condicion modular sobre `3^s q mod 128`. Se hizo este calculo? Si la fraccion teorica de `tail = 1` dada la congruencia coincide con 0.4527, tenemos una explicacion algebraica cerrada y M14 se resuelve sin mas experimentos. *Clasificacion: lemma candidato.*
