# Decision M19 - busqueda de posibilidad cientifica fuerte

Fecha: 2026-04-27
Responsable: Codex orquestador
Estado: busqueda completada; reapertura condicionada

## Preguntas antes

- Estamos en algo potencialmente virgen?
  - No dentro del arco estadistico odd-to-odd. Ese camino quedo cerrado en M18.
  - Si hay potencial alto, esta fuera de esa linea: formalizacion, reescritura, ciclos o teoria 2-adica.
- Alguien ya hizo esto?
  - Si. Hay literatura activa y reciente en verificacion computacional, rewriting, formalizacion y ciclos.
- Que seria nuevo si sale bien?
  - No "probar Collatz" directamente. Un resultado fuerte realista seria: reproducir y extender una prueba automatica de un debilitamiento no trivial, o formalizar/auditar un resultado reconocido de la literatura.
- Que resultado destruiria la hipotesis?
  - Que la direccion elegida solo reproduzca claims existentes sin extension, o que requiera herramientas teoricas fuera del alcance del repo.
- Que tan lejos estamos de algo publicable?
  - Lejos de una prueba. Pero una contribucion formal/reproducible podria llegar a nivel 3-4 si es nueva y verificable.
- Hay riesgo post-hoc?
  - Alto. El cierre M18 crea tentacion de inventar una nueva pista por inercia. Por eso M19 solo evalua puertas de entrada de alto ceiling.

## Fuentes revisadas

1. Collatz Conjecture Challenge
   - URL: https://ccchallenge.org/
   - Relevancia: proyecto activo para formalizar literatura de Collatz. Lista resultados como Tao2022 y Eliahou1993; Eliahou1993 aparece como "Ready to be audited".

2. Yolcu, Aaronson, Heule - Mixed Base Rewriting for the Collatz Conjecture
   - Paper: https://www.cs.cmu.edu/~mheule/publications/WST21.pdf
   - Codigo: https://github.com/emreyolcu/rewriting-collatz
   - Relevancia: transforma Collatz y variantes en problemas de terminacion de sistemas de reescritura; usa interpretaciones matriciales/arctic/tropical y SAT. No prueba Collatz, pero automatiza pruebas de debilitamientos no triviales.

3. Angeltveit - An improved algorithm for checking the Collatz conjecture for all n < 2^N
   - URL: https://arxiv.org/abs/2602.10466
   - Relevancia: algoritmo reciente de verificacion computacional. Buen engineering, pero no cambia el problema teorico central.

4. Knight - Collatz high cycles do not exist
   - DOI: https://doi.org/10.1016/j.disc.2025.114812
   - Relevancia: resultado teorico reciente sobre ciclos racionales/high cycles. Alto ceiling teorico, pero entrada computacional limitada.

5. Near-conjugacy log_6
   - URL: https://arxiv.org/abs/2601.04289
   - Relevancia: ya fue auditado en M18; no aporta una via fuerte para este repo.

## Evaluacion de direcciones

### A - Continuar estadistica odd-to-odd

Veredicto: no.

- Ceiling: 2.5.
- Probabilidad de resultado nuevo fuerte: baja.
- Razon: M12-M18 agotaron esta linea. El modelo geometrico i.i.d. es suficiente para n > 2.5M en nuestras metricas.

### B - Verificacion computacional mas alta

Veredicto: no como prioridad.

- Ceiling: 2-3.
- Probabilidad de aporte reproducible: media.
- Razon: Angeltveit 2026 ya trabaja exactamente en mejorar verificacion para `n < 2^N`. Competir ahi requiere optimizacion de bajo nivel, no la infraestructura actual.

### C - Formalizacion Lean / Collatz Challenge

Veredicto: fuerte pero no inmediata.

- Ceiling: 3-4.
- Probabilidad de aporte util: media.
- Bloqueo: Lean/Lake no estan instalados localmente.
- Valor realista: formalizar/auditar un resultado conocido, por ejemplo Eliahou1993 o una lemma de parity vectors.
- Riesgo: alto costo de onboarding; no produce una idea nueva sobre Collatz, pero si un artefacto matematico serio.

### D - Ciclos/high cycles

Veredicto: teoricamente fuerte, entrada computacional debil.

- Ceiling: 4.
- Probabilidad con este repo: baja.
- Razon: Knight 2026 es un resultado teorico reciente; extenderlo requiere teoria de Christoffel words/parity vectors, no solo experimentos.

### E - Mixed-base rewriting / SAT termination

Veredicto: mejor candidato para reabrir con posibilidad alta relativa.

- Ceiling: 3.5-4.
- Probabilidad de aporte local: media-baja, pero mayor que otras lineas de alto ceiling.
- Encaje con repo: bueno. Es codigo, pruebas automaticas y sistemas de reescritura.
- Evidencia de factibilidad: el repo `rewriting-collatz` existe y contiene prover, reglas, pruebas y logs.
- Bloqueos actuales: faltan dependencias locales (`numpy`; probablemente solver SAT tipo CaDiCaL/Kissat).

## Decision

Reabrir solo de forma condicionada con una nueva linea:

```text
M19 - Auditoria y reproduccion de mixed-base rewriting para Collatz
```

No se reabre el arco estadistico.
No se busca una prueba directa.
No se hacen claims de novedad.

La hipotesis de trabajo no es "vamos a probar Collatz", sino:

```text
Podemos reproducir, auditar y quizas extender pruebas automaticas de debilitamientos no triviales del problema usando rewriting/SAT?
```

## Criterio de exito de M19

M19 tiene exito si logra al menos uno:

- reproducir localmente una prueba del repo `rewriting-collatz`;
- documentar exactamente que dependencias y parametros se requieren;
- verificar una prueba existente de un debilitamiento no trivial;
- encontrar una extension pequena y nueva: por ejemplo, una clase residual/debilitamiento no listada en los logs existentes con prueba automatica reproducible.

## Criterio de abandono de M19

Abandonar si:

- no se puede reproducir ninguna prueba base por dependencias o incompatibilidades;
- todo lo reproducido es identico al repo original sin mejora ni auditoria;
- extender requiere busqueda SAT grande sin principio de parada;
- aparecen claims de prueba global no verificables.

## Preguntas despues

- Avanzamos o solo confirmamos algo conocido?
  - Avanzamos en seleccionar una unica puerta de alto ceiling. Todavia no hay resultado nuevo.
- La hipotesis quedo mas fuerte, mas debil o descartada?
  - Se descarta continuar estadistica; se abre condicionalmente rewriting/SAT.
- Hay riesgo post-hoc?
  - Si. La mitigacion es reproducir primero, extender despues.
- Hay explicacion algebraica trivial?
  - No para rewriting/SAT. Si aparece una "near-conjugacy" o transformacion logaritmica, debe auditarse como en M18.
- Hay evidencia independiente?
  - Si: paper Yolcu-Aaronson-Heule y codigo publico.
- Que toca ahora?
  - M19 paso 1: preparar entorno minimo y reproducir una prueba existente, sin modificar claims cientificos.
