from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block  # noqa: E402


RESIDUES = (1, 3, 5, 7)
RESIDUE_INDEX = {residue: index for index, residue in enumerate(RESIDUES)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Estimate the q_{i+1} mod 8 | q_i mod 8 transition matrix for the "
            "project's odd-to-odd alternating-block map."
        )
    )
    parser.add_argument("--start", type=int, default=3)
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--mixing-steps", type=int, default=4)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m15_qmod8_transition")
    return parser.parse_args()


def first_odd_at_least(value: int) -> int:
    return value if value % 2 else value + 1


def q_mod8_for_odd(n: int) -> int:
    return alternating_block(n).odd_factor % 8


def collect_counts(start: int, limit: int) -> list[list[int]]:
    if limit < start:
        raise ValueError("limit must be greater than or equal to start")

    counts = [[0 for _ in RESIDUES] for _ in RESIDUES]
    for n in range(first_odd_at_least(start), limit + 1, 2):
        block = alternating_block(n)
        next_block = alternating_block(block.next_odd)
        source = block.odd_factor % 8
        target = next_block.odd_factor % 8
        counts[RESIDUE_INDEX[source]][RESIDUE_INDEX[target]] += 1
    return counts


def row_probabilities(counts: list[list[int]]) -> list[list[float]]:
    probabilities: list[list[float]] = []
    for row in counts:
        total = sum(row)
        if total == 0:
            probabilities.append([0.0 for _ in row])
        else:
            probabilities.append([value / total for value in row])
    return probabilities


def matrix_multiply(left: list[list[float]], right: list[list[float]]) -> list[list[float]]:
    size = len(left)
    return [
        [
            sum(left[row][inner] * right[inner][col] for inner in range(size))
            for col in range(size)
        ]
        for row in range(size)
    ]


def vector_matrix_multiply(vector: list[float], matrix: list[list[float]]) -> list[float]:
    return [
        sum(vector[row] * matrix[row][col] for row in range(len(vector)))
        for col in range(len(vector))
    ]


def stationary_distribution(matrix: list[list[float]], tolerance: float = 1e-15) -> list[float]:
    size = len(matrix)
    distribution = [1.0 / size for _ in range(size)]
    for _ in range(100_000):
        updated = vector_matrix_multiply(distribution, matrix)
        if max(abs(updated[index] - distribution[index]) for index in range(size)) < tolerance:
            return updated
        distribution = updated
    return distribution


