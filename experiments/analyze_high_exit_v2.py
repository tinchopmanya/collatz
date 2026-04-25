from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block  # noqa: E402


@dataclass(frozen=True)
class BlockSample:
    source: str
    chain_id: int
    block_index: int
    tail: int
    exit_v2: int
    local_log: float
    cumulative_log: float
    expansive: bool


@dataclass
class ConditionalStats:
    source: str
    condition: str
    count: int = 0
    next_expansive_count: int = 0
    next_log_sum: float = 0.0
    next_log_sq_sum: float = 0.0
    next_tail_sum: int = 0
    next_tail_sq_sum: int = 0
    next_exit_v2_sum: int = 0
    next_exit_v2_sq_sum: int = 0

    def add(self, next_block: BlockSample) -> None:
        self.count += 1
        if next_block.expansive:
            self.next_expansive_count += 1
        self.next_log_sum += next_block.local_log
        self.next_log_sq_sum += next_block.local_log**2
        self.next_tail_sum += next_block.tail
        self.next_tail_sq_sum += next_block.tail**2
        self.next_exit_v2_sum += next_block.exit_v2
        self.next_exit_v2_sq_sum += next_block.exit_v2**2

    def mean_log(self) -> float:
        return self.next_log_sum / self.count if self.count else 0.0

    def mean_tail(self) -> float:
        return self.next_tail_sum / self.count if self.count else 0.0

    def mean_exit_v2(self) -> float:
        return self.next_exit_v2_sum / self.count if self.count else 0.0

    def next_expansive_fraction(self) -> float:
        return self.next_expansive_count / self.count if self.count else 0.0

    def standard_error(self, metric: str) -> float:
        if self.count < 2:
            return 0.0

        if metric == "next_log":
            total = self.next_log_sum
            sq_total = self.next_log_sq_sum
        elif metric == "next_tail":
            total = float(self.next_tail_sum)
            sq_total = float(self.next_tail_sq_sum)
        elif metric == "next_exit_v2":
            total = float(self.next_exit_v2_sum)
            sq_total = float(self.next_exit_v2_sq_sum)
        else:
            raise ValueError(f"unknown metric {metric}")

        mean = total / self.count
        variance = max(0.0, (sq_total - self.count * mean**2) / (self.count - 1))
        return math.sqrt(variance / self.count)

    def as_row(self) -> dict[str, object]:
        p = self.next_expansive_fraction()
        p_se = math.sqrt(p * (1.0 - p) / self.count) if self.count else 0.0
        return {
            "source": self.source,
            "condition": self.condition,
            "count": self.count,
            "next_expansive_count": self.next_expansive_count,
            "next_expansive_fraction": round(p, 8),
            "next_expansive_se": round(p_se, 10),
            "avg_next_log": round(self.mean_log(), 12),
            "avg_next_log_se": round(self.standard_error("next_log"), 12),
            "avg_next_tail": round(self.mean_tail(), 8),
            "avg_next_tail_se": round(self.standard_error("next_tail"), 10),
            "avg_next_exit_v2": round(self.mean_exit_v2(), 8),
            "avg_next_exit_v2_se": round(self.standard_error("next_exit_v2"), 10),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze whether high exit_v2 blocks bias the following Collatz odd-to-odd block."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--max-threshold", type=int, default=12)
    parser.add_argument("--max-exact", type=int, default=12)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="high_exit_v2_limit_1000000")
    return parser.parse_args()


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def sample_geometric_half(rng: random.Random) -> int:
    value = 1
    while rng.random() < 0.5:
        value += 1
    return value


def real_blocks_for_start(n: int, max_blocks: int) -> list[BlockSample]:
    current = n
    cumulative_log = 0.0
    blocks: list[BlockSample] = []

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        next_odd = block.next_odd
        local_log = math.log(next_odd / current)
        cumulative_log += local_log
        blocks.append(
            BlockSample(
                source="real",
                chain_id=n,
                block_index=block_index,
                tail=block.tail_length,
                exit_v2=block.exit_v2,
                local_log=local_log,
                cumulative_log=cumulative_log,
                expansive=local_log > 0,
            )
        )

        current = next_odd
        if current == 1 or current < n:
            break

    return blocks


