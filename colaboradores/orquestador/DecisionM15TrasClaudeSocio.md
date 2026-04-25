# Decision M15 tras revision de ClaudeSocioCritico

Fecha: 2026-04-25
Milestone: M15
Entrada principal: `colaboradores/claude-socio/RevisionM15ModeloModular.md`
Commit integrado: `fbd812e`

## Preguntas antes de decidir

- Estamos en algo potencialmente virgen?
  - No como algebra local. Si queda algo interesante, estaria en la propagacion de informacion modular a metricas de cadena.
- Alguien ya hizo esto?
  - El InvestigadorWeb no encontro la ablation exacta. ClaudeSocio confirma que el mecanismo local es conocido y que la unica pregunta no trivial es propagacion a cadena.
- Que seria realmente nuevo si sale bien?
  - Una formulacion experimental limpia de cuanta memoria modular `q mod 8` afecta `blocks_to_descend` o supervivencia, no una identidad de bloque.
- Que resultado destruiria la hipotesis?
  - Que la matriz `q_{i+1} mod 8 | q_i mod 8` mezcle rapido a uniforme, o que la mejora solo exista para predecir `next_tail` local.
- Que tan lejos estamos de algo publicable?
  - Todavia lejos. Primero necesitamos saber si hay memoria modular suficiente para justificar experimento.
- Esta decision necesita web, algebra, experimento o revision critica?
  - Web y critica ya pasaron. Ahora necesita algebra/computo pequeno, sin holdout.

## Sintesis de ClaudeSocio

Veredicto: aprobar con cambios.

Punto clave:

- Medir si `q mod 8` predice `next_tail` mejor que geometrico es tautologico.
- La pregunta real es si esa ventaja local se propaga a metricas de cadena completa.
- Antes de usar holdout, hay que calcular la matriz de transicion `q_{i+1} mod 8 | q_i mod 8`.

Criterio propuesto:

- Si la matriz mezcla rapido hacia uniforme, M15 se descarta en frio.
- Si la matriz tiene memoria lenta, entonces vale la pena diseñar experimento train/holdout sobre cadenas completas.

## Decision

Acepto la critica de ClaudeSocio.

No se corre holdout.
No se implementa todavia comparacion de supervivencia.
No se abre `q mod 16`.

Siguiente tarea:

- Activar CodexHijo1 para calcular y reportar la matriz de transicion `q_{i+1} mod 8 | q_i mod 8` bajo el mapa odd-to-odd usado por el proyecto.

Estado de agentes:

- CodexInvestigadorWeb: completado e integrado.
- ClaudeSocioCritico: completado, rama pusheada e integrado.
- CodexHijo1: desbloqueado para M15 Ronda 2.
- CodexHijo2: bloqueado hasta tener resultado de CodexHijo1 para replicar/falsar.

## Criterio de exito para la Ronda 2

La tarea de CodexHijo1 tiene exito si entrega:

- definicion exacta de estado `q mod 8`;
- matriz de transicion estimada o derivada;
- explicacion de si la matriz depende de variables ocultas como `tail`, `exit_v2` o distribucion de estados;
- autovalores o medida simple de mezcla;
- conclusion: M15 sigue vivo o se enfria.

## Criterio de abandono

Abandonar M15 como experimento modular si:

- la transicion marginal desde `q_i mod 8` a `q_{i+1} mod 8` es uniforme o casi uniforme;
- la informacion modular desaparece en 2-3 pasos;
- la unica mejora demostrable es prediccion local de `next_tail`;
- avanzar requiere abrir muchos modulos/residuos sin principio de parada.

## Preguntas despues

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos: ClaudeSocio nos evito un holdout tautologico y transformo M15 en una pregunta de memoria modular.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Mas estricta. No descartada, pero ahora debe pasar una prueba de mezcla antes de gastar holdout.
- Hay riesgo post-hoc?
  - Menor si nos limitamos a `q mod 8` y preregistramos el criterio antes del calculo.
- Hay explicacion algebraica trivial?
  - Si para `next_tail`. Todavia no sabemos para la transicion entre estados.
- Hay replica independiente?
  - No para la matriz de transicion. CodexHijo2 se activara despues.
- Que toca ahora?
  - Lanzar CodexHijo1 con `PromptsM15Ronda2.md`.
