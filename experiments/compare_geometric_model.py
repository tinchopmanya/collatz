from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block  # noqa: E402


@dataclass(frozen=True)
class ChainSample:
    source: str
    sample_id: int
    status: str
    blocks: int
    max_log_odd_ratio: float
    max_log_peak_ratio: float
    final_log_ratio: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare real Collatz odd-to-odd chains with an independent geometric model."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="geometric_model_limit_1000000")
    return parser.parse_args()


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def quantile(sorted_values: list[float], probability: float) -> float:
    if not sorted_values:
        raise ValueError("quantile requires at least one value")
    if probability <= 0:
        return sorted_values[0]
    if probability >= 1:
        return sorted_values[-1]

    index = probability * (len(sorted_values) - 1)
    lower = math.floor(index)
    upper = math.ceil(index)
    if lower == upper:
        return sorted_values[lower]
    weight = index - lower
    return sorted_values[lower] * (1 - weight) + sorted_values[upper] * weight


def sample_geometric_half(rng: random.Random) -> int:
    value = 1
    while rng.random() < 0.5:
        value += 1
    return value


def analyze_real_start(n: int, max_blocks: int) -> ChainSample:
    current = n
    max_odd = n
    max_peak = n

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        current = block.next_odd
        max_odd = max(max_odd, current)
        max_peak = max(max_peak, block.block_peak)

        if current == 1:
            return ChainSample(
                source="real",
                sample_id=n,
                status="one",
                blocks=block_index,
                max_log_odd_ratio=math.log(max_odd / n),
                max_log_peak_ratio=math.log(max_peak / n),
                final_log_ratio=math.log(current / n),
            )
        if current < n:
            return ChainSample(
                source="real",
                sample_id=n,
                status="drop",
                blocks=block_index,
                max_log_odd_ratio=math.log(max_odd / n),
                max_log_peak_ratio=math.log(max_peak / n),
                final_log_ratio=math.log(current / n),
            )

    return ChainSample(
        source="real",
        sample_id=n,
        status="maxed",
        blocks=max_blocks,
        max_log_odd_ratio=math.log(max_odd / n),
        max_log_peak_ratio=math.log(max_peak / n),
        final_log_ratio=math.log(current / n),
    )


def simulate_model_sample(sample_id: int, *, max_blocks: int, rng: random.Random) -> ChainSample:
    cumulative_log = 0.0
    max_log_odd = 0.0
    max_log_peak = 0.0
    log_three_halves = math.log(1.5)
    log_two = math.log(2.0)

    for block_index in range(1, max_blocks + 1):
        tail = sample_geometric_half(rng)
        exit_v2 = sample_geometric_half(rng)
        peak_log = cumulative_log + log_two + tail * log_three_halves
        local_log = tail * log_three_halves - exit_v2 * log_two
        cumulative_log += local_log
        max_log_peak = max(max_log_peak, peak_log)
        max_log_odd = max(max_log_odd, cumulative_log)

        if cumulative_log < 0:
            return ChainSample(
                source="model",
                sample_id=sample_id,
                status="drop",
                blocks=block_index,
                max_log_odd_ratio=max_log_odd,
                max_log_peak_ratio=max_log_peak,
                final_log_ratio=cumulative_log,
            )

    return ChainSample(
        source="model",
        sample_id=sample_id,
        status="maxed",
        blocks=max_blocks,
        max_log_odd_ratio=max_log_odd,
        max_log_peak_ratio=max_log_peak,
        final_log_ratio=cumulative_log,
    )


