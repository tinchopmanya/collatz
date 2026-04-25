# Prompts M15 Ronda 1

Fecha: 2026-04-25
Milestone: M15
Decision actual: antes de diseñar el experimento modular, necesitamos estado del arte y critica independiente.

## Mapa de dependencias

```text
CodexInvestigadorWeb
  -> ClaudeSocioCritico
      -> Codex Papa Orquestador decide
          -> CodexHijo1 ejecuta diseno o experimento
              -> CodexHijo2 replica/falsifica
```

Para esta ronda:

- Prompt 1 esta completado e integrado en `main`.
- Prompt 2 es bloqueante y puede empezar ahora.
- Prompt 3 esta bloqueado por Prompt 1 + Prompt 2 + decision del orquestador.
- Prompt 4 esta bloqueado por Prompt 3.

## Prompt 1 - CodexInvestigadorWeb

Agente: CodexInvestigadorWeb
Objetivo: investigar literatura sobre si ya existe una comparacion modular tipo `q mod 8` contra modelo geometrico/aleatorio para supervivencia orbital, stopping time o cadenas odd-to-odd en Collatz.
Bloqueante: si
Puede empezar ahora: completado
Depende de: nadie
Desbloquea a: ClaudeSocioCritico y decision del orquestador
Rama sugerida: `codex-investigador/m15-modelo-modular-literatura`
Archivos permitidos: `colaboradores/investigador-web/InformeM15ModeloModularLiteratura.md`
Archivos prohibidos: `MILESTONES.md`, `experiments/`, `src/`, `reports/`, cualquier archivo de otros colaboradores
Git: crear rama propia desde `main`, escribir informe, commit y push. No tocar `main`.
Salida esperada: informe con fuentes primarias, links, fechas, nombres tecnicos, nivel de novedad y recomendacion.

Prompt para pegar:

```text
Actuas como CodexInvestigadorWeb dentro del proyecto Collatz.

Tu unica tarea es investigar literatura web/papers. No implementes codigo, no corras experimentos y no decidas la direccion final.

Contexto del proyecto:
- Estamos en M15.
- Ya se verifico algebraicamente que `q mod 4` coincide con la geometrica, pero `q mod 8` predice `next_tail`.
- Valores replicados: `q=1 mod 8 -> P(next_tail=1)=5/6`, `q=3 -> 2/3`, `q=5 -> 1/6`, `q=7 -> 1/3`.
- Claude ya indico que esto es esperable por dinamica 2-adica, no un resultado fuerte por si solo.
- La pregunta real es si un modelo modular `P(next_tail | q mod 8)` mejora la prediccion de supervivencia orbital / stopping time / blocks_to_descend frente al modelo geometrico independiente.

Preguntas que debes responder:
1. ¿Esta comparacion entre modelos modulares 2-adicos y modelos geometricos/aleatorios ya existe en la literatura de Collatz?
2. ¿Aparece especificamente algo equivalente a condicionar por `q mod 8`, residuos modulo potencias de 2, parity vectors, stopping time o cadenas odd-to-odd?
3. ¿Quienes lo hicieron, cuando, y con que nombres tecnicos?
4. ¿Esto esta en Terras, Everett, Wirsching, Lagarias, Tao, Oliveira e Silva, Krasikov, Applegate/Lagarias u otros?
5. ¿La idea M15 parece conocida, implicita, reformulacion util, o potencialmente nueva como experimento?

Fuentes:
- Prioriza papers, libros, surveys y arXiv.
- Usa fuentes primarias cuando existan.
- Incluye links.
- No exageres novedad: si no encuentras algo, di "no encontrado", no "nuevo".

Git:
- Trabaja desde `main` actualizado.
- Crea la rama `codex-investigador/m15-modelo-modular-literatura`.
- Escribe solo `colaboradores/investigador-web/InformeM15ModeloModularLiteratura.md`.
- Usa la plantilla `colaboradores/investigador-web/PlantillaInformeInvestigadorWeb.md`.
- Haz commit y push de tu rama.
- No toques `main`, `MILESTONES.md`, `experiments/`, `src/` ni `reports/`.

Entrega final:
- Rama.
- Commit.
- Fuentes principales.
- Respuesta corta: conocido / implicito / no encontrado.
- Nivel de novedad estimado.
- Recomendacion para el orquestador.
```