def model_blocks_for_sample(sample_id: int, *, max_blocks: int, rng: random.Random) -> list[BlockSample]:
    cumulative_log = 0.0
    blocks: list[BlockSample] = []
    log_three_halves = math.log(1.5)
    log_two = math.log(2.0)

    for block_index in range(1, max_blocks + 1):
        tail = sample_geometric_half(rng)
        exit_v2 = sample_geometric_half(rng)
        local_log = tail * log_three_halves - exit_v2 * log_two
        cumulative_log += local_log
        blocks.append(
            BlockSample(
                source="model",
                chain_id=sample_id,
                block_index=block_index,
                tail=tail,
                exit_v2=exit_v2,
                local_log=local_log,
                cumulative_log=cumulative_log,
                expansive=local_log > 0,
            )
        )

        if cumulative_log < 0:
            break

    return blocks


def paired_blocks(chains: list[list[BlockSample]]) -> list[tuple[BlockSample, BlockSample]]:
    pairs: list[tuple[BlockSample, BlockSample]] = []
    for blocks in chains:
        pairs.extend(zip(blocks, blocks[1:]))
    return pairs


def collect_stats(
    source: str,
    pairs: list[tuple[BlockSample, BlockSample]],
    *,
    max_threshold: int,
    max_exact: int,
) -> tuple[list[ConditionalStats], list[ConditionalStats]]:
    threshold_stats = [
        ConditionalStats(source=source, condition=f"prev_exit_v2_ge_{threshold}")
        for threshold in range(1, max_threshold + 1)
    ]
    exact_stats = [
        ConditionalStats(source=source, condition=f"prev_exit_v2_eq_{value}")
        for value in range(1, max_exact + 1)
    ]

    for previous, next_block in pairs:
        for index, threshold in enumerate(range(1, max_threshold + 1)):
            if previous.exit_v2 >= threshold:
                threshold_stats[index].add(next_block)

        if 1 <= previous.exit_v2 <= max_exact:
            exact_stats[previous.exit_v2 - 1].add(next_block)

    return threshold_stats, exact_stats


def diff_proportion_row(condition: str, real: ConditionalStats, model: ConditionalStats) -> dict[str, object]:
    real_p = real.next_expansive_fraction()
    model_p = model.next_expansive_fraction()
    diff = real_p - model_p
    se = 0.0
    if real.count and model.count:
        se = math.sqrt(
            real_p * (1.0 - real_p) / real.count
            + model_p * (1.0 - model_p) / model.count
        )
    z_score = diff / se if se else 0.0
    return {
        "condition": condition,
        "real_count": real.count,
        "model_count": model.count,
        "real_next_expansive_fraction": round(real_p, 8),
        "model_next_expansive_fraction": round(model_p, 8),
        "diff_real_minus_model": round(diff, 8),
        "diff_se": round(se, 10),
        "diff_z_score": round(z_score, 6),
        "diff_ci95_low": round(diff - 1.96 * se, 8),
        "diff_ci95_high": round(diff + 1.96 * se, 8),
        "real_avg_next_log": round(real.mean_log(), 12),
        "model_avg_next_log": round(model.mean_log(), 12),
        "diff_avg_next_log": round(real.mean_log() - model.mean_log(), 12),
        "real_avg_next_tail": round(real.mean_tail(), 8),
        "model_avg_next_tail": round(model.mean_tail(), 8),
        "diff_avg_next_tail": round(real.mean_tail() - model.mean_tail(), 8),
        "real_avg_next_exit_v2": round(real.mean_exit_v2(), 8),
        "model_avg_next_exit_v2": round(model.mean_exit_v2(), 8),
        "diff_avg_next_exit_v2": round(real.mean_exit_v2() - model.mean_exit_v2(), 8),
    }