def summarize_samples(source: str, samples: list[ChainSample]) -> dict[str, object]:
    blocks = sorted(float(sample.blocks) for sample in samples)
    max_odd = sorted(math.exp(sample.max_log_odd_ratio) for sample in samples)
    max_peak = sorted(math.exp(sample.max_log_peak_ratio) for sample in samples)
    final_logs = sorted(sample.final_log_ratio for sample in samples)
    status_counts = Counter(sample.status for sample in samples)

    return {
        "source": source,
        "samples": len(samples),
        "drop_fraction": round(status_counts["drop"] / len(samples), 8),
        "one_fraction": round(status_counts["one"] / len(samples), 8),
        "maxed_fraction": round(status_counts["maxed"] / len(samples), 8),
        "mean_blocks": round(sum(blocks) / len(blocks), 6),
        "median_blocks": round(quantile(blocks, 0.5), 6),
        "p90_blocks": round(quantile(blocks, 0.9), 6),
        "p99_blocks": round(quantile(blocks, 0.99), 6),
        "p999_blocks": round(quantile(blocks, 0.999), 6),
        "max_blocks": int(max(blocks)),
        "mean_max_odd_ratio": round(sum(max_odd) / len(max_odd), 6),
        "p99_max_odd_ratio": round(quantile(max_odd, 0.99), 6),
        "max_odd_ratio": round(max(max_odd), 6),
        "mean_max_peak_ratio": round(sum(max_peak) / len(max_peak), 6),
        "p99_max_peak_ratio": round(quantile(max_peak, 0.99), 6),
        "max_peak_ratio": round(max(max_peak), 6),
        "median_final_log_ratio": round(quantile(final_logs, 0.5), 12),
    }


def distribution_rows(real: list[ChainSample], model: list[ChainSample]) -> list[dict[str, object]]:
    real_counts = Counter(sample.blocks for sample in real)
    model_counts = Counter(sample.blocks for sample in model)
    total_real = len(real)
    total_model = len(model)
    rows = []

    for blocks in range(1, max(max(real_counts), max(model_counts)) + 1):
        real_count = real_counts[blocks]
        model_count = model_counts[blocks]
        real_fraction = real_count / total_real
        model_fraction = model_count / total_model
        rows.append(
            {
                "blocks": blocks,
                "real_count": real_count,
                "model_count": model_count,
                "real_fraction": round(real_fraction, 8),
                "model_fraction": round(model_fraction, 8),
                "fraction_diff_real_minus_model": round(real_fraction - model_fraction, 8),
            }
        )

    return rows


def top_record_rows(source: str, samples: list[ChainSample], metric: str, limit: int = 20) -> list[dict[str, object]]:
    if metric == "blocks":
        key = lambda sample: (sample.blocks, sample.max_log_peak_ratio, sample.max_log_odd_ratio)
    elif metric == "max_peak_ratio":
        key = lambda sample: (sample.max_log_peak_ratio, sample.blocks, sample.max_log_odd_ratio)
    elif metric == "max_odd_ratio":
        key = lambda sample: (sample.max_log_odd_ratio, sample.blocks, sample.max_log_peak_ratio)
    else:
        raise ValueError(f"unknown metric {metric}")

    rows = []
    for rank, sample in enumerate(sorted(samples, key=key, reverse=True)[:limit], start=1):
        rows.append(
            {
                "source": source,
                "rank_metric": metric,
                "rank": rank,
                "sample_id": sample.sample_id,
                "status": sample.status,
                "blocks": sample.blocks,
                "max_odd_ratio": round(math.exp(sample.max_log_odd_ratio), 6),
                "max_peak_ratio": round(math.exp(sample.max_log_peak_ratio), 6),
                "final_log_ratio": round(sample.final_log_ratio, 12),
            }
        )
    return rows


