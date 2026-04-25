from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block, mersenne_tail_length  # noqa: E402


@dataclass
class TailStats:
    tail_length: int
    count: int = 0
    exit_v2_sum: int = 0
    next_tail_sum: int = 0
    peak_ratio_sum: float = 0.0
    next_odd_ratio_sum: float = 0.0
    growth_count: int = 0
    max_exit_v2: int = -1
    argmax_exit_v2: int = -1
    max_next_tail: int = -1
    argmax_next_tail: int = -1
    max_peak_ratio: float = -1.0
    argmax_peak_ratio: int = -1

    def add(
        self,
        *,
        n: int,
        exit_v2: int,
        next_tail: int,
        peak_ratio: float,
        next_odd_ratio: float,
        grows: bool,
    ) -> None:
        self.count += 1
        self.exit_v2_sum += exit_v2
        self.next_tail_sum += next_tail
        self.peak_ratio_sum += peak_ratio
        self.next_odd_ratio_sum += next_odd_ratio
        if grows:
            self.growth_count += 1

        if exit_v2 > self.max_exit_v2:
            self.max_exit_v2 = exit_v2
            self.argmax_exit_v2 = n

        if next_tail > self.max_next_tail:
            self.max_next_tail = next_tail
            self.argmax_next_tail = n

        if peak_ratio > self.max_peak_ratio:
            self.max_peak_ratio = peak_ratio
            self.argmax_peak_ratio = n

    def as_row(self) -> dict[str, object]:
        if self.count == 0:
            return {
                "tail_length": self.tail_length,
                "count": 0,
                "avg_exit_v2": 0.0,
                "avg_next_tail": 0.0,
                "growth_fraction": 0.0,
                "avg_peak_ratio": 0.0,
                "avg_next_odd_ratio": 0.0,
                "max_exit_v2": 0,
                "argmax_exit_v2": -1,
                "max_next_tail": 0,
                "argmax_next_tail": -1,
                "max_peak_ratio": 0.0,
                "argmax_peak_ratio": -1,
            }

        return {
            "tail_length": self.tail_length,
            "count": self.count,
            "avg_exit_v2": round(self.exit_v2_sum / self.count, 6),
            "avg_next_tail": round(self.next_tail_sum / self.count, 6),
            "growth_fraction": round(self.growth_count / self.count, 6),
            "avg_peak_ratio": round(self.peak_ratio_sum / self.count, 6),
            "avg_next_odd_ratio": round(self.next_odd_ratio_sum / self.count, 6),
            "max_exit_v2": self.max_exit_v2,
            "argmax_exit_v2": self.argmax_exit_v2,
            "max_next_tail": self.max_next_tail,
            "argmax_next_tail": self.argmax_next_tail,
            "max_peak_ratio": round(self.max_peak_ratio, 6),
            "argmax_peak_ratio": self.argmax_peak_ratio,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze the exit map after the initial alternating Collatz block."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="exit_map_limit_1000000")
    return parser.parse_args()


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyze(limit: int) -> tuple[list[dict[str, object]], list[dict[str, object]], list[dict[str, object]]]:
    if limit < 1:
        raise ValueError("limit must be positive")

    by_tail: dict[int, TailStats] = {}
    exit_v2_counts: Counter[int] = Counter()
    transitions: Counter[tuple[int, int]] = Counter()

    for n in range(1, limit + 1, 2):
        block = alternating_block(n)
        next_tail = mersenne_tail_length(block.next_odd)
        peak_ratio = block.block_peak / n
        next_odd_ratio = block.next_odd / n
        grows = block.next_odd > n

        stats = by_tail.setdefault(
            block.tail_length,
            TailStats(tail_length=block.tail_length),
        )
        stats.add(
            n=n,
            exit_v2=block.exit_v2,
            next_tail=next_tail,
            peak_ratio=peak_ratio,
            next_odd_ratio=next_odd_ratio,
            grows=grows,
        )
        exit_v2_counts[block.exit_v2] += 1
        transitions[(block.tail_length, next_tail)] += 1

    by_tail_rows = [by_tail[key].as_row() for key in sorted(by_tail)]
    total = sum(exit_v2_counts.values())
    exit_rows = [
        {
            "exit_v2": exit_v2,
            "count": count,
            "fraction": round(count / total, 8),
        }
        for exit_v2, count in sorted(exit_v2_counts.items())
    ]
    transition_rows = [
        {
            "tail_length": tail,
            "next_tail": next_tail,
            "count": count,
        }
        for (tail, next_tail), count in sorted(transitions.items())
    ]
    return by_tail_rows, exit_rows, transition_rows


def main() -> int:
    args = parse_args()
    by_tail_rows, exit_rows, transition_rows = analyze(args.limit)

    by_tail_path = args.out_dir / f"{args.prefix}_by_tail.csv"
    exit_path = args.out_dir / f"{args.prefix}_exit_v2.csv"
    transition_path = args.out_dir / f"{args.prefix}_transitions.csv"

    write_csv(
        by_tail_rows,
        by_tail_path,
        [
            "tail_length",
            "count",
            "avg_exit_v2",
            "avg_next_tail",
            "growth_fraction",
            "avg_peak_ratio",
            "avg_next_odd_ratio",
            "max_exit_v2",
            "argmax_exit_v2",
            "max_next_tail",
            "argmax_next_tail",
            "max_peak_ratio",
            "argmax_peak_ratio",
        ],
    )
    write_csv(exit_rows, exit_path, ["exit_v2", "count", "fraction"])
    write_csv(transition_rows, transition_path, ["tail_length", "next_tail", "count"])

    print(f"limit={args.limit}")
    print(f"by_tail={by_tail_path}")
    print(f"exit_v2={exit_path}")
    print(f"transitions={transition_path}")

    for row in by_tail_rows[:12]:
        print(
            f"s={row['tail_length']} count={row['count']} "
            f"avg_r={row['avg_exit_v2']} avg_next_s={row['avg_next_tail']} "
            f"growth={row['growth_fraction']} avg_next_ratio={row['avg_next_odd_ratio']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