def compare_stats(real_stats: list[ConditionalStats], model_stats: list[ConditionalStats]) -> list[dict[str, object]]:
    by_model = {stats.condition: stats for stats in model_stats}
    rows = []
    for real in real_stats:
        rows.append(diff_proportion_row(real.condition, real, by_model[real.condition]))
    return rows


def main() -> int:
    args = parse_args()
    if args.limit < 3:
        raise ValueError("limit must be at least 3")
    if args.max_blocks < 2:
        raise ValueError("max_blocks must be at least 2")
    if args.max_threshold < 1 or args.max_exact < 1:
        raise ValueError("max thresholds must be positive")

    sample_count = args.samples if args.samples is not None else (args.limit - 1) // 2
    rng = random.Random(args.seed)

    real_chains = [
        real_blocks_for_start(n, args.max_blocks)
        for n in range(3, args.limit + 1, 2)
    ]
    model_chains = [
        model_blocks_for_sample(sample_id, max_blocks=args.max_blocks, rng=rng)
        for sample_id in range(1, sample_count + 1)
    ]

    real_thresholds, real_exact = collect_stats(
        "real",
        paired_blocks(real_chains),
        max_threshold=args.max_threshold,
        max_exact=args.max_exact,
    )
    model_thresholds, model_exact = collect_stats(
        "model",
        paired_blocks(model_chains),
        max_threshold=args.max_threshold,
        max_exact=args.max_exact,
    )

    threshold_rows = [stats.as_row() for stats in real_thresholds + model_thresholds]
    exact_rows = [stats.as_row() for stats in real_exact + model_exact]
    threshold_compare_rows = compare_stats(real_thresholds, model_thresholds)
    exact_compare_rows = compare_stats(real_exact, model_exact)

    threshold_path = args.out_dir / f"{args.prefix}_thresholds.csv"
    exact_path = args.out_dir / f"{args.prefix}_exact.csv"
    threshold_compare_path = args.out_dir / f"{args.prefix}_threshold_compare.csv"
    exact_compare_path = args.out_dir / f"{args.prefix}_exact_compare.csv"

    stats_fields = [
        "source",
        "condition",
        "count",
        "next_expansive_count",
        "next_expansive_fraction",
        "next_expansive_se",
        "avg_next_log",
        "avg_next_log_se",
        "avg_next_tail",
        "avg_next_tail_se",
        "avg_next_exit_v2",
        "avg_next_exit_v2_se",
    ]
    compare_fields = [
        "condition",
        "real_count",
        "model_count",
        "real_next_expansive_fraction",
        "model_next_expansive_fraction",
        "diff_real_minus_model",
        "diff_se",
        "diff_z_score",
        "diff_ci95_low",
        "diff_ci95_high",
        "real_avg_next_log",
        "model_avg_next_log",
        "diff_avg_next_log",
        "real_avg_next_tail",
        "model_avg_next_tail",
        "diff_avg_next_tail",
        "real_avg_next_exit_v2",
        "model_avg_next_exit_v2",
        "diff_avg_next_exit_v2",
    ]

    write_csv(threshold_rows, threshold_path, stats_fields)
    write_csv(exact_rows, exact_path, stats_fields)
    write_csv(threshold_compare_rows, threshold_compare_path, compare_fields)
    write_csv(exact_compare_rows, exact_compare_path, compare_fields)

    print(f"limit={args.limit}")
    print(f"samples={sample_count}")
    print(f"seed={args.seed}")
    print(f"thresholds={threshold_path}")
    print(f"exact={exact_path}")
    print(f"threshold_compare={threshold_compare_path}")
    print(f"exact_compare={exact_compare_path}")
    for row in threshold_compare_rows[:8]:
        print(
            f"{row['condition']} real={row['real_next_expansive_fraction']} "
            f"model={row['model_next_expansive_fraction']} "
            f"diff={row['diff_real_minus_model']} z={row['diff_z_score']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
