from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


@dataclass(frozen=True)
class Distribution:
    probabilities: tuple[Fraction, ...]
    tail_after_max: Fraction

    def plus(self, other: "Distribution") -> "Distribution":
        if len(self.probabilities) != len(other.probabilities):
            raise ValueError("distributions must use the same support")
        return Distribution(
            probabilities=tuple(a + b for a, b in zip(self.probabilities, other.probabilities)),
            tail_after_max=self.tail_after_max + other.tail_after_max,
        )

    def scale(self, weight: Fraction) -> "Distribution":
        return Distribution(
            probabilities=tuple(weight * value for value in self.probabilities),
            tail_after_max=weight * self.tail_after_max,
        )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compute exact low-modulus algebraic distributions for next_tail under "
            "2-adic uniform lifting, without sampling orbit ranges."
        )
    )
    parser.add_argument("--min-k", type=int, default=2)
    parser.add_argument("--max-k", type=int, default=6)
    parser.add_argument("--max-next-tail", type=int, default=10)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    return parser.parse_args()


def v2(value: int) -> int:
    if value <= 0:
        raise ValueError("v2 expects a positive integer")
    exponent = 0
    while value % 2 == 0:
        exponent += 1
        value //= 2
    return exponent


def zero_distribution(max_tail: int) -> Distribution:
    return Distribution(tuple(Fraction(0) for _ in range(max_tail)), Fraction(0))


def point_distribution(next_tail: int, max_tail: int) -> Distribution:
    probabilities = [Fraction(0) for _ in range(max_tail)]
    tail_after_max = Fraction(0)
    if next_tail <= max_tail:
        probabilities[next_tail - 1] = Fraction(1)
    else:
        tail_after_max = Fraction(1)
    return Distribution(tuple(probabilities), tail_after_max)


def shifted_geometric_distribution(start_tail: int, max_tail: int) -> Distribution:
    probabilities = []
    for next_tail in range(1, max_tail + 1):
        if next_tail < start_tail:
            probabilities.append(Fraction(0))
        else:
            probabilities.append(Fraction(1, 2 ** (next_tail - start_tail + 1)))

    if max_tail < start_tail:
        tail_after_max = Fraction(1)
    else:
        tail_after_max = Fraction(1, 2 ** (max_tail - start_tail + 1))
    return Distribution(tuple(probabilities), tail_after_max)


def geometric_distribution(max_tail: int) -> Distribution:
    return shifted_geometric_distribution(1, max_tail)


def multiplicative_order_three(k: int) -> int:
    if k <= 1:
        return 1
    if k == 2:
        return 2
    return 2 ** (k - 2)


def fixed_tail_q_class_distribution(tail: int, q_residue: int, q_k: int, max_tail: int) -> Distribution:
    """Return P(next_tail | fixed tail, q == q_residue mod 2^q_k)."""
    if q_k < 1:
        raise ValueError("q_k must be positive because q is odd")
    modulus = 1 << q_k
    q_residue %= modulus
    if q_residue % 2 == 0:
        raise ValueError("q_residue must be odd")

    y_residue = (pow(3, tail, modulus) * q_residue) % modulus
    if y_residue == 1:
        return geometric_distribution(max_tail)

    exit_v2 = v2((y_residue - 1) % modulus)
    known_bits_after_exit = q_k - exit_v2
    next_odd_residue = (((y_residue - 1) % modulus) >> exit_v2) % (1 << known_bits_after_exit)

    if (next_odd_residue + 1) % (1 << known_bits_after_exit) == 0:
        return shifted_geometric_distribution(known_bits_after_exit, max_tail)

    return point_distribution(v2(next_odd_residue + 1), max_tail)


def q_mod_distribution(q_residue: int, k: int, max_tail: int) -> Distribution:
    """Return P(next_tail | q == q_residue mod 2^k), averaging tail geometrically."""
    period = multiplicative_order_three(k)
    period_denominator = Fraction(1) - Fraction(1, 2**period)
    result = zero_distribution(max_tail)

    for tail_residue in range(1, period + 1):
        weight = Fraction(1, 2**tail_residue) / period_denominator
        result = result.plus(
            fixed_tail_q_class_distribution(tail_residue, q_residue, k, max_tail).scale(weight)
        )

    return result


def n_mod_distribution(n_residue: int, k: int, max_tail: int) -> Distribution:
    """Return P(next_tail | odd n == n_residue mod 2^k)."""
    modulus = 1 << k
    n_residue %= modulus
    if n_residue % 2 == 0:
        raise ValueError("n_residue must be odd")

    if n_residue == modulus - 1:
        return geometric_distribution(max_tail)

    tail = v2(n_residue + 1)
    q_k = k - tail
    q_residue = ((n_residue + 1) >> tail) % (1 << q_k)
    return fixed_tail_q_class_distribution(tail, q_residue, q_k, max_tail)


def fraction_text(value: Fraction) -> str:
    return f"{value.numerator}/{value.denominator}"


def decimal(value: Fraction) -> float:
    return float(value)