def total_variation(left: list[float], right: list[float]) -> float:
    return 0.5 * sum(abs(a - b) for a, b in zip(left, right))


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def transition_rows(counts: list[list[int]], probabilities: list[list[float]]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for source_index, source in enumerate(RESIDUES):
        row_total = sum(counts[source_index])
        for target_index, target in enumerate(RESIDUES):
            probability = probabilities[source_index][target_index]
            rows.append(
                {
                    "from_q_mod8": source,
                    "to_q_mod8": target,
                    "count": counts[source_index][target_index],
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
    source_totals = [sum(row) for row in counts]
    target_totals = [
        sum(counts[row][col] for row in range(len(RESIDUES)))
        for col in range(len(RESIDUES))
    ]
    next_from_source = vector_matrix_multiply(
        [source_total / total for source_total in source_totals],
        probabilities,
    )
    return [
        {
            "q_mod8": residue,
            "source_count": source_totals[index],
            "target_count": target_totals[index],
            "source_fraction": f"{source_totals[index] / total:.12f}",
            "target_fraction": f"{target_totals[index] / total:.12f}",
            "one_step_from_source_fraction": f"{next_from_source[index]:.12f}",
            "stationary_fraction": f"{stationary[index]:.12f}",
            "uniform_fraction": "0.250000000000",
            "stationary_diff_vs_uniform": f"{stationary[index] - 0.25:.12f}",
        }
        for index, residue in enumerate(RESIDUES)
    ]


def mixing_rows(probabilities: list[list[float]], stationary: list[float], steps: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    uniform = [1.0 / len(RESIDUES) for _ in RESIDUES]
    power = [row[:] for row in probabilities]
    for step in range(1, steps + 1):
        for source_index, source in enumerate(RESIDUES):
            distribution = power[source_index]
            rows.append(
                {
                    "steps": step,
                    "from_q_mod8": source,
                    "p_to_1": f"{distribution[0]:.12f}",
                    "p_to_3": f"{distribution[1]:.12f}",
                    "p_to_5": f"{distribution[2]:.12f}",
                    "p_to_7": f"{distribution[3]:.12f}",
                    "tv_to_stationary": f"{total_variation(distribution, stationary):.12f}",
                    "tv_to_uniform": f"{total_variation(distribution, uniform):.12f}",
                }
            )
        power = matrix_multiply(power, probabilities)
    return rows


def summary_rows(
    start: int,
    limit: int,
    counts: list[list[int]],
    probabilities: list[list[float]],
    stationary: list[float],
    mixing: list[dict[str, object]],
) -> list[dict[str, object]]:
    total = sum(sum(row) for row in counts)
    max_row_tv_uniform = max(
        total_variation(row, [0.25, 0.25, 0.25, 0.25])
        for row in probabilities
    )
    max_row_abs_diff = max(abs(value - 0.25) for row in probabilities for value in row)
    max_stationary_abs_diff = max(abs(value - 0.25) for value in stationary)
    max_tv_by_step: dict[int, float] = {}
    for row in mixing:
        step = int(row["steps"])
        max_tv_by_step[step] = max(max_tv_by_step.get(step, 0.0), float(row["tv_to_uniform"]))

    rows = [
        {"metric": "start", "value": start},
        {"metric": "limit", "value": limit},
        {"metric": "total_transitions", "value": total},
        {"metric": "max_row_total_variation_to_uniform", "value": f"{max_row_tv_uniform:.12f}"},
        {"metric": "max_cell_abs_diff_vs_uniform", "value": f"{max_row_abs_diff:.12f}"},
        {"metric": "max_stationary_abs_diff_vs_uniform", "value": f"{max_stationary_abs_diff:.12f}"},
    ]
    for step in sorted(max_tv_by_step):
        rows.append(
            {
                "metric": f"max_total_variation_to_uniform_after_{step}_steps",
                "value": f"{max_tv_by_step[step]:.12f}",
            }
        )
    recommendation = (
        "cool_m15_before_holdout"
        if max_tv_by_step.get(3, max_row_tv_uniform) < 0.001
        else "consider_confirmatory_design"
    )
    rows.append({"metric": "mechanical_recommendation", "value": recommendation})
    rows.append(
        {
            "metric": "scope_note",
            "value": (
                "empirical exploratory local transitions on burned range; "
                "not a holdout and not a survival comparison"
            ),
        }
    )
    return rows


def main() -> int:
    args = parse_args()
    counts = collect_counts(args.start, args.limit)
    probabilities = row_probabilities(counts)
    stationary = stationary_distribution(probabilities)
    mixing = mixing_rows(probabilities, stationary, args.mixing_steps)

    matrix_path = args.out_dir / f"{args.prefix}_matrix.csv"
    stationary_path = args.out_dir / f"{args.prefix}_stationary.csv"
    mixing_path = args.out_dir / f"{args.prefix}_mixing.csv"
    summary_path = args.out_dir / f"{args.prefix}_summary.csv"

    write_csv(
        transition_rows(counts, probabilities),
        matrix_path,
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
        stationary_rows(counts, probabilities, stationary),
        stationary_path,
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
        mixing,
        mixing_path,
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
        summary_rows(args.start, args.limit, counts, probabilities, stationary, mixing),
        summary_path,
        ["metric", "value"],
    )

    print(f"start={args.start}")
    print(f"limit={args.limit}")
    print(f"matrix={matrix_path}")
    print(f"stationary={stationary_path}")
    print(f"mixing={mixing_path}")
    print(f"summary={summary_path}")
    for source_index, source in enumerate(RESIDUES):
        formatted = " ".join(f"{value:.8f}" for value in probabilities[source_index])
        print(f"from {source}: {formatted}")
    max_tv_after_three = max(
        float(row["tv_to_uniform"])
        for row in mixing
        if int(row["steps"]) == min(3, args.mixing_steps)
    )
    print(f"max_tv_to_uniform_after_{min(3, args.mixing_steps)}_steps={max_tv_after_three:.12f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
