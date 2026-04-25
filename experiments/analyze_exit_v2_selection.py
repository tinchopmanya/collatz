from __future__ import annotations

import argparse
import csv
import math
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import AlternatingBlock, alternating_block  # noqa: E402


@dataclass
class TransitionStats:
    source: str
    prev_exit_v2: int
    count: int = 0
    next_expansive_count: int = 0
    next_tail_sum: int = 0
    next_exit_v2_sum: int = 0
    tail_counts: Counter[int] = field(default_factory=Counter)
    exit_counts: Counter[int] = field(default_factory=Counter)
    joint_counts: Counter[tuple[int, int]] = field(default_factory=Counter)

    def add(self, next_block: AlternatingBlock) -> None:
        self.count += 1
        if is_expansive(next_block):
            self.next_expansive_count += 1
        self.next_tail_sum += next_block.tail_length
        self.next_exit_v2_sum += next_block.exit_v2
        self.tail_counts[next_block.tail_length] += 1
        self.exit_counts[next_block.exit_v2] += 1
        self.joint_counts[(next_block.tail_length, next_block.exit_v2)] += 1

    def next_expansive_fraction(self) -> float:
        return self.next_expansive_count / self.count if self.count else 0.0

    def avg_next_tail(self) -> float:
        return self.next_tail_sum / self.count if self.count else 0.0

    def avg_next_exit_v2(self) -> float:
        return self.next_exit_v2_sum / self.count if self.count else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Compare local exit_v2 transitions against the survivor-chain sample used "
            "in the high-exit experiment."
        )
    )
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--targets", default="1,2,3,4,5,6,7,8")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="exit_v2_selection_limit_5000000")
    return parser.parse_args()


def parse_targets(raw: str) -> set[int]:
    targets = {int(part.strip()) for part in raw.split(",") if part.strip()}
    if not targets:
        raise ValueError("at least one target exit_v2 is required")
    if any(target < 1 for target in targets):
        raise ValueError("target exit_v2 values must be positive")
    return targets


def is_expansive(block: AlternatingBlock) -> bool:
    return block.next_odd > block.n


def expands_from_tail_exit(tail: int, exit_v2: int) -> bool:
    return 3**tail > 2 ** (tail + exit_v2)


def geometric_probability(value: int) -> float:
    return 2.0 ** (-value)


def geometric_expansion_probability(max_value: int = 80) -> float:
    return sum(
        geometric_probability(tail) * geometric_probability(exit_v2)
        for tail in range(1, max_value + 1)
        for exit_v2 in range(1, max_value + 1)
        if expands_from_tail_exit(tail, exit_v2)
    )


def get_stats(
    stats: dict[tuple[str, int], TransitionStats],
    source: str,
    prev_exit_v2: int,
) -> TransitionStats:
    key = (source, prev_exit_v2)
    if key not in stats:
        stats[key] = TransitionStats(source=source, prev_exit_v2=prev_exit_v2)
    return stats[key]


def collect_local_transitions(limit: int, targets: set[int]) -> dict[tuple[str, int], TransitionStats]:
    stats: dict[tuple[str, int], TransitionStats] = {}

    for n in range(3, limit + 1, 2):
        previous = alternating_block(n)
        if previous.exit_v2 not in targets:
            continue
        next_block = alternating_block(previous.next_odd)
        get_stats(stats, "local_all_starts", previous.exit_v2).add(next_block)

    return stats


def collect_survivor_chain_transitions(
    limit: int,
    targets: set[int],
    max_blocks: int,
) -> dict[tuple[str, int], TransitionStats]:
    stats: dict[tuple[str, int], TransitionStats] = {}

    for n in range(3, limit + 1, 2):
        current = n
        previous: AlternatingBlock | None = None

        for _ in range(max_blocks):
            block = alternating_block(current)
            if previous is not None and previous.exit_v2 in targets:
                get_stats(stats, "chain_before_descent", previous.exit_v2).add(block)

            current = block.next_odd
            if current == 1 or current < n:
                break

            previous = block

    return stats


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def summary_rows(stats: dict[tuple[str, int], TransitionStats]) -> list[dict[str, object]]:
    geometric_expansion = geometric_expansion_probability()
    rows = []
    for stat in sorted(stats.values(), key=lambda item: (item.prev_exit_v2, item.source)):
        rows.append(
            {
                "source": stat.source,
                "prev_exit_v2": stat.prev_exit_v2,
                "count": stat.count,
                "next_expansive_count": stat.next_expansive_count,
                "next_expansive_fraction": round(stat.next_expansive_fraction(), 8),
                "geometric_expansive_fraction": round(geometric_expansion, 8),
                "diff_vs_geometric": round(stat.next_expansive_fraction() - geometric_expansion, 8),
                "avg_next_tail": round(stat.avg_next_tail(), 8),
                "avg_next_exit_v2": round(stat.avg_next_exit_v2(), 8),
            }
        )
    return rows


