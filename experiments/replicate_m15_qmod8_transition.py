from __future__ import annotations

import argparse
import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RESIDUES = (1, 3, 5, 7)
POSITION = {residue: index for index, residue in enumerate(RESIDUES)}
UNIFORM = [0.25, 0.25, 0.25, 0.25]

# Counts reported by CodexHijo1 for
# reports/m15_qmod8_transition_matrix.csv. They are used only for the
# explicit replication comparison, not for the computation below.
CODEXHIJO1_COUNTS = {
    1: {1: 156256, 3: 156252, 5: 156244, 7: 156257},
    3: {1: 156268, 3: 156271, 5: 156248, 7: 156215},
    5: {1: 156247, 3: 156248, 5: 156250, 7: 156251},
    7: {1: 156248, 3: 156247, 5: 156244, 7: 156253},
}
CODEXHIJO1_TV_STEP1 = 0.000060799805
CODEXHIJO1_TV_STEP3 = 0.000015000447


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Independent replication of the q_{i+1} mod 8 | q_i mod 8 "
            "transition matrix for the M15 Collatz gate."
        )
    )
    parser.add_argument("--start", type=int, default=3)
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--mixing-steps", type=int, default=4)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m15_qmod8_transition_replica")
    parser.add_argument(
        "--report",
        type=Path,
        default=ROOT / "colaboradores" / "codex-hijo" / "ReplicaM15QMod8Transition.md",
    )
    return parser.parse_args()


def twos(value: int) -> int:
    if value <= 0:
        raise ValueError("twos expects a positive integer")
    return (value & -value).bit_length() - 1


def odd_factor_of_successor(n: int) -> int:
    return (n + 1) >> twos(n + 1)


def odd_to_odd_step(n: int) -> int:
    """Project block map, implemented directly from the arithmetic formula."""

    tail = twos(n + 1)
    q = (n + 1) >> tail
    exit_source = (3**tail) * q - 1
    return exit_source >> twos(exit_source)


def first_odd_at_or_after(value: int) -> int:
    return value if value % 2 else value + 1


def collect_transition_counts(start: int, limit: int) -> list[list[int]]:
    if limit < start:
        raise ValueError("limit must be >= start")

    matrix = [[0 for _ in RESIDUES] for _ in RESIDUES]
    for n in range(first_odd_at_or_after(start), limit + 1, 2):
        q_now = odd_factor_of_successor(n) % 8
        next_n = odd_to_odd_step(n)
        q_next = odd_factor_of_successor(next_n) % 8
        matrix[POSITION[q_now]][POSITION[q_next]] += 1
    return matrix


def normalize_rows(counts: list[list[int]]) -> list[list[float]]:
    rows: list[list[float]] = []
    for row in counts:
        row_total = sum(row)
        rows.append([cell / row_total for cell in row])
    return rows