def tail_probability_rows(real: list[ChainSample], model: list[ChainSample]) -> list[dict[str, object]]:
    specs = [
        (
            "blocks_ge",
            [5, 10, 20, 30, 40, 50],
            lambda sample: float(sample.blocks),
        ),
        (
            "max_odd_ratio_ge",
            [10, 100, 1_000, 10_000, 100_000],
            lambda sample: math.exp(sample.max_log_odd_ratio),
        ),
        (
            "max_peak_ratio_ge",
            [10, 100, 1_000, 10_000, 100_000, 1_000_000],
            lambda sample: math.exp(sample.max_log_peak_ratio),
        ),
    ]
    rows = []
    for metric, thresholds, value_func in specs:
        real_values = [value_func(sample) for sample in real]
        model_values = [value_func(sample) for sample in model]
        for threshold in thresholds:
            real_count = sum(1 for value in real_values if value >= threshold)
            model_count = sum(1 for value in model_values if value >= threshold)
            real_fraction = real_count / len(real)
            model_fraction = model_count / len(model)
            ratio = None if real_fraction == 0 else model_fraction / real_fraction
            rows.append(
                {
                    "metric": metric,
                    "threshold": threshold,
                    "real_count": real_count,
                    "model_count": model_count,
                    "real_fraction": round(real_fraction, 8),
                    "model_fraction": round(model_fraction, 8),
                    "model_over_real": "" if ratio is None else round(ratio, 6),
                    "fraction_diff_model_minus_real": round(model_fraction - real_fraction, 8),
                }
            )
    return rows


def main() -> int:
    args = parse_args()
    if args.limit < 3:
        raise ValueError("limit must be at least 3")
    if args.max_blocks < 1:
        raise ValueError("max_blocks must be positive")

    sample_count = args.samples if args.samples is not None else (args.limit - 1) // 2
    rng = random.Random(args.seed)

    real_samples = [
        analyze_real_start(n, args.max_blocks)
        for n in range(3, args.limit + 1, 2)
    ]
    model_samples = [
        simulate_model_sample(index, max_blocks=args.max_blocks, rng=rng)
        for index in range(1, sample_count + 1)
    ]

    summary_rows = [
        summarize_samples("real", real_samples),
        summarize_samples("model", model_samples),
    ]
    blocks_rows = distribution_rows(real_samples, model_samples)
    tail_rows = tail_probability_rows(real_samples, model_samples)

    record_rows: list[dict[str, object]] = []
    for metric in ("blocks", "max_peak_ratio", "max_odd_ratio"):
        record_rows.extend(top_record_rows("real", real_samples, metric))
        record_rows.extend(top_record_rows("model", model_samples, metric))

    summary_path = args.out_dir / f"{args.prefix}_summary.csv"
    blocks_path = args.out_dir / f"{args.prefix}_blocks.csv"
    tails_path = args.out_dir / f"{args.prefix}_tail_probabilities.csv"
    records_path = args.out_dir / f"{args.prefix}_records.csv"

    write_csv(
        summary_rows,
        summary_path,
        [
            "source",
            "samples",
            "drop_fraction",
            "one_fraction",
            "maxed_fraction",
            "mean_blocks",
            "median_blocks",
            "p90_blocks",
            "p99_blocks",
            "p999_blocks",
            "max_blocks",
            "mean_max_odd_ratio",
            "p99_max_odd_ratio",
            "max_odd_ratio",
            "mean_max_peak_ratio",
            "p99_max_peak_ratio",
            "max_peak_ratio",
            "median_final_log_ratio",
        ],
    )
    write_csv(
        blocks_rows,
        blocks_path,
        [
            "blocks",
            "real_count",
            "model_count",
            "real_fraction",
            "model_fraction",
            "fraction_diff_real_minus_model",
        ],
    )
    write_csv(
        tail_rows,
        tails_path,
        [
            "metric",
            "threshold",
            "real_count",
            "model_count",
            "real_fraction",
            "model_fraction",
            "model_over_real",
            "fraction_diff_model_minus_real",
        ],
    )
    write_csv(
        record_rows,
        records_path,
        [
            "source",
            "rank_metric",
            "rank",
            "sample_id",
            "status",
            "blocks",
            "max_odd_ratio",
            "max_peak_ratio",
            "final_log_ratio",
        ],
    )

    print(f"limit={args.limit}")
    print(f"samples={sample_count}")
    print(f"seed={args.seed}")
    print(f"summary={summary_path}")
    print(f"blocks={blocks_path}")
    print(f"tails={tails_path}")
    print(f"records={records_path}")
    for row in summary_rows:
        print(
            f"{row['source']}: mean_blocks={row['mean_blocks']} "
            f"p99={row['p99_blocks']} max={row['max_blocks']} "
            f"max_peak={row['max_peak_ratio']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
