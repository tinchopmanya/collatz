from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import classic_step, compute_metrics  # noqa: E402


@dataclass
class AlternatingStats:
    residue: int
    count: int = 0
    alternating_sum: int = 0
    max_alternating_len: int = -1
    argmax_alternating_len: int = -1
    early_peak_ratio_sum: float = 0.0
    max_early_peak_ratio: float = -1.0
    argmax_early_peak_ratio: int = -1
    avg_total_steps_sum: int = 0
    avg_stopping_time_sum: int = 0
    stopping_time_count: int = 0

    def add(
        self,
        *,
        n: int,
        alternating_len: int,
        early_peak_ratio: float,
        total_steps: int,
        stopping_time: int | None,
    ) -> None:
        self.count += 1
        self.alternating_sum += alternating_len
        self.early_peak_ratio_sum += early_peak_ratio
        self.avg_total_steps_sum += total_steps

        if stopping_time is not None:
            self.avg_stopping_time_sum += stopping_time
            self.stopping_time_count += 1

        if alternating_len > self.max_alternating_len:
            self.max_alternating_len = alternating_len
            self.argmax_alternating_len = n

        if early_peak_ratio > self.max_early_peak_ratio:
            self.max_early_peak_ratio = early_peak_ratio
            self.argmax_early_peak_ratio = n

    def as_row(self) -> dict[str, object]:
        if self.count == 0:
            return {
                "residue": self.residue,
                "count": 0,
                "avg_alternating_len": 0.0,
                "max_alternating_len": 0,
                "argmax_alternating_len": -1,
                "avg_early_peak_ratio": 0.0,
                "max_early_peak_ratio": 0.0,
                "argmax_early_peak_ratio": -1,
                "avg_total_steps": 0.0,
                "avg_stopping_time": 0.0,
            }

        avg_stopping_time = (
            self.avg_stopping_time_sum / self.stopping_time_count
            if self.stopping_time_count
            else 0.0
        )
        return {
            "residue": self.residue,
            "count": self.count,
            "avg_alternating_len": round(self.alternating_sum / self.count, 6),
            "max_alternating_len": self.max_alternating_len,
            "argmax_alternating_len": self.argmax_alternating_len,
            "avg_early_peak_ratio": round(self.early_peak_ratio_sum / self.count, 6),
            "max_early_peak_ratio": round(self.max_early_peak_ratio, 6),
            "argmax_early_peak_ratio": self.argmax_early_peak_ratio,
            "avg_total_steps": round(self.avg_total_steps_sum / self.count, 6),
            "avg_stopping_time": round(avg_stopping_time, 6),
        }


def parse_residues(raw: str) -> list[int]:
    residues = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not residues:
        raise ValueError("at least one residue is required")
    return residues


def alternating_prefix_len(n: int, *, max_len: int) -> int:
    current = n
    expected = current % 2
    length = 0

    for _ in range(max_len):
        if current % 2 != expected:
            break
        length += 1
        current = classic_step(current)
        expected = 1 - expected

    return length


def early_peak_ratio(n: int, *, window: int) -> float:
    current = n
    peak = n
    for _ in range(window):
        if current == 1:
            break
        current = classic_step(current)
        if current > peak:
            peak = current
    return peak / n


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure alternating parity prefixes and early excursions by residue."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--power", type=int, default=9)
    parser.add_argument(
        "--residues",
        default="511,510,255,254,127,126,447,283,167,155,1,0",
    )
    parser.add_argument("--max-prefix-len", type=int, default=128)
    parser.add_argument("--early-window", type=int, default=64)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/alternating_prefix_mod_512_limit_1000000.csv"),
    )
    parser.add_argument("--max-steps", type=int, default=100_000)
    return parser.parse_args()


def analyze(
    *,
    limit: int,
    power: int,
    residues: list[int],
    max_prefix_len: int,
    early_window: int,
    max_steps: int,
) -> list[dict[str, object]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if power < 1:
        raise ValueError("power must be positive")
    if max_prefix_len < 1:
        raise ValueError("max-prefix-len must be positive")
    if early_window < 1:
        raise ValueError("early-window must be positive")

    modulus = 2**power
    residue_set = {residue % modulus for residue in residues}
    stats = {residue: AlternatingStats(residue=residue) for residue in sorted(residue_set)}

    for n in range(1, limit + 1):
        residue = n % modulus
        if residue not in stats:
            continue

        metrics = compute_metrics(n, max_steps=max_steps, parity_prefix_len=0)
        if not metrics.reached_one:
            raise RuntimeError(f"{n} did not reach 1 within {max_steps} steps")

        stats[residue].add(
            n=n,
            alternating_len=alternating_prefix_len(n, max_len=max_prefix_len),
            early_peak_ratio=early_peak_ratio(n, window=early_window),
            total_steps=metrics.total_steps,
            stopping_time=metrics.stopping_time,
        )

    return [stats[residue].as_row() for residue in sorted(stats)]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "residue",
        "count",
        "avg_alternating_len",
        "max_alternating_len",
        "argmax_alternating_len",
        "avg_early_peak_ratio",
        "max_early_peak_ratio",
        "argmax_early_peak_ratio",
        "avg_total_steps",
        "avg_stopping_time",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    rows = analyze(
        limit=args.limit,
        power=args.power,
        residues=parse_residues(args.residues),
        max_prefix_len=args.max_prefix_len,
        early_window=args.early_window,
        max_steps=args.max_steps,
    )
    write_csv(rows, args.out)

    print(
        f"modulus={2**args.power} limit={args.limit} "
        f"max_prefix_len={args.max_prefix_len} early_window={args.early_window}"
    )
    for row in sorted(rows, key=lambda item: item["avg_alternating_len"], reverse=True):
        print(
            f"residue={row['residue']} count={row['count']} "
            f"avg_alt={row['avg_alternating_len']} "
            f"avg_peak={row['avg_early_peak_ratio']} "
            f"avg_steps={row['avg_total_steps']} "
            f"avg_stop={row['avg_stopping_time']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
