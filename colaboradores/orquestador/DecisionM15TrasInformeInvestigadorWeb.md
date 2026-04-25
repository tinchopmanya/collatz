# Decision M15 tras informe de CodexInvestigadorWeb

Fecha: 2026-04-25
Milestone: M15
Entrada principal: `colaboradores/investigador-web/InformeM15ModeloModularLiteratura.md`
Commit integrado: `5699058`

## Preguntas antes de decidir

- Estamos en algo potencialmente virgen?
  - No como matematica local. El condicionamiento por residuos modulo potencias de 2 y parity vectors es conocido desde Terras/Everett/Lagarias y aparece en la teoria 2-adica de Collatz.
- Alguien ya hizo esto?
  - La maquinaria general si. La comparacion exacta `P(next_tail | q mod 8)` vs geometrico independiente para predecir supervivencia/stopping/blocks_to_descend no fue encontrada por el InvestigadorWeb.
- Que seria nuevo si sale bien?
  - No seria "descubrimos una ley local nueva". Seria una ablation predictiva concreta: mostrar que un feature modular muy barato mejora out-of-sample la prediccion de supervivencia orbital frente a un baseline geometrico justo.
- Que resultado destruiria la hipotesis?
  - Que el modelo modular no mejore out-of-sample, o que mejore solo por condicionamiento tautologico/post-hoc, o que un baseline geometrico correctamente condicionado iguale la mejora.
- Que tan lejos estamos de algo publicable?
  - Lejos de un resultado matematico fuerte. Cerca de una nota interna rigurosa si el experimento queda bien preregistrado y replicado.
- Esta decision necesita web, algebra, experimento o revision critica?
  - Web ya completada para esta compuerta. Ahora necesita critica independiente de ClaudeSocio antes de activar ejecucion.

## Sintesis del informe web

El fenomeno local es conocido/implicito:

- parity vectors / parity sequences;
- clases modulo `2^k`;
- accelerated map / Syracuse map / odd-to-odd map;
- valuaciones `ord_2(3n+1)`;
- modelos geometricos y estocasticos para stopping time.

No se encontro la comparacion exacta de M15:

- usar `q mod 8` como feature modular finito;
- comparar contra un modelo geometrico independiente;
- medir mejora en supervivencia orbital, stopping time o `blocks_to_descend`.

Nivel de novedad adoptado:

- Nivel 1-2 como matematica local: conocido o implicito.
- Nivel 3 posible como formulacion experimental interna si el diseno es limpio.
- No subir a Nivel 4 sin resultado out-of-sample y revision critica.

## Decision

M15 sigue vivo, pero reformulado como experimento de validacion predictiva, no como busqueda de un lemma local nuevo.

No se activa todavia CodexHijo1 para implementar.

Siguiente paso bloqueante:

- ClaudeSocioCritico debe auditar si la pregunta M15 es valida, tautologica, mal condicionada o demasiado debil.

## Estado de agentes

- CodexInvestigadorWeb: completado e integrado.
- ClaudeSocioCritico: desbloqueado; debe correr ahora.
- CodexHijo1: bloqueado hasta revision de ClaudeSocio y decision del orquestador.
- CodexHijo2: bloqueado hasta que exista trabajo de CodexHijo1 para replicar/falsar.

## Preguntas despues

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos en delimitacion: sabemos que no debemos vender novedad matematica local, pero hay una pregunta experimental no encontrada exactamente.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Mas debil como novedad teorica; todavia razonable como ablation predictiva.
- Hay riesgo post-hoc?
  - Si. Por eso falta preregistro y holdout fresco antes de cualquier corrida confirmatoria.
- Hay explicacion algebraica trivial?
  - Si para `q mod 8 -> next_tail`. No para la utilidad predictiva sobre supervivencia orbital.
- Hay replica independiente?
  - Para la algebra si. Para la utilidad predictiva todavia no.
- Que toca ahora?
  - Lanzar ClaudeSocioCritico con el Prompt 2 de `PromptsM15Ronda1.md`.
