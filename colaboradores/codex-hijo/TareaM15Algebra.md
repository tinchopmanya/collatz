# Tarea para Codex hijo - M15 algebra previa

Fecha: 2026-04-25
Estado: lista para ejecutar en rama propia

## Rol

Eres Codex hijo. Tu tarea no es buscar patrones ni correr holdout. Tu tarea es hacer el calculo algebraico previo que Claude pidio para M15.

## Regla principal

```text
Algebra antes que datos.
```

No hagas barridos estadisticos sobre rangos grandes hasta que el calculo modular diga que hay algo que buscar.

## Git

Antes de trabajar:

```powershell
git status --short --branch
git switch main
git pull
git switch -c codex-hijo/m15-algebra
```

Si la rama ya existe:

```powershell
git switch codex-hijo/m15-algebra
git pull
```

No trabajes en `main`.

Puedes hacer commit y push de tu rama:

```powershell
git add <archivos>
git commit -m "Analyze M15 modular algebra"
git push -u origin codex-hijo/m15-algebra
```

No hagas merge a `main`.

## Archivos que puedes tocar

Puedes crear:

- `experiments/analyze_m15_algebra.py`
- `reports/m15_algebra_next_tail_by_mod.csv`
- `reports/m15_algebra_summary.csv`
- `colaboradores/codex-hijo/ResultadosM15Algebra.md`

Puedes leer:

- `src/collatz/core.py`
- `experiments/test_m14_residual_robustness.py`
- `reports/m14_residual_robustness.md`
- `colaboradores/orquestador/DecisionM15TrasRevisionClaude.md`
- `colaboradores/revisor-claude/RevisionDisenoM15.md`

No modifiques:

- `Conlusion.md`
- `Investigacion.md`
- `InvestigacionMapa.md`
- `MILESTONES.md`
- `README.md`
- `src/`
- `tests/`

## Objetivo tecnico

Calcular si clases residuales de bajo modulo predicen `next_tail` de forma teorica.

Pregunta concreta:

```text
Para impares n agrupados por n mod 2^K o por q mod 2^K, cual es la distribucion teorica de next_tail?
```

Donde:

```text
tail = v2(n + 1)
q = (n + 1) / 2^tail
exit_v2 = v2(3^tail q - 1)
next_odd = (3^tail q - 1) / 2^exit_v2
next_tail = v2(next_odd + 1)
```

## Alcance inicial

Usar `K <= 6`.

No usar `prev_exit_v2 = 5` como foco aislado.

No usar holdout.

No mirar rangos `15M..25M`.

## Salida esperada

CSV:

```text
reports/m15_algebra_next_tail_by_mod.csv
reports/m15_algebra_summary.csv
```

Reporte:

```text
colaboradores/codex-hijo/ResultadosM15Algebra.md
```

El reporte debe responder:

1. La distribucion `P(next_tail | clase modular)` coincide con geometrica?
2. Hay alguna clase con desviacion teorica clara?
3. La desviacion aparece ya en modulo bajo (`2^3`, `2^4`, `2^5`, `2^6`)?
4. Vale la pena correr experimento train/holdout?
5. Que hipotesis pre-registrada recomendarias para H1?

## Criterio de exito

Exito si produces una tabla teorica clara y una recomendacion:

```text
H1 se descarta algebraicamente
```

o:

```text
H1 merece experimento train/holdout por estas clases exactas y este efecto teorico esperado.
```

## Criterio de abandono

Abandona o limita si:

- el calculo requiere modulo mayor que `2^6` para tener sentido;
- la cantidad de clases explota;
- no puedes definir una distribucion teorica sin hacer supuestos adicionales.

En ese caso, documenta exactamente donde se rompe el calculo.

## Estilo

Se conservador.

No vendas hallazgos.

No digas que hay prueba de Collatz.

Tu salida debe ayudar al orquestador a decidir si M15 debe gastar computo o no.
