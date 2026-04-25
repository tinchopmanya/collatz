# Prompts M15 Ronda 2

Fecha: 2026-04-25
Milestone: M15
Decision actual: despues de InvestigadorWeb y ClaudeSocio, la proxima compuerta es calcular memoria modular `q mod 8` entre bloques consecutivos.

## Mapa de dependencias

```text
CodexInvestigadorWeb: completado
ClaudeSocioCritico: completado
Orquestador: decision completada
  -> CodexHijo1 calcula transicion q mod 8
      -> CodexHijo2 replica/falsifica
          -> Orquestador decide si M15 sigue a train/holdout o se descarta
```

Para esta ronda:

- Prompt 1 es bloqueante y puede empezar ahora.
- Prompt 2 es bloqueante, pero no debe empezar hasta que termine Prompt 1.

## Prompt 1 - CodexHijo1 transicion `q mod 8`

Agente: CodexHijo1_PrincipalEjecutor
Objetivo: calcular la matriz de transicion `q_{i+1} mod 8 | q_i mod 8` bajo el mapa odd-to-odd del proyecto y decidir si hay memoria modular suficiente para justificar M15.
Bloqueante: si
Puede empezar ahora: si
Depende de: InvestigadorWeb integrado, ClaudeSocio integrado, decision del orquestador en `DecisionM15TrasClaudeSocio.md`
Desbloquea a: CodexHijo2_ReplicaYFalsacion
Rama sugerida: `codex-hijo/m15-qmod8-transition`
Archivos permitidos:
- `experiments/analyze_m15_qmod8_transition.py`
- `reports/m15_qmod8_transition*.csv`
- `colaboradores/codex-hijo/ResultadosM15QMod8Transition.md`
Archivos prohibidos:
- `MILESTONES.md`
- `colaboradores/orquestador/`
- `colaboradores/claude-socio/`
- `colaboradores/investigador-web/`
- holdout fresco `15000001..25000000`
Git: crear rama propia desde `main`, commit y push. No tocar `main`.
Salida esperada: script reproducible, CSV liviano, reporte con matriz, autovalores/mezcla y recomendacion.

Prompt para pegar:

```text
Actuas como CodexHijo1_PrincipalEjecutor del proyecto Collatz.

Tu tarea es pequena pero bloqueante: calcular la matriz de transicion `q_{i+1} mod 8 | q_i mod 8` bajo el mapa odd-to-odd usado por el proyecto. No corras holdout fresco y no implementes aun la comparacion completa de supervivencia.

Contexto minimo:
- M15 investiga si el feature modular `q mod 8` aporta prediccion sobre supervivencia orbital.
- Ya sabemos que `q mod 8` predice `next_tail`; eso es algebra local conocida.
- ClaudeSocioCritico indico que lo no trivial es si esa informacion tiene memoria entre bloques consecutivos.
- Si la matriz de transicion mezcla rapido hacia uniforme, M15 se puede descartar en frio.
- Si mezcla lento, M15 merece un experimento train/holdout posterior.

Debes leer antes de tocar codigo:
1. `MILESTONES.md`
2. `colaboradores/orquestador/DecisionM15TrasClaudeSocio.md`
3. `colaboradores/claude-socio/RevisionM15ModeloModular.md`
4. `colaboradores/codex-hijo/ResultadosM15Algebra.md`
5. `colaboradores/codex-hijo/ReplicaM15Algebra.md`
6. scripts existentes en `experiments/` que definan bloques odd-to-odd, `tail`, `exit_v2` o `q`

Definicion operativa inicial:
- Para un impar actual `n_i`, usar la convencion del proyecto si ya existe.
- Si no existe una convencion unica, documenta explicitamente una:
  - `s_i = v2(n_i + 1)`
  - `q_i = (n_i + 1) / 2^s_i`
  - bloque alternante hasta `3^s_i * q_i - 1`
  - `exit_v2_i = v2(3^s_i * q_i - 1)`
  - `n_{i+1} = (3^s_i * q_i - 1) / 2^exit_v2_i`
  - luego calcular `q_{i+1}` con la misma definicion sobre `n_{i+1}`

Trabajo requerido:
1. Crear `experiments/analyze_m15_qmod8_transition.py`.
2. Calcular transiciones para un rango exploratorio NO holdout, por defecto `n <= 5000000`, solo impares.
3. Producir una matriz 4x4 para residuos impares `1,3,5,7 mod 8`.
4. Reportar probabilidades por fila, conteos, distribucion estacionaria estimada y autovalores o una medida simple de mezcla.
5. Si puedes derivar parte algebraica exacta sin complicar demasiado, incluyela; si no, deja claro que es empirico exploratorio.
6. No abras `q mod 16`, no optimices de mas, no mires holdout `15000001..25000000`.

Criterio de interpretacion:
- Si cada fila esta cerca de uniforme y la memoria desaparece en 2-3 pasos, recomienda enfriar/descartar M15 antes de holdout.
- Si hay filas muy no uniformes o autovalor subdominante alto, recomienda que el orquestador disene experimento confirmatorio.

Git:
- Trabaja desde `main` actualizado.
- Crea rama `codex-hijo/m15-qmod8-transition`.
- Solo puedes crear/modificar:
  - `experiments/analyze_m15_qmod8_transition.py`
  - `reports/m15_qmod8_transition*.csv`
  - `colaboradores/codex-hijo/ResultadosM15QMod8Transition.md`
- Haz commit y push de tu rama.
- No toques `main`, `MILESTONES.md`, ni carpetas de orquestador/Claude/investigador.

Entrega final:
- Rama:
- Commit:
- Comando reproducible:
- Archivos creados:
- Matriz de transicion:
- Medida de mezcla/autovalores:
- Recomendacion: descartar/enfriar M15 o seguir.
- Que no deberiamos concluir:
```

## Prompt 2 - CodexHijo2 replica/falsacion

Agente: CodexHijo2_ReplicaYFalsacion
Objetivo: replicar o falsificar la matriz de transicion de CodexHijo1.
Bloqueante: si
Puede empezar ahora: no
Depende de: Prompt 1 terminado
Desbloquea a: decision del orquestador
Rama sugerida: `codex-hijo/m15-qmod8-transition-replica`
Archivos permitidos:
- `experiments/replicate_m15_qmod8_transition.py`
- `reports/m15_qmod8_transition_replica*.csv`
- `colaboradores/codex-hijo/ReplicaM15QMod8Transition.md`
Archivos prohibidos:
- copiar literalmente el script de CodexHijo1;
- `MILESTONES.md`;
- `colaboradores/orquestador/`;
- holdout fresco.
Git: rama propia desde `main`, commit y push. No tocar `main`.
Salida esperada: replica independiente o falsacion.

Estado: no lanzar todavia.