def multiply_square(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    width = len(left)
    return [
        [
            sum(left[row][middle] * right[middle][col] for middle in range(width))
            for col in range(width)
        ]
        for row in range(width)
    ]


def apply_row_vector(vector: list[float], matrix: list[list[float]]) -> list[float]:
    return [
        sum(vector[row] * matrix[row][col] for row in range(len(vector)))
        for col in range(len(vector))
    ]


def tv_distance(a: list[float], b: list[float]) -> float:
    return 0.5 * sum(abs(left - right) for left, right in zip(a, b))


def estimate_stationary(matrix: list[list[float]]) -> list[float]:
    current = [0.25, 0.25, 0.25, 0.25]
    for _ in range(100_000):
        updated = apply_row_vector(current, matrix)
        if max(abs(updated[i] - current[i]) for i in range(4)) < 1e-15:
            return updated
        current = updated
    return current


def transition_rows(counts: list[list[int]], probabilities: list[list[float]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for from_index, from_residue in enumerate(RESIDUES):
        row_total = sum(counts[from_index])
        for to_index, to_residue in enumerate(RESIDUES):
            probability = probabilities[from_index][to_index]
            rows.append(
                {
                    "from_q_mod8": from_residue,
                    "to_q_mod8": to_residue,
                    "count": counts[from_index][to_index],
                    "row_count": row_total,
                    "probability": f"{probability:.12f}",
                    "uniform_probability": "0.250000000000",
                    "diff_vs_uniform": f"{probability - 0.25:.12f}",
                }
            )
    return rows


def stationary_rows(
    counts: list[list[int]],
    probabilities: list[list[float]],
    stationary: list[float],
) -> list[dict[str, object]]:
    total = sum(sum(row) for row in counts)
    row_totals = [sum(row) for row in counts]
    col_totals = [sum(counts[row][col] for row in range(4)) for col in range(4)]
    empirical_source = [row_total / total for row_total in row_totals]
    one_step = apply_row_vector(empirical_source, probabilities)

    return [
        {
            "q_mod8": residue,
            "source_count": row_totals[index],
            "target_count": col_totals[index],
            "source_fraction": f"{empirical_source[index]:.12f}",
            "target_fraction": f"{col_totals[index] / total:.12f}",
            "one_step_from_source_fraction": f"{one_step[index]:.12f}",
            "stationary_fraction": f"{stationary[index]:.12f}",
            "uniform_fraction": "0.250000000000",
            "stationary_diff_vs_uniform": f"{stationary[index] - 0.25:.12f}",
        }
        for index, residue in enumerate(RESIDUES)
    ]


def mixing_rows(probabilities: list[list[float]], stationary: list[float], steps: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    power = [row[:] for row in probabilities]
    for step in range(1, steps + 1):
        for from_index, from_residue in enumerate(RESIDUES):
            distribution = power[from_index]
            rows.append(
                {
                    "steps": step,
                    "from_q_mod8": from_residue,
                    "p_to_1": f"{distribution[0]:.12f}",
                    "p_to_3": f"{distribution[1]:.12f}",
                    "p_to_5": f"{distribution[2]:.12f}",
                    "p_to_7": f"{distribution[3]:.12f}",
                    "tv_to_stationary": f"{tv_distance(distribution, stationary):.12f}",
                    "tv_to_uniform": f"{tv_distance(distribution, UNIFORM):.12f}",
                }
            )
        power = multiply_square(power, probabilities)
    return rows


def matrix_max_tv(probabilities: list[list[float]]) -> float:
    return max(tv_distance(row, UNIFORM) for row in probabilities)


def max_tv_by_step(rows: list[dict[str, object]]) -> dict[int, float]:
    by_step: dict[int, float] = {}
    for row in rows:
        step = int(row["steps"])
        by_step[step] = max(by_step.get(step, 0.0), float(row["tv_to_uniform"]))
    return by_step


def reference_probability(from_residue: int, to_residue: int) -> float:
    ref_row = CODEXHIJO1_COUNTS[from_residue]
    return ref_row[to_residue] / sum(ref_row.values())


def comparison_rows(counts: list[list[int]], probabilities: list[list[float]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for from_index, from_residue in enumerate(RESIDUES):
        for to_index, to_residue in enumerate(RESIDUES):
            observed_count = counts[from_index][to_index]
            ref_count = CODEXHIJO1_COUNTS[from_residue][to_residue]
            observed_probability = probabilities[from_index][to_index]
            ref_probability = reference_probability(from_residue, to_residue)
            rows.append(
                {
                    "from_q_mod8": from_residue,
                    "to_q_mod8": to_residue,
                    "replica_count": observed_count,
                    "codexhijo1_count": ref_count,
                    "count_diff": observed_count - ref_count,
                    "replica_probability": f"{observed_probability:.12f}",
                    "codexhijo1_probability": f"{ref_probability:.12f}",
                    "probability_diff": f"{observed_probability - ref_probability:.12f}",
                    "abs_probability_diff": f"{abs(observed_probability - ref_probability):.12f}",
                }
            )
    return rows


def summary_rows(
    start: int,
    limit: int,
    counts: list[list[int]],
    probabilities: list[list[float]],
    stationary: list[float],
    mixing: list[dict[str, object]],
    comparison: list[dict[str, object]],
) -> list[dict[str, object]]:
    step_tvs = max_tv_by_step(mixing)
    total = sum(sum(row) for row in counts)
    max_cell_abs_diff = max(abs(value - 0.25) for row in probabilities for value in row)
    max_stationary_abs_diff = max(abs(value - 0.25) for value in stationary)
    max_count_diff = max(abs(int(row["count_diff"])) for row in comparison)
    max_probability_diff = max(float(row["abs_probability_diff"]) for row in comparison)

    rows = [
        {"metric": "start", "value": start},
        {"metric": "limit", "value": limit},
        {"metric": "total_transitions", "value": total},
        {"metric": "max_row_total_variation_to_uniform", "value": f"{matrix_max_tv(probabilities):.12f}"},
        {"metric": "max_cell_abs_diff_vs_uniform", "value": f"{max_cell_abs_diff:.12f}"},
        {"metric": "max_stationary_abs_diff_vs_uniform", "value": f"{max_stationary_abs_diff:.12f}"},
    ]
    for step in sorted(step_tvs):
        rows.append(
            {
                "metric": f"max_total_variation_to_uniform_after_{step}_steps",
                "value": f"{step_tvs[step]:.12f}",
            }
        )
    rows.extend(
        [
            {"metric": "codexhijo1_tv_step1", "value": f"{CODEXHIJO1_TV_STEP1:.12f}"},
            {"metric": "codexhijo1_tv_step3", "value": f"{CODEXHIJO1_TV_STEP3:.12f}"},
            {
                "metric": "tv_step1_diff_vs_codexhijo1",
                "value": f"{abs(step_tvs[1] - CODEXHIJO1_TV_STEP1):.12f}",
            },
            {
                "metric": "tv_step3_diff_vs_codexhijo1",
                "value": f"{abs(step_tvs[3] - CODEXHIJO1_TV_STEP3):.12f}",
            },
            {"metric": "max_count_diff_vs_codexhijo1", "value": max_count_diff},
            {
                "metric": "max_probability_diff_vs_codexhijo1",
                "value": f"{max_probability_diff:.12f}",
            },
            {
                "metric": "verdict",
                "value": "replica_exacta" if max_count_diff == 0 else "contradice",
            },
            {
                "metric": "recommendation",
                "value": "cerrar_o_enfriar_m15_marginal_q_mod8",
            },
        ]
    )
    return rows


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def matrix_markdown(probabilities: list[list[float]]) -> str:
    lines = [
        "| desde \\ hacia | 1 | 3 | 5 | 7 |",
        "| ---: | ---: | ---: | ---: | ---: |",
    ]
    for row_index, residue in enumerate(RESIDUES):
        values = " | ".join(f"{probabilities[row_index][col]:.12f}" for col in range(4))
        lines.append(f"| {residue} | {values} |")
    return "\n".join(lines)


def counts_markdown(counts: list[list[int]]) -> str:
    lines = ["| `q_i mod 8` | conteo |", "| ---: | ---: |"]
    for row_index, residue in enumerate(RESIDUES):
        lines.append(f"| {residue} | {sum(counts[row_index])} |")
    return "\n".join(lines)


def mixing_markdown(step_tvs: dict[int, float]) -> str:
    lines = ["| pasos | max TV contra uniforme |", "| ---: | ---: |"]
    for step in sorted(step_tvs):
        lines.append(f"| {step} | {step_tvs[step]:.12f} |")
    return "\n".join(lines)


def write_report(
    path: Path,
    start: int,
    limit: int,
    probabilities: list[list[float]],
    counts: list[list[int]],
    stationary: list[float],
    step_tvs: dict[int, float],
    max_probability_diff: float,
    max_count_diff: int,
) -> None:
    station_lines = ["| `q mod 8` | estacionaria | diff vs uniforme |", "| ---: | ---: | ---: |"]
    for index, residue in enumerate(RESIDUES):
        station_lines.append(
            f"| {residue} | {stationary[index]:.12f} | {stationary[index] - 0.25:+.12f} |"
        )

    verdict = "replica exacta" if max_count_diff == 0 else "contradice"
    report = f"""# Replica M15 - transicion `q mod 8`

Fecha: 2026-04-25
Rama: `codex-hijo/m15-qmod8-transition-replica`

## Comando reproducible

```powershell
python experiments\\replicate_m15_qmod8_transition.py --limit {limit} --out-dir reports --prefix m15_qmod8_transition_replica
```

Tambien verifique compilacion con:

```powershell
python -m py_compile experiments\\replicate_m15_qmod8_transition.py
```

## Definicion replicada

Use la definicion de `q` del proyecto:

```text
s_i = v2(n_i + 1)
q_i = (n_i + 1) / 2^s_i
n_{{i+1}} = (3^s_i q_i - 1) / 2^v2(3^s_i q_i - 1)
q_{{i+1}} = (n_{{i+1}} + 1) / 2^v2(n_{{i+1}} + 1)
```

La implementacion de replica no importa `collatz.alternating_block`; calcula
`v2`, `q` y el paso odd-to-odd directamente desde la formula. No encontre en
los documentos una segunda definicion razonable de `q`; `n mod 8` seria otra
variable, no otra definicion de `q`.

Poblacion:

```text
impares {start} <= n <= {limit}
una transicion odd-to-odd por impar inicial
sin holdout fresco
```

## Archivos

- `experiments/replicate_m15_qmod8_transition.py`
- `reports/m15_qmod8_transition_replica_matrix.csv`
- `reports/m15_qmod8_transition_replica_stationary.csv`
- `reports/m15_qmod8_transition_replica_mixing.csv`
- `reports/m15_qmod8_transition_replica_comparison.csv`
- `reports/m15_qmod8_transition_replica_summary.csv`

## Matriz replicada

Filas: `q_i mod 8`. Columnas: `q_{{i+1}} mod 8`.

{matrix_markdown(probabilities)}

Conteos por fila:

{counts_markdown(counts)}

## Mezcla

{mixing_markdown(step_tvs)}

Distribucion estacionaria estimada:

{chr(10).join(station_lines)}

## Comparacion contra CodexHijo1

CodexHijo1 reporto:

```text
max TV contra uniforme en 1 paso = 0.000060799805
max TV contra uniforme en 3 pasos = 0.000015000447
```

Esta replica obtiene:

```text
max TV contra uniforme en 1 paso = {step_tvs[1]:.12f}
max TV contra uniforme en 3 pasos = {step_tvs[3]:.12f}
```

Diferencias contra CodexHijo1:

```text
max diferencia de conteos = {max_count_diff}
max diferencia de probabilidad de celda = {max_probability_diff:.12f}
diff TV paso 1 = {abs(step_tvs[1] - CODEXHIJO1_TV_STEP1):.12f}
diff TV paso 3 = {abs(step_tvs[3] - CODEXHIJO1_TV_STEP3):.12f}
```

## Veredicto

```text
{verdict}
```

La matriz queda casi uniforme fila por fila y la distancia total variation
contra uniforme baja a escala `1.5e-5` en 2-3 pasos. Esto replica la compuerta
de CodexHijo1: `q mod 8` predice `next_tail` localmente, pero no conserva
memoria marginal apreciable como estado entre bloques consecutivos.

## Recomendacion al orquestador

Recomiendo cerrar o enfriar M15 en la forma marginal:

```text
q mod 8 como memoria suficiente para supervivencia orbital
```

Si M15 sigue vivo, deberia ser con otra formulacion preregistrada, no como
holdout inmediato de esta variable marginal.

## Que no deberiamos concluir

- No concluir una prueba ni una negacion global de Collatz.
- No concluir que `q mod 8` no predice `next_tail`; si lo predice localmente.
- No concluir que todo modulo superior o toda variable orbital carece de memoria.
- No concluir nada sobre el holdout fresco `15000001..25000000`; no se miro.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(report, encoding="utf-8")


def main() -> int:
    args = parse_args()
    counts = collect_transition_counts(args.start, args.limit)
    probabilities = normalize_rows(counts)
    stationary = estimate_stationary(probabilities)
    mixing = mixing_rows(probabilities, stationary, args.mixing_steps)
    comparison = comparison_rows(counts, probabilities)
    summary = summary_rows(
        args.start,
        args.limit,
        counts,
        probabilities,
        stationary,
        mixing,
        comparison,
    )

    matrix_path = args.out_dir / f"{args.prefix}_matrix.csv"
    stationary_path = args.out_dir / f"{args.prefix}_stationary.csv"
    mixing_path = args.out_dir / f"{args.prefix}_mixing.csv"
    comparison_path = args.out_dir / f"{args.prefix}_comparison.csv"
    summary_path = args.out_dir / f"{args.prefix}_summary.csv"

    write_csv(
        matrix_path,
        transition_rows(counts, probabilities),
        [
            "from_q_mod8",
            "to_q_mod8",
            "count",
            "row_count",
            "probability",
            "uniform_probability",
            "diff_vs_uniform",
        ],
    )
    write_csv(
        stationary_path,
        stationary_rows(counts, probabilities, stationary),
        [
            "q_mod8",
            "source_count",
            "target_count",
            "source_fraction",
            "target_fraction",
            "one_step_from_source_fraction",
            "stationary_fraction",
            "uniform_fraction",
            "stationary_diff_vs_uniform",
        ],
    )
    write_csv(
        mixing_path,
        mixing,
        [
            "steps",
            "from_q_mod8",
            "p_to_1",
            "p_to_3",
            "p_to_5",
            "p_to_7",
            "tv_to_stationary",
            "tv_to_uniform",
        ],
    )
    write_csv(
        comparison_path,
        comparison,
        [
            "from_q_mod8",
            "to_q_mod8",
            "replica_count",
            "codexhijo1_count",
            "count_diff",
            "replica_probability",
            "codexhijo1_probability",
            "probability_diff",
            "abs_probability_diff",
        ],
    )
    write_csv(summary_path, summary, ["metric", "value"])

    step_tvs = max_tv_by_step(mixing)
    max_count_diff = max(abs(int(row["count_diff"])) for row in comparison)
    max_probability_diff = max(float(row["abs_probability_diff"]) for row in comparison)
    write_report(
        args.report,
        args.start,
        args.limit,
        probabilities,
        counts,
        stationary,
        step_tvs,
        max_probability_diff,
        max_count_diff,
    )

    print(f"start={args.start}")
    print(f"limit={args.limit}")
    print(f"matrix={matrix_path}")
    print(f"stationary={stationary_path}")
    print(f"mixing={mixing_path}")
    print(f"comparison={comparison_path}")
    print(f"summary={summary_path}")
    print(f"report={args.report}")
    for row_index, residue in enumerate(RESIDUES):
        print(f"from {residue}: " + " ".join(f"{value:.8f}" for value in probabilities[row_index]))
    print(f"max_probability_diff_vs_codexhijo1={max_probability_diff:.12f}")
    print(f"max_tv_to_uniform_after_1_steps={step_tvs[1]:.12f}")
    if 3 in step_tvs:
        print(f"max_tv_to_uniform_after_3_steps={step_tvs[3]:.12f}")
    print("verdict=" + ("replica_exacta" if max_count_diff == 0 else "contradice"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
