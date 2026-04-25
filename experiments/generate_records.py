from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import CollatzMetrics, compute_metrics  # noqa: E402


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate Collatz record tables for a bounded range."
    )
    parser.add_argument("--limit", type=int, default=100_000)
    parser.add_argument("--out", type=Path, default=Path("reports/records_limit_100000.csv"))
    parser.add_argument("--max-steps", type=int, default=100_000)
    return parser.parse_args()


def update_record(
    records: dict[str, CollatzMetrics],
    key: str,
    candidate: CollatzMetrics,
    value: int,
) -> None:
    current = records.get(key)
    if current is None:
        records[key] = candidate
        return

    current_value = getattr(current, key)
    if value > current_value or (value == current_value and candidate.n < current.n):
        records[key] = candidate


def generate_records(limit: int, max_steps: int) -> list[dict[str, object]]:
    if limit < 1:
        raise ValueError("limit must be positive")

    records: dict[str, CollatzMetrics] = {}
    rows: list[dict[str, object]] = []

    for n in range(1, limit + 1):
        metrics = compute_metrics(n, max_steps=max_steps, parity_prefix_len=64)
        if not metrics.reached_one:
            raise RuntimeError(f"{n} did not reach 1 within {max_steps} steps")

        update_record(records, "total_steps", metrics, metrics.total_steps)
        update_record(records, "max_value", metrics, metrics.max_value)
        stopping_value = metrics.stopping_time if metrics.stopping_time is not None else -1
        current = records.get("stopping_time")
        current_value = (
            current.stopping_time if current is not None and current.stopping_time is not None else -1
        )
        if current is None or stopping_value > current_value:
            records["stopping_time"] = metrics

    for metric_name in ("total_steps", "stopping_time", "max_value"):
        metrics = records[metric_name]
        row = asdict(metrics)
        row["record_type"] = metric_name
        rows.append(row)

    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "record_type",
        "n",
        "total_steps",
        "stopping_time",
        "max_value",
        "odd_steps",
        "even_steps",
        "parity_prefix",
        "reached_one",
        "terminal_value",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    rows = generate_records(args.limit, args.max_steps)
    write_csv(rows, args.out)
    for row in rows:
        print(
            f"{row['record_type']}: n={row['n']} "
            f"steps={row['total_steps']} stop={row['stopping_time']} max={row['max_value']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