## Prompt 2 - ClaudeSocioCritico

Agente: ClaudeSocioCritico
Objetivo: auditar la idea M15 despues de leer el informe de CodexInvestigadorWeb.
Bloqueante: si
Puede empezar ahora: si
Depende de: Prompt 1 terminado
Desbloquea a: decision del orquestador
Rama sugerida: `claude-socio/m15-critica-modelo-modular`
Archivos permitidos: `colaboradores/claude-socio/RevisionM15ModeloModular.md`
Archivos prohibidos: `MILESTONES.md`, `experiments/`, `src/`, `reports/`, archivos de otros colaboradores
Git: si escribe archivo en repo, usar rama propia, commit y push. Si responde solo en chat, no hace git.
Salida esperada: veredicto critico sobre si M15 debe avanzar, reformularse o descartarse.

Prompt para pegar despues de tener Prompt 1:

```text
Actuas como ClaudeSocioCritico del proyecto Collatz.

No eres subordinado del orquestador. Tu trabajo es criticar, auditar y proponer alternativas. No implementes codigo.

Debes leer:
- `MILESTONES.md`
- `colaboradores/orquestador/DecisionM15TrasAlgebraReplicaYClaude.md`
- `colaboradores/orquestador/ArquitecturaTrabajoMultiagenteCollatz.md`
- `colaboradores/investigador-web/InformeM15ModeloModularLiteratura.md`
- si existen, los reportes de Codex hijo sobre M15 algebra.

Pregunta a auditar:
Queremos saber si vale la pena diseñar un experimento M15 donde un modelo modular `P(next_tail | q mod 8)` compita contra el modelo geometrico independiente para predecir supervivencia orbital / `blocks_to_descend` / stopping time.

Audita:
1. ¿La pregunta es cientificamente valida o tautologica?
2. ¿El informe web sugiere que esto ya esta resuelto?
3. ¿Que seria un resultado no trivial?
4. ¿Que resultado destruiria la hipotesis?
5. ¿Como evitar contaminacion train/holdout?
6. ¿Cual debe ser el criterio de exito y abandono?
7. ¿Conviene activar CodexHijo1 o descartar/reformular primero?

Git:
- Si vas a escribir archivo, crea rama `claude-socio/m15-critica-modelo-modular`.
- Escribe solo `colaboradores/claude-socio/RevisionM15ModeloModular.md`.
- Usa la plantilla `colaboradores/claude-socio/PlantillaRevisionCritica.md`.
- Haz commit y push de tu rama.
- No toques `main`, `MILESTONES.md`, `experiments/`, `src/` ni `reports/`.

Entrega final:
- Veredicto: aprobar / aprobar con cambios / rechazar / pedir mas evidencia.
- Riesgo principal.
- Recomendacion concreta al orquestador.
- Si aplica: rama y commit.
```

## Prompt 3 - CodexHijo1_PrincipalEjecutor

Agente: CodexHijo1_PrincipalEjecutor
Objetivo: diseñar o implementar el experimento M15 solo despues de decision del orquestador.
Bloqueante: no para la investigacion web, si para la ejecucion experimental.
Puede empezar ahora: no
Depende de: Prompt 1 + Prompt 2 + decision escrita del orquestador
Desbloquea a: CodexHijo2
Rama sugerida: se definira despues de la decision
Archivos permitidos: se definiran despues de la decision
Archivos prohibidos: holdout fresco hasta que este pre-registrado
Git: rama propia, commit y push; no tocar `main`
Salida esperada: script/reporte reproducible o diseño experimental, segun decision futura.

Estado: no lanzar todavia.

## Prompt 4 - CodexHijo2_ReplicaYFalsacion

Agente: CodexHijo2_ReplicaYFalsacion
Objetivo: replicar o falsificar lo que produzca CodexHijo1.
Bloqueante: no para decidir si diseñar M15; si para aceptar resultados de ejecucion.
Puede empezar ahora: no
Depende de: Prompt 3 terminado
Desbloquea a: integracion final del orquestador
Rama sugerida: se definira despues de Prompt 3
Archivos permitidos: se definiran despues de Prompt 3
Archivos prohibidos: copiar literalmente el script de CodexHijo1 sin replica conceptual
Git: rama propia, commit y push; no tocar `main`
Salida esperada: replica independiente, falsacion o reporte de discrepancias.

Estado: no lanzar todavia.
