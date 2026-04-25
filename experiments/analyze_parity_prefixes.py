from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import compute_metrics  # noqa: E402


@dataclass
class PrefixStats:
    residue: int
    count: int = 0
    total_steps_sum: int = 0
    stopping_time_sum: int = 0
    stopping_time_count: int = 0
    max_value_sum: int = 0
    odd_counts: list[int] | None = None

    def ensure_width(self, width: int) -> None:
        if self.odd_counts is None:
            self.odd_counts = [0] * width

    def add(self, n: int, modulus: int, prefix_len: int, max_steps: int) -> None:
        self.ensure_width(prefix_len)
        metrics = compute_metrics(
            n,
            max_steps=max_steps,
            parity_prefix_len=prefix_len,
        )
        if not metrics.reached_one:
            raise RuntimeError(f"{n} did not reach 1 within {max_steps} steps")

        self.count += 1
        self.total_steps_sum += metrics.total_steps
        self.max_value_sum += metrics.max_value
        if metrics.stopping_time is not None:
            self.stopping_time_sum += metrics.stopping_time
            self.stopping_time_count += 1

        assert self.odd_counts is not None
        for index, bit in enumerate(metrics.parity_prefix):
            if bit == "1":
                self.odd_counts[index] += 1

    def as_row(self) -> dict[str, object]:
        if not self.count:
            return {
                "residue": self.residue,
                "count": 0,
                "avg_total_steps": 0.0,
                "avg_stopping_time": 0.0,
                "avg_max_value": 0.0,
                "prefix_odd_rates": "",
                "first_16_odd_rate": 0.0,
                "first_32_odd_rate": 0.0,
            }

        odd_counts = self.odd_counts or []
        rates = [count / self.count for count in odd_counts]
        first_16 = sum(rates[:16]) / min(16, len(rates)) if rates else 0.0
        first_32 = sum(rates[:32]) / min(32, len(rates)) if rates else 0.0
        avg_stopping_time = (
            self.stopping_time_sum / self.stopping_time_count
            if self.stopping_time_count
            else 0.0
        )
        return {
            "residue": self.residue,
            "count": self.count,
            "avg_total_steps": round(self.total_steps_sum / self.count, 6),
            "avg_stopping_time": round(avg_stopping_time, 6),
            "avg_max_value": round(self.max_value_sum / self.count, 6),
            "prefix_odd_rates": " ".join(f"{rate:.6f}" for rate in rates),
            "first_16_odd_rate": round(first_16, 6),
            "first_32_odd_rate": round(first_32, 6),
        }


def parse_residues(raw: str) -> list[int]:
    residues = [int(part.strip()) for part in raw.split(",") if part.strip()]
    if not residues:
        raise ValueError("at least one residue is required")
    return residues


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare Collatz parity prefixes for selected residue classes."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--power", type=int, default=9)
    parser.add_argument(
        "--residues",
        default="511,510,255,254,127,126,447,283,167,155,1,0",
    )
    parser.add_argument("--prefix-len", type=int, default=64)
    parser.add_argument(
        "--out",
        type=Path,
        default=Path("reports/parity_prefix_mod_512_limit_1000000.csv"),
    )
    parser.add_argument("--max-steps", type=int, default=100_000)
    return parser.parse_args()


def analyze(
    *,
    limit: int,
    power: int,
    residues: list[int],
    prefix_len: int,
    max_steps: int,
) -> list[dict[str, object]]:
    if limit < 1:
        raise ValueError("limit must be positive")
    if power < 1:
        raise ValueError("power must be positive")
    if prefix_len < 1:
        raise ValueError("prefix-len must be positive")

    modulus = 2**power
    residue_set = {residue % modulus for residue in residues}
    stats = {residue: PrefixStats(residue=residue) for residue in sorted(residue_set)}

    for n in range(1, limit + 1):
        residue = n % modulus
        if residue in stats:
            stats[residue].add(n, modulus, prefix_len, max_steps)

    return [stats[residue].as_row() for residue in sorted(stats)]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "residue",
        "count",
        "avg_total_steps",
        "avg_stopping_time",
        "avg_max_value",
        "first_16_odd_rate",
        "first_32_odd_rate",
        "prefix_odd_rates",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    args = parse_args()
    residues = parse_residues(args.residues)
    rows = analyze(
        limit=args.limit,
        power=args.power,
        residues=residues,
        prefix_len=args.prefix_len,
        max_steps=args.max_steps,
    )
    write_csv(rows, args.out)

    print(f"modulus={2**args.power} limit={args.limit} prefix_len={args.prefix_len}")
    for row in sorted(rows, key=lambda item: item["first_32_odd_rate"], reverse=True):
        print(
            f"residue={row['residue']} count={row['count']} "
            f"first32_odd={row['first_32_odd_rate']} "
            f"avg_steps={row['avg_total_steps']} "
            f"avg_stop={row['avg_stopping_time']}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
