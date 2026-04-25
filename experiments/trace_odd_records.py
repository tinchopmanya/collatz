from __future__ import annotations

import argparse
import csv
import math
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block, mersenne_tail_length  # noqa: E402


DEFAULT_STARTS = [
    626331,
    667375,
    704623,
    159487,
    270271,
    288615,
    704511,
    405407,
]


@dataclass(frozen=True)
class TraceSummary:
    n: int
    status: str
    blocks: int
    compressed_steps: int
    expansive_blocks: int
    max_tail_seen: int
    max_odd: int
    max_peak: int
    terminal_odd: int
    max_odd_ratio: float
    max_peak_ratio: float
    final_log_ratio: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Trace selected Collatz odd-to-odd record chains."
    )
    parser.add_argument(
        "--starts",
        nargs="*",
        type=int,
        default=DEFAULT_STARTS,
        help="Odd starting values to trace.",
    )
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="odd_record_traces")
    return parser.parse_args()


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def trace_start(n: int, max_blocks: int) -> tuple[TraceSummary, list[dict[str, object]]]:
    if n < 1 or n % 2 == 0:
        raise ValueError("all starts must be positive odd integers")
    if max_blocks < 1:
        raise ValueError("max_blocks must be positive")

    current = n
    max_odd = n
    max_peak = n
    max_tail_seen = mersenne_tail_length(n)
    compressed_steps = 0
    expansive_blocks = 0
    cumulative_log = 0.0
    rows: list[dict[str, object]] = []

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        next_odd = block.next_odd
        next_tail = mersenne_tail_length(next_odd)
        local_odd_ratio = next_odd / current
        cumulative_odd_ratio = next_odd / n
        local_peak_ratio = block.block_peak / current
        cumulative_peak_ratio = block.block_peak / n
        local_log = math.log(local_odd_ratio)

        compressed_steps += block.block_steps_to_next_odd
        cumulative_log += local_log
        max_odd = max(max_odd, next_odd)
        max_peak = max(max_peak, block.block_peak)
        max_tail_seen = max(max_tail_seen, next_tail)
        if next_odd > current:
            expansive_blocks += 1

        status_after = "continue"
        if next_odd == 1:
            status_after = "one"
        elif next_odd < n:
            status_after = "drop"

        rows.append(
            {
                "n": n,
                "block": block_index,
                "current_odd": current,
                "tail": block.tail_length,
                "odd_factor": block.odd_factor,
                "exit_v2": block.exit_v2,
                "next_odd": next_odd,
                "next_tail": next_tail,
                "steps_to_next_odd": block.block_steps_to_next_odd,
                "compressed_steps": compressed_steps,
                "local_odd_ratio": round(local_odd_ratio, 12),
                "cumulative_odd_ratio": round(cumulative_odd_ratio, 12),
                "local_peak_ratio": round(local_peak_ratio, 12),
                "cumulative_peak_ratio": round(cumulative_peak_ratio, 12),
                "local_log_ratio": round(local_log, 12),
                "cumulative_log_ratio": round(cumulative_log, 12),
                "status_after": status_after,
            }
        )

        current = next_odd
        if status_after != "continue":
            return (
                TraceSummary(
                    n=n,
                    status=status_after,
                    blocks=block_index,
                    compressed_steps=compressed_steps,
                    expansive_blocks=expansive_blocks,
                    max_tail_seen=max_tail_seen,
                    max_odd=max_odd,
                    max_peak=max_peak,
                    terminal_odd=current,
                    max_odd_ratio=max_odd / n,
                    max_peak_ratio=max_peak / n,
                    final_log_ratio=cumulative_log,
                ),
                rows,
            )

    return (
        TraceSummary(
            n=n,
            status="maxed",
            blocks=max_blocks,
            compressed_steps=compressed_steps,
            expansive_blocks=expansive_blocks,
            max_tail_seen=max_tail_seen,
            max_odd=max_odd,
            max_peak=max_peak,
            terminal_odd=current,
            max_odd_ratio=max_odd / n,
            max_peak_ratio=max_peak / n,
            final_log_ratio=cumulative_log,
        ),
        rows,
    )


def main() -> int:
    args = parse_args()
    trace_rows: list[dict[str, object]] = []
    summary_rows: list[dict[str, object]] = []

    for n in args.starts:
        summary, rows = trace_start(n, args.max_blocks)
        trace_rows.extend(rows)
        summary_rows.append(
            {
                "n": summary.n,
                "status": summary.status,
                "blocks": summary.blocks,
                "compressed_steps": summary.compressed_steps,
                "expansive_blocks": summary.expansive_blocks,
                "max_tail_seen": summary.max_tail_seen,
                "max_odd": summary.max_odd,
                "max_peak": summary.max_peak,
                "terminal_odd": summary.terminal_odd,
                "max_odd_ratio": round(summary.max_odd_ratio, 6),
                "max_peak_ratio": round(summary.max_peak_ratio, 6),
                "final_log_ratio": round(summary.final_log_ratio, 12),
            }
        )

    trace_path = args.out_dir / f"{args.prefix}.csv"
    summary_path = args.out_dir / f"{args.prefix}_summary.csv"

    write_csv(
        trace_rows,
        trace_path,
        [
            "n",
            "block",
            "current_odd",
            "tail",
            "odd_factor",
            "exit_v2",
            "next_odd",
            "next_tail",
            "steps_to_next_odd",
            "compressed_steps",
            "local_odd_ratio",
            "cumulative_odd_ratio",
            "local_peak_ratio",
            "cumulative_peak_ratio",
            "local_log_ratio",
            "cumulative_log_ratio",
            "status_after",
        ],
    )
    write_csv(
        summary_rows,
        summary_path,
        [
            "n",
            "status",
            "blocks",
            "compressed_steps",
            "expansive_blocks",
            "max_tail_seen",
            "max_odd",
            "max_peak",
            "terminal_odd",
            "max_odd_ratio",
            "max_peak_ratio",
            "final_log_ratio",
        ],
    )

    print(f"traces={trace_path}")
    print(f"summary={summary_path}")
    for row in summary_rows:
        print(
            f"n={row['n']} blocks={row['blocks']} "
            f"max_peak_ratio={row['max_peak_ratio']} terminal={row['terminal_odd']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
