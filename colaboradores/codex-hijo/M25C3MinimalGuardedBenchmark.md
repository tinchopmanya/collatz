# M25 C3 minimal guarded benchmark

Fecha: 2026-04-29
Agente: CodexHijo-M25-C3-MinimalGuardedBenchmark
Worktree: `C:\dev\vert\collatz-m25-c3-minimal-guarded-benchmark`
Rama: `codex-hijo/m25-c3-minimal-guarded-benchmark`

## Veredicto

Se construyo el primer artefacto minimo de M25 para la microguarda M24
`r mod 2^13 = 8189`, pero **no** se genero un SRS guardado.

El checker de implicacion pasa para los hechos finitos auditables:

```text
m25_c3_minimal_guarded_benchmark=PASS
c3_build_status=blocked
c3_blocked_reason=guarded_srs_semantics_missing
accepted_count=8
certified_overlap_count=0
dynamic_rule=bad -> d
```

El estado `blocked` es intencional: sin una definicion local de como se propaga
el estado de residuo por las reglas auxiliares, la orientacion de bits y el
contexto de aplicacion, emitir reglas SRS concretas seria un claim semantico no
justificado.

No se corrio Matchbox, AProVE ni ningun prover de terminacion. No hay claim de
terminacion ni claim de Collatz.

## Entradas leidas

Se usaron como base los artefactos indicados para la tarea:

```text
colaboradores/codex-hijo/M24SRSSemanticAudit.md
colaboradores/codex-hijo/M24MicroGuardDesign.md
scripts/m19_generate_rewriting_challenges.py
reports/m19_rewriting_challenges/*
scripts/m24_microguard_design.py
```

Tambien se reutilizo el auditor ejecutable de M24:

```text
scripts/m24_srs_semantic_audit.py
```

## Artefactos M25

Archivos agregados:

```text
scripts/m25_c3_minimal_guarded_benchmark.py
tests/test_m25_c3_minimal_guarded_benchmark.py
reports/m25_c3_minimal_guarded_benchmark.metadata.txt
reports/m25_c3_minimal_guarded_benchmark_summary.csv
reports/m25_c3_minimal_guarded_benchmark_violations.csv
colaboradores/codex-hijo/M25C3MinimalGuardedBenchmark.md
```

El formato textual es `m25.c3-minimal-guarded-benchmark.v1`.

`reports/m25_c3_minimal_guarded_benchmark.metadata.txt` documenta:

```text
c3_build_status: blocked
emits_srs: false
prover_calls: none
exact_subset_statement: G_8189 = U_16 intersection {r | r mod 2^13 = 8189}
ascii_rule: bad -> d
paper_rule: tf* -> *
branch_condition: n mod 8 = 5
insertion_point_status: conceptual_anchor_only_not_materialized
```

`reports/m25_c3_minimal_guarded_benchmark_violations.csv` queda solo con header
si todos los checks pasan.

## Checks de implicacion

El checker recalcula la microguarda y valida:

```text
G_8189 = {8189, 16381, 24573, 32765, 40957, 49149, 57341, 65533}
G_8189 = U_16 intersection {r | r mod 2^13 = 8189}
G_8189 intersection C_16 = empty
forall r in G_8189: r mod 8 = 5
```

Tambien audita la rama dinamica local:

```text
S_full contiene bad -> d
S2_without_tf_end_to_end elimina solo bad -> d
bad -> d corresponde a tf* -> *
tf* -> * corresponde a n mod 8 = 5
```

Hashes congelados reportados:

```text
accepted_residues_sha256 = de4100dcb707ee6d42acf0fc6af8b8bb8d2a70852b1a2af461d64e4926eb281c
frozen_uncovered_sha256 = bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210
certified_set_sha256_checked_not_embedded = 0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa
```

## Punto de insercion documentado

El ancla conceptual de guardado es la regla dinamica:

```text
bad -> d
```

La guarda se insertaria sobre esa contraccion dinamica, despues de que la palabra
S en alfabeto mixto expone el lhs `bad` y antes de contraerlo a `d`.

No se materializa esa regla en SRS porque falta especificar, de forma local y
testeable:

```text
residue-state threading through auxiliary rules
bit orientation
context handling around the guarded dynamic contraction
```

Por eso el artefacto M25 es metadata/checker y no benchmark SRS.

## Reproduccion

Comandos ejecutados:

```powershell
python -m py_compile scripts\m25_c3_minimal_guarded_benchmark.py tests\test_m25_c3_minimal_guarded_benchmark.py
python -m unittest tests.test_m25_c3_minimal_guarded_benchmark
python -m unittest tests.test_m24_microguard_design tests.test_m24_srs_semantic_audit tests.test_m25_c3_minimal_guarded_benchmark
python scripts\m25_c3_minimal_guarded_benchmark.py --root C:\dev\vert\collatz-m25-c3-minimal-guarded-benchmark
```

Resultado de la suite M25:

```text
Ran 7 tests in 0.258s
OK
```

Resultado de la verificacion final M24+M25:

```text
Ran 19 tests in 0.288s
OK
```

El script devuelve codigo `0` cuando pasan los checks de implicacion, aunque el
campo `c3_build_status` permanezca `blocked`. Esto separa el exito del checker
finito de cualquier claim inexistente sobre terminacion o SRS guardado.
