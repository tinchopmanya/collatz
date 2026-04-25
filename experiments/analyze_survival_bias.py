from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block  # noqa: E402


@dataclass(frozen=True)
class ChainStep:
    block_index: int
    tail: int
    exit_v2: int
    local_log: float
    before_log: float
    after_log: float

    @property
    def expansive(self) -> bool:
        return self.local_log > 0.0


@dataclass
class BucketStats:
    source: str
    bucket: str
    count: int = 0
    tail_one_count: int = 0
    expansive_count: int = 0
    tail_sum: int = 0
    exit_v2_sum: int = 0
    local_log_sum: float = 0.0
    before_log_sum: float = 0.0
    after_log_sum: float = 0.0
    tail_counts: Counter[int] = field(default_factory=Counter)

    def add(self, step: ChainStep) -> None:
        self.count += 1
        if step.tail == 1:
            self.tail_one_count += 1
        if step.expansive:
            self.expansive_count += 1
        self.tail_sum += step.tail
        self.exit_v2_sum += step.exit_v2
        self.local_log_sum += step.local_log
        self.before_log_sum += step.before_log
        self.after_log_sum += step.after_log
        self.tail_counts[step.tail] += 1

    def fraction(self, value: int) -> float:
        return value / self.count if self.count else 0.0

    def mean(self, value: float) -> float:
        return value / self.count if self.count else 0.0

    def as_row(self) -> dict[str, object]:
        tail_one_fraction = self.fraction(self.tail_one_count)
        expansive_fraction = self.fraction(self.expansive_count)
        return {
            "source": self.source,
            "bucket": self.bucket,
            "count": self.count,
            "tail_one_fraction": round(tail_one_fraction, 8),
            "tail_one_diff_vs_geometric": round(tail_one_fraction - 0.5, 8),
            "expansive_fraction": round(expansive_fraction, 8),
            "avg_tail": round(self.mean(float(self.tail_sum)), 8),
            "avg_exit_v2": round(self.mean(float(self.exit_v2_sum)), 8),
            "avg_local_log": round(self.mean(self.local_log_sum), 12),
            "avg_before_log": round(self.mean(self.before_log_sum), 12),
            "avg_after_log": round(self.mean(self.after_log_sum), 12),
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Measure how survival before first descent biases Mersenne-block tails."
    )
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="survival_bias_limit_5000000")
    return parser.parse_args()


def sample_geometric_half(rng: random.Random) -> int:
    value = 1
    while rng.random() < 0.5:
        value += 1
    return value


def real_chain(start: int, max_blocks: int) -> list[ChainStep]:
    current = start
    before_log = 0.0
    steps: list[ChainStep] = []

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        next_odd = block.next_odd
        local_log = math.log(next_odd / current)
        after_log = before_log + local_log
        steps.append(
            ChainStep(
                block_index=block_index,
                tail=block.tail_length,
                exit_v2=block.exit_v2,
                local_log=local_log,
                before_log=before_log,
                after_log=after_log,
            )
        )

        current = next_odd
        if current == 1 or current < start:
            break
        before_log = after_log

    return steps


def model_chain(sample_id: int, max_blocks: int, rng: random.Random) -> list[ChainStep]:
    del sample_id
    before_log = 0.0
    steps: list[ChainStep] = []
    log_three_halves = math.log(1.5)
    log_two = math.log(2.0)

    for block_index in range(1, max_blocks + 1):
        tail = sample_geometric_half(rng)
        exit_v2 = sample_geometric_half(rng)
        local_log = tail * log_three_halves - exit_v2 * log_two
        after_log = before_log + local_log
        steps.append(
            ChainStep(
                block_index=block_index,
                tail=tail,
                exit_v2=exit_v2,
                local_log=local_log,
                before_log=before_log,
                after_log=after_log,
            )
        )

        if after_log < 0.0:
            break
        before_log = after_log

    return steps


def depth_bucket(block_index: int) -> str:
    if block_index <= 20:
        return f"depth_{block_index:02d}"
    return "depth_21_plus"


def duration_bucket(duration: int) -> str:
    if duration <= 10:
        return f"duration_{duration:02d}"
    if duration <= 20:
        return "duration_11_20"
    if duration <= 40:
        return "duration_21_40"
    return "duration_41_plus"


def margin_bucket(before_log: float) -> str:
    if before_log < 0.25:
        return "margin_0_0p25"
    if before_log < 0.5:
        return "margin_0p25_0p5"
    if before_log < 1.0:
        return "margin_0p5_1"
    if before_log < 2.0:
        return "margin_1_2"
    if before_log < 4.0:
        return "margin_2_4"
    return "margin_4_plus"


def position_bucket(step_index: int, duration: int) -> str:
    if duration == 1:
        return "only_block"
    if step_index == 1:
        return "first_block"
    if step_index == duration:
        return "final_block"
    return "interior_block"