def distribution_rows(
    classifier: str,
    k: int,
    residue: int,
    distribution: Distribution,
    geometric: Distribution,
) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    modulus = 1 << k
    for index, (probability, geometric_probability) in enumerate(
        zip(distribution.probabilities, geometric.probabilities),
        start=1,
    ):
        rows.append(
            {
                "classifier": classifier,
                "k": k,
                "modulus": modulus,
                "residue": residue,
                "next_tail": str(index),
                "probability_fraction": fraction_text(probability),
                "probability": f"{decimal(probability):.12f}",
                "geometric_fraction": fraction_text(geometric_probability),
                "geometric_probability": f"{decimal(geometric_probability):.12f}",
                "diff_vs_geometric": f"{decimal(probability - geometric_probability):.12f}",
                "abs_diff_vs_geometric": f"{abs(decimal(probability - geometric_probability)):.12f}",
            }
        )

    rows.append(
        {
            "classifier": classifier,
            "k": k,
            "modulus": modulus,
            "residue": residue,
            "next_tail": f"ge_{len(distribution.probabilities) + 1}",
            "probability_fraction": fraction_text(distribution.tail_after_max),
            "probability": f"{decimal(distribution.tail_after_max):.12f}",
            "geometric_fraction": fraction_text(geometric.tail_after_max),
            "geometric_probability": f"{decimal(geometric.tail_after_max):.12f}",
            "diff_vs_geometric": f"{decimal(distribution.tail_after_max - geometric.tail_after_max):.12f}",
            "abs_diff_vs_geometric": f"{abs(decimal(distribution.tail_after_max - geometric.tail_after_max)):.12f}",
        }
    )
    return rows


def distribution_max_diff(distribution: Distribution, geometric: Distribution) -> tuple[Fraction, str]:
    max_diff = Fraction(0)
    max_label = "1"
    for index, (probability, geometric_probability) in enumerate(
        zip(distribution.probabilities, geometric.probabilities),
        start=1,
    ):
        diff = abs(probability - geometric_probability)
        if diff > max_diff:
            max_diff = diff
            max_label = str(index)

    tail_diff = abs(distribution.tail_after_max - geometric.tail_after_max)
    if tail_diff > max_diff:
        max_diff = tail_diff
        max_label = f"ge_{len(distribution.probabilities) + 1}"

    return max_diff, max_label


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    if args.min_k < 1:
        raise ValueError("min-k must be positive")
    if args.max_k < args.min_k:
        raise ValueError("max-k must be greater than or equal to min-k")
    if args.max_next_tail < 1:
        raise ValueError("max-next-tail must be positive")

    geometric = geometric_distribution(args.max_next_tail)
    detail_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for classifier in ("q_mod", "n_mod"):
        for k in range(args.min_k, args.max_k + 1):
            class_count = 0
            geometric_class_count = 0
            max_abs_diff = Fraction(0)
            max_abs_diff_residue = 1
            max_abs_diff_tail = "1"
            max_tail1_diff = Fraction(0)
            max_tail1_residue = 1

            for residue in range(1, 1 << k, 2):
                if classifier == "q_mod":
                    distribution = q_mod_distribution(residue, k, args.max_next_tail)
                else:
                    distribution = n_mod_distribution(residue, k, args.max_next_tail)

                class_count += 1
                if distribution == geometric:
                    geometric_class_count += 1

                class_diff, class_tail = distribution_max_diff(distribution, geometric)
                if class_diff > max_abs_diff:
                    max_abs_diff = class_diff
                    max_abs_diff_residue = residue
                    max_abs_diff_tail = class_tail

                tail1_diff = distribution.probabilities[0] - geometric.probabilities[0]
                if abs(tail1_diff) > abs(max_tail1_diff):
                    max_tail1_diff = tail1_diff
                    max_tail1_residue = residue

                detail_rows.extend(
                    distribution_rows(classifier, k, residue, distribution, geometric)
                )

            summary_rows.append(
                {
                    "classifier": classifier,
                    "k": k,
                    "modulus": 1 << k,
                    "class_count": class_count,
                    "classes_matching_geometric": geometric_class_count,
                    "classes_deviating_from_geometric": class_count - geometric_class_count,
                    "max_abs_diff_fraction": fraction_text(max_abs_diff),
                    "max_abs_diff": f"{decimal(max_abs_diff):.12f}",
                    "max_abs_diff_residue": max_abs_diff_residue,
                    "max_abs_diff_next_tail": max_abs_diff_tail,
                    "max_tail1_diff_fraction": fraction_text(max_tail1_diff),
                    "max_tail1_diff": f"{decimal(max_tail1_diff):.12f}",
                    "max_tail1_diff_residue": max_tail1_residue,
                    "recommendation": (
                        "deviates_theoretically"
                        if class_count - geometric_class_count
                        else "matches_geometric"
                    ),
                }
            )

    detail_path = args.out_dir / "m15_algebra_next_tail_by_mod.csv"
    summary_path = args.out_dir / "m15_algebra_summary.csv"
    write_csv(
        detail_rows,
        detail_path,
        [
            "classifier",
            "k",
            "modulus",
            "residue",
            "next_tail",
            "probability_fraction",
            "probability",
            "geometric_fraction",
            "geometric_probability",
            "diff_vs_geometric",
            "abs_diff_vs_geometric",
        ],
    )
    write_csv(
        summary_rows,
        summary_path,
        [
            "classifier",
            "k",
            "modulus",
            "class_count",
            "classes_matching_geometric",
            "classes_deviating_from_geometric",
            "max_abs_diff_fraction",
            "max_abs_diff",
            "max_abs_diff_residue",
            "max_abs_diff_next_tail",
            "max_tail1_diff_fraction",
            "max_tail1_diff",
            "max_tail1_diff_residue",
            "recommendation",
        ],
    )

    print(f"min_k={args.min_k}")
    print(f"max_k={args.max_k}")
    print(f"max_next_tail={args.max_next_tail}")
    print(f"detail={detail_path}")
    print(f"summary={summary_path}")
    for row in summary_rows:
        if row["classifier"] == "q_mod":
            print(
                "q_mod",
                f"K={row['k']}",
                f"deviating={row['classes_deviating_from_geometric']}/{row['class_count']}",
                f"max_abs_diff={row['max_abs_diff']}",
                f"residue={row['max_abs_diff_residue']}",
                f"next_tail={row['max_abs_diff_next_tail']}",
            )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