def distribution_rows(
    stats: dict[tuple[str, int], TransitionStats],
    *,
    kind: str,
) -> list[dict[str, object]]:
    rows = []
    for stat in sorted(stats.values(), key=lambda item: (item.prev_exit_v2, item.source)):
        counts = stat.tail_counts if kind == "tail" else stat.exit_counts
        for value in sorted(counts):
            fraction = counts[value] / stat.count if stat.count else 0.0
            rows.append(
                {
                    "source": stat.source,
                    "prev_exit_v2": stat.prev_exit_v2,
                    f"next_{kind}": value,
                    "count": counts[value],
                    "fraction": round(fraction, 8),
                    "geometric_fraction": round(geometric_probability(value), 8),
                    "diff_vs_geometric": round(fraction - geometric_probability(value), 8),
                }
            )
    return rows


def decomposition_rows(stats: dict[tuple[str, int], TransitionStats]) -> list[dict[str, object]]:
    geometric_expansion = geometric_expansion_probability()
    rows = []

    for stat in sorted(stats.values(), key=lambda item: (item.prev_exit_v2, item.source)):
        if not stat.count:
            continue

        tail_probs = {tail: count / stat.count for tail, count in stat.tail_counts.items()}
        exit_probs = {exit_v2: count / stat.count for exit_v2, count in stat.exit_counts.items()}
        joint_expansion = sum(
            count / stat.count
            for (tail, exit_v2), count in stat.joint_counts.items()
            if expands_from_tail_exit(tail, exit_v2)
        )
        observed_tail_geometric_exit = sum(
            tail_prob * geometric_probability(exit_v2)
            for tail, tail_prob in tail_probs.items()
            for exit_v2 in range(1, 81)
            if expands_from_tail_exit(tail, exit_v2)
        )
        geometric_tail_observed_exit = sum(
            geometric_probability(tail) * exit_prob
            for tail in range(1, 81)
            for exit_v2, exit_prob in exit_probs.items()
            if expands_from_tail_exit(tail, exit_v2)
        )
        observed_marginal_product = sum(
            tail_prob * exit_prob
            for tail, tail_prob in tail_probs.items()
            for exit_v2, exit_prob in exit_probs.items()
            if expands_from_tail_exit(tail, exit_v2)
        )

        rows.append(
            {
                "source": stat.source,
                "prev_exit_v2": stat.prev_exit_v2,
                "actual_expansive_fraction": round(stat.next_expansive_fraction(), 8),
                "joint_tail_exit_fraction": round(joint_expansion, 8),
                "geometric_independent_fraction": round(geometric_expansion, 8),
                "observed_tail_geometric_exit": round(observed_tail_geometric_exit, 8),
                "geometric_tail_observed_exit": round(geometric_tail_observed_exit, 8),
                "observed_marginal_product": round(observed_marginal_product, 8),
            }
        )

    return rows


def main() -> None:
    args = parse_args()
    targets = parse_targets(args.targets)

    stats = {}
    stats.update(collect_local_transitions(args.limit, targets))
    stats.update(collect_survivor_chain_transitions(args.limit, targets, args.max_blocks))

    args.out_dir.mkdir(parents=True, exist_ok=True)
    summary_path = args.out_dir / f"{args.prefix}_summary.csv"
    tail_path = args.out_dir / f"{args.prefix}_tail_distribution.csv"
    exit_path = args.out_dir / f"{args.prefix}_exit_distribution.csv"
    decomposition_path = args.out_dir / f"{args.prefix}_decomposition.csv"

    write_csv(
        summary_rows(stats),
        summary_path,
        [
            "source",
            "prev_exit_v2",
            "count",
            "next_expansive_count",
            "next_expansive_fraction",
            "geometric_expansive_fraction",
            "diff_vs_geometric",
            "avg_next_tail",
            "avg_next_exit_v2",
        ],
    )
    write_csv(
        distribution_rows(stats, kind="tail"),
        tail_path,
        [
            "source",
            "prev_exit_v2",
            "next_tail",
            "count",
            "fraction",
            "geometric_fraction",
            "diff_vs_geometric",
        ],
    )
    write_csv(
        distribution_rows(stats, kind="exit_v2"),
        exit_path,
        [
            "source",
            "prev_exit_v2",
            "next_exit_v2",
            "count",
            "fraction",
            "geometric_fraction",
            "diff_vs_geometric",
        ],
    )
    write_csv(
        decomposition_rows(stats),
        decomposition_path,
        [
            "source",
            "prev_exit_v2",
            "actual_expansive_fraction",
            "joint_tail_exit_fraction",
            "geometric_independent_fraction",
            "observed_tail_geometric_exit",
            "geometric_tail_observed_exit",
            "observed_marginal_product",
        ],
    )

    print(f"limit={args.limit}")
    print(f"targets={','.join(str(target) for target in sorted(targets))}")
    print(f"summary={summary_path}")
    print(f"tail_distribution={tail_path}")
    print(f"exit_distribution={exit_path}")
    print(f"decomposition={decomposition_path}")

    for row in summary_rows(stats):
        if row["prev_exit_v2"] == 5:
            print(
                row["source"],
                "prev_exit_v2=5",
                f"count={row['count']}",
                f"next_expansive_fraction={row['next_expansive_fraction']}",
                f"diff_vs_geometric={row['diff_vs_geometric']}",
                f"avg_next_tail={row['avg_next_tail']}",
                f"avg_next_exit_v2={row['avg_next_exit_v2']}",
            )


if __name__ == "__main__":
    main()