def prev_exit_bucket(exit_v2: int) -> str:
    if exit_v2 <= 10:
        return f"prev_exit_v2_{exit_v2:02d}"
    return "prev_exit_v2_11_plus"


def get_bucket(stats: dict[tuple[str, str], BucketStats], source: str, bucket: str) -> BucketStats:
    key = (source, bucket)
    if key not in stats:
        stats[key] = BucketStats(source=source, bucket=bucket)
    return stats[key]


def add_chain_to_stats(
    source: str,
    steps: list[ChainStep],
    *,
    depth_stats: dict[tuple[str, str], BucketStats],
    margin_stats: dict[tuple[str, str], BucketStats],
    duration_stats: dict[tuple[str, str], BucketStats],
    position_stats: dict[tuple[str, str], BucketStats],
    prev_exit_stats: dict[tuple[str, str], BucketStats],
    prev_exit_position_stats: dict[tuple[str, str], BucketStats],
) -> None:
    duration = len(steps)
    duration_label = duration_bucket(duration)

    for index, step in enumerate(steps, start=1):
        get_bucket(depth_stats, source, depth_bucket(step.block_index)).add(step)
        get_bucket(margin_stats, source, margin_bucket(step.before_log)).add(step)
        get_bucket(duration_stats, source, duration_label).add(step)
        get_bucket(position_stats, source, position_bucket(index, duration)).add(step)

        if index > 1:
            previous = steps[index - 2]
            previous_exit_label = prev_exit_bucket(previous.exit_v2)
            current_position_label = position_bucket(index, duration)
            get_bucket(prev_exit_stats, source, previous_exit_label).add(step)
            get_bucket(
                prev_exit_position_stats,
                source,
                f"{previous_exit_label}__{current_position_label}",
            ).add(step)


