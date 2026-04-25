from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import CollatzMetrics, compute_metrics  # noqa: E402


@dataclass
class ResidueStats:
    residue: int
    count: int = 0
    total_steps_sum: int = 0
    stopping_time_sum: int = 0
    stopping_time_count: int = 0
    max_total_steps: int = -1
    argmax_total_steps: int = -1
    max_stopping_time: int = -1
    argmax_stopping_time: int = -1
    max_value: int = -1
    argmax_max_value: int = -1

    def add(self, metrics: CollatzMetrics) -> None:
        self.count += 1
        self.total_steps_sum += metrics.total_steps

        if metrics.stopping_time is not None:
            self.stopping_time_sum += metrics.stopping_time
            self.stopping_time_count += 1
            if metrics.stopping_time > self.max_stopping_time:
                self.max_stopping_time = metrics.stopping_time
                self.argmax_stopping_time = metrics.n

        if metrics.total_steps > self.max_total_steps:
            self.max_total_steps = metrics.total_steps
            self.argmax_total_steps = metrics.n

        if metrics.max_value > self.max_value:
            self.max_value = metrics.max_value
            self.argmax_max_value = metrics.n

    def as_row(self) -> dict[str, object]:
        avg_total_steps = self.total_steps_sum / self.count if self.count else 0.0
        avg_stopping_time = (
            self.stopping_time_sum / self.stopping_time_count
            if self.stopping_time_count
            else 0.0
        )
        return {
            "residue": self.residue,
            "count": self.count,
            "avg_total_steps": round(avg_total_steps, 6),
            "avg_stopping_time": round(avg_stopping_time, 6),
            "max_total_steps": self.max_total_steps,
            "argmax_total_steps": self.argmax_total_steps,
            "max_stopping_time": self.max_stopping_time,
            "argmax_stopping_time": self.argmax_stopping_time,
            "max_value": self.max_value,
            "argmax_max_value": self.argmax_max_value,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Aggregate Collatz metrics by residue class modulo 2^k."
    )
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--power", type=int, default=7)
    parser.add_argument("--out", type=Path, default=Path("reports/residue_mod_128_limit_100000.csv"))
    parser.add_argument("--max-steps", type=int, default=100_000)
    return parser.parse_args()


def analyze(limit: int, power: int, max_steps: int) -> list[dict[str, object]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if power < 1:
        raise ValueError("power must be positive")

    modulus = 2**power
    buckets = [ResidueStats(residue=i) for i in range(modulus)]

    for n in range(1, limit + 1):
        metrics = compute_metrics(n, max_steps=max_steps, parity_prefix_len=0)
        if not metrics.reached_one:
            raise RuntimeError(f"{n} did not reach 1 within {max_steps} steps")
        buckets[n % modulus].add(metrics)

    return [bucket.as_row() for bucket in buckets]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "residue",
        "count",
        "avg_total_steps",
        "avg_stopping_time",
        "max_total_steps",
        "argmax_total_steps",
        "max_stopping_time",
        "argmax_stopping_time",
        "max_value",
        "argmax_max_value",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    rows = analyze(args.limit, args.power, args.max_steps)
    write_csv(rows, args.out)

    top_total = max(rows, key=lambda row: row["max_total_steps"])
    top_stop = max(rows, key=lambda row: row["max_stopping_time"])
    top_height = max(rows, key=lambda row: row["max_value"])

    modulus = 2**args.power
    print(f"modulus={modulus} limit={args.limit}")
    print(
        f"top_total: residue={top_total['residue']} "
        f"n={top_total['argmax_total_steps']} steps={top_total['max_total_steps']}"
    )
    print(
        f"top_stop: residue={top_stop['residue']} "
        f"n={top_stop['argmax_stopping_time']} stop={top_stop['max_stopping_time']}"
    )
    print(
        f"top_height: residue={top_height['residue']} "
        f"n={top_height['argmax_max_value']} max={top_height['max_value']}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
