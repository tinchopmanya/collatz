# M24 microguard design

Fecha: 2026-04-29
Agente: CodexHijo-M24-MicroGuardDesign
Rama: `codex-hijo/m24-microguard-design`
Estado: exploratorio; bloqueado por `M24-SRS-SemanticAudit`

## Veredicto corto

El candidato `r mod 2^13 = 8189` sigue siendo rank 1 en
`reports/m22_residual_stats_candidate_subfamilies.csv`.

Se materializo un artefacto minimo y textual, no un SRS:

- `reports/m24_microguard_8189.guard.txt`
- `reports/m24_microguard_8189_summary.csv`
- `reports/m24_microguard_8189_violations.csv`
- `scripts/m24_microguard_design.py`
- `tests/test_m24_microguard_design.py`

Resultado del checker:

```text
m24_microguard=PASS
accepted_count=8
certified_overlap_count=0
srs_equivalence_status=blocked_by_M24-SRS-SemanticAudit
```

No se ejecuto C3. No se llamo a Matchbox, AProVE ni a ningun prover de
terminacion. Este M24 no afirma equivalencia SRS ni terminacion.

## Formato de guard

Formato textual: `m24.microguard.v1`.

La guarda propuesta es solo una condicion finita sobre residuos:

```text
universe: r modulo 2^16
branch_tag: S2_without_tf_end_to_end
branch_tag_status: tag_only_not_operational_equivalence
guard: r mod 2^13 = 8189
claim_scope: finite_residue_implication_only
srs_equivalence_status: blocked_by_M24-SRS-SemanticAudit
contains_certificates: false
```

Residuos aceptados:

```text
8189 16381 24573 32765 40957 49149 57341 65533
```

La guarda usa un selector low-bit simple: fijar los 13 bits bajos a `8189`.
Como `8189 mod 8 = 5`, tambien implica el tag local S2 por residuos. Esa frase
no debe leerse como equivalencia operacional con el SRS mixto; es solo el tag
heredado de M22.

## Checker de implicacion

`scripts/m24_microguard_design.py` hace checks finitos sobre `0 <= r < 2^16`.
No importa ni genera SRS, no invoca provers y no embeddea certificados.

Checks principales:

- Selecciona `r mod 2^13 = 8189` y falla por defecto si ya no es rank 1.
- Recalcula los residuos aceptados desde la sintaxis del selector, no confia
  solo en la columna `residues`.
- Verifica que la fila del CSV declara `selector_exact_for_u16=True` y
  `non_residual_s2_overinclude=0`.
- Verifica `guard(r) => r in U_16`, donde `U_16` es el complemento congelado
  `reports/m22_s2_k16_uncovered_residues.csv`.
- Verifica `guard(r) => r not in C_16`, usando
  `reports/m22_c1_rechecker.certified_residues.csv` solo como lista de control.
- Verifica `guard(r) => r mod 8 = 5`.
- Verifica hashes congelados de `U_16` y `C_16`.

Hashes esperados:

```text
U_16 uncovered_sha256 = bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210
C_16 certified_sha256 = 0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa
G_8189 accepted_sha256 = de4100dcb707ee6d42acf0fc6af8b8bb8d2a70852b1a2af461d64e4926eb281c
```

## Entradas y salidas esperadas

Entradas por defecto:

```text
reports/m22_residual_stats_candidate_subfamilies.csv
reports/m22_s2_k16_uncovered_residues.csv
reports/m22_c1_rechecker.certified_residues.csv
```

Comando reproducible:

```powershell
python scripts\m24_microguard_design.py
python -m py_compile scripts\m24_microguard_design.py tests\test_m24_microguard_design.py
python -m unittest tests.test_m24_microguard_design
```

Salidas esperadas:

```text
reports/m24_microguard_8189.guard.txt
reports/m24_microguard_8189_summary.csv
reports/m24_microguard_8189_violations.csv
```

`summary.csv` debe reportar:

```text
candidate_rank = 1
accepted_count = 8
frozen_selector_count = 8
certified_overlap_count = 0
outside_s2_count = 0
passed = True
claim_scope = finite_residue_implication_only
srs_equivalence_status = blocked_by_M24-SRS-SemanticAudit
contains_certificates = False
```

`violations.csv` debe tener solo header mientras el guard siga siendo valido.

## Riesgos de inflar CNF

- Codificar la guarda como ocho residuos completos de 16 bits es tolerable para
  esta microfamilia, pero escalar a los 378 residuos de `U_16` puede multiplicar
  disyunciones de igualdades y variables Tseitin.
- Duplicar el predicado en cada regla o posicion del SRS puede convertir una
  guarda pequena en producto `reglas x posiciones x bits`.
- Usar un automata/trie completo para el complemento congelado podria heredar
  los 1473 nodos LSB-first de M22; para un primer benchmark conviene fijar
  solo los 13 bits bajos de esta microfamilia.
- Codificar `not in C_16` dentro del benchmark seria un error practico y
  epistemico: `C_16` tiene 7814 residuos y no debe embeddearse como certificado
  negativo. El checker lo usa fuera de banda.
- Si la traduccion SRS requiere producto entre estados del guard y estados del
  sistema de reescritura, el benchmark puede crecer aunque la microfamilia sea
  aritmeticamente pequena.
- Una reduccion de instancias no implica menor CNF: algunos frontends SAT
  bit-blastean congruencias, rangos o automatas con overhead mayor que el SRS
  base.

Mitigacion propuesta: en un futuro M24 post-auditoria, empezar solo con
`r mod 2^13 = 8189` como igualdad de 13 LSBs, medir variables/clausulas contra
S2 base antes de cualquier claim, y abortar si el guardado cambia el problema o
infla CNF sin una nueva senal objetiva.

## Bloqueo semantico

Este artefacto queda bloqueado por `M24-SRS-SemanticAudit`.

Antes de cualquier claim fuerte hace falta una auditoria que demuestre, con una
especificacion local, que el guard sobre residuos corresponde exactamente al
subproblema operacional del SRS mixto que se quiere conservar. Hasta entonces:

- No hay equivalencia SRS.
- No hay benchmark C3 valido.
- No hay claim de terminacion.
- No hay prueba de Collatz.
- El artefacto solo dice que una microfamilia finita es subset exacto del
  complemento congelado y no intersecta certificados.