def write_rows(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def stats_rows(stats: dict[tuple[str, str], BucketStats]) -> list[dict[str, object]]:
    return [stat.as_row() for stat in sorted(stats.values(), key=lambda item: (item.bucket, item.source))]


def binomial_diff(real_success: int, real_count: int, model_success: int, model_count: int) -> tuple[float, float, float, float, float]:
    real_fraction = real_success / real_count if real_count else 0.0
    model_fraction = model_success / model_count if model_count else 0.0
    diff = real_fraction - model_fraction
    se = (
        math.sqrt(
            real_fraction * (1.0 - real_fraction) / real_count
            + model_fraction * (1.0 - model_fraction) / model_count
        )
        if real_count and model_count
        else 0.0
    )
    z_score = diff / se if se else 0.0
    return diff, se, diff - 1.96 * se, diff + 1.96 * se, z_score


def compare_rows(stats: dict[tuple[str, str], BucketStats]) -> list[dict[str, object]]:
    rows = []
    buckets = sorted({bucket for _, bucket in stats})

    for bucket in buckets:
        real = stats.get(("real", bucket))
        model = stats.get(("model", bucket))
        if real is None or model is None:
            continue

        tail_diff, tail_se, tail_low, tail_high, tail_z = binomial_diff(
            real.tail_one_count,
            real.count,
            model.tail_one_count,
            model.count,
        )
        exp_diff, exp_se, exp_low, exp_high, exp_z = binomial_diff(
            real.expansive_count,
            real.count,
            model.expansive_count,
            model.count,
        )
        rows.append(
            {
                "bucket": bucket,
                "real_count": real.count,
                "model_count": model.count,
                "real_tail_one_fraction": round(real.fraction(real.tail_one_count), 8),
                "model_tail_one_fraction": round(model.fraction(model.tail_one_count), 8),
                "tail_one_diff_real_minus_model": round(tail_diff, 8),
                "tail_one_diff_se": round(tail_se, 10),
                "tail_one_diff_ci95_low": round(tail_low, 8),
                "tail_one_diff_ci95_high": round(tail_high, 8),
                "tail_one_diff_z": round(tail_z, 6),
                "real_expansive_fraction": round(real.fraction(real.expansive_count), 8),
                "model_expansive_fraction": round(model.fraction(model.expansive_count), 8),
                "expansive_diff_real_minus_model": round(exp_diff, 8),
                "expansive_diff_se": round(exp_se, 10),
                "expansive_diff_ci95_low": round(exp_low, 8),
                "expansive_diff_ci95_high": round(exp_high, 8),
                "expansive_diff_z": round(exp_z, 6),
                "real_avg_tail": round(real.mean(float(real.tail_sum)), 8),
                "model_avg_tail": round(model.mean(float(model.tail_sum)), 8),
                "avg_tail_diff_real_minus_model": round(
                    real.mean(float(real.tail_sum)) - model.mean(float(model.tail_sum)),
                    8,
                ),
            }
        )

    return rows


def tail_distribution_rows(stats: dict[tuple[str, str], BucketStats]) -> list[dict[str, object]]:
    rows = []
    for stat in sorted(stats.values(), key=lambda item: (item.bucket, item.source)):
        for tail, count in sorted(stat.tail_counts.items()):
            fraction = count / stat.count if stat.count else 0.0
            rows.append(
                {
                    "source": stat.source,
                    "bucket": stat.bucket,
                    "tail": tail,
                    "count": count,
                    "fraction": round(fraction, 8),
                    "geometric_fraction": round(2.0 ** (-tail), 8),
                    "diff_vs_geometric": round(fraction - 2.0 ** (-tail), 8),
                }
            )
    return rows


def run_real(limit: int, max_blocks: int, collectors: dict[str, dict[tuple[str, str], BucketStats]]) -> None:
    for start in range(3, limit + 1, 2):
        steps = real_chain(start, max_blocks)
        add_chain_to_stats("real", steps, **collectors)


def run_model(
    samples: int,
    max_blocks: int,
    seed: int,
    collectors: dict[str, dict[tuple[str, str], BucketStats]],
) -> None:
    rng = random.Random(seed)
    for sample_id in range(samples):
        steps = model_chain(sample_id, max_blocks, rng)
        add_chain_to_stats("model", steps, **collectors)


def main() -> None:
    args = parse_args()
    samples = args.samples if args.samples is not None else (args.limit - 1) // 2
    collectors: dict[str, dict[tuple[str, str], BucketStats]] = {
        "depth_stats": {},
        "margin_stats": {},
        "duration_stats": {},
        "position_stats": {},
        "prev_exit_stats": {},
        "prev_exit_position_stats": {},
    }

    run_real(args.limit, args.max_blocks, collectors)
    run_model(samples, args.max_blocks, args.seed, collectors)

    args.out_dir.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source",
        "bucket",
        "count",
        "tail_one_fraction",
        "tail_one_diff_vs_geometric",
        "expansive_fraction",
        "avg_tail",
        "avg_exit_v2",
        "avg_local_log",
        "avg_before_log",
        "avg_after_log",
    ]
    outputs = {
        "depth": stats_rows(collectors["depth_stats"]),
        "margin": stats_rows(collectors["margin_stats"]),
        "duration": stats_rows(collectors["duration_stats"]),
        "position": stats_rows(collectors["position_stats"]),
        "prev_exit": stats_rows(collectors["prev_exit_stats"]),
        "prev_exit_position": stats_rows(collectors["prev_exit_position_stats"]),
    }

    for suffix, rows in outputs.items():
        write_rows(rows, args.out_dir / f"{args.prefix}_{suffix}.csv", fieldnames)

    compare_fieldnames = [
        "bucket",
        "real_count",
        "model_count",
        "real_tail_one_fraction",
        "model_tail_one_fraction",
        "tail_one_diff_real_minus_model",
        "tail_one_diff_se",
        "tail_one_diff_ci95_low",
        "tail_one_diff_ci95_high",
        "tail_one_diff_z",
        "real_expansive_fraction",
        "model_expansive_fraction",
        "expansive_diff_real_minus_model",
        "expansive_diff_se",
        "expansive_diff_ci95_low",
        "expansive_diff_ci95_high",
        "expansive_diff_z",
        "real_avg_tail",
        "model_avg_tail",
        "avg_tail_diff_real_minus_model",
    ]
    for suffix, collector_name in [
        ("depth_compare", "depth_stats"),
        ("margin_compare", "margin_stats"),
        ("duration_compare", "duration_stats"),
        ("position_compare", "position_stats"),
        ("prev_exit_compare", "prev_exit_stats"),
        ("prev_exit_position_compare", "prev_exit_position_stats"),
    ]:
        write_rows(
            compare_rows(collectors[collector_name]),
            args.out_dir / f"{args.prefix}_{suffix}.csv",
            compare_fieldnames,
        )

    write_rows(
        tail_distribution_rows(collectors["position_stats"]),
        args.out_dir / f"{args.prefix}_position_tail_distribution.csv",
        [
            "source",
            "bucket",
            "tail",
            "count",
            "fraction",
            "geometric_fraction",
            "diff_vs_geometric",
        ],
    )

    print(f"limit={args.limit}")
    print(f"samples={samples}")
    print(f"seed={args.seed}")
    for suffix in outputs:
        print(f"{suffix}={args.out_dir / f'{args.prefix}_{suffix}.csv'}")
    print(
        "position_tail_distribution="
        f"{args.out_dir / f'{args.prefix}_position_tail_distribution.csv'}"
    )

    for row in outputs["position"]:
        if row["bucket"] in {"interior_block", "final_block"}:
            print(
                row["source"],
                row["bucket"],
                f"count={row['count']}",
                f"tail_one_fraction={row['tail_one_fraction']}",
                f"expansive_fraction={row['expansive_fraction']}",
                f"avg_tail={row['avg_tail']}",
            )


if __name__ == "__main__":
    main()
