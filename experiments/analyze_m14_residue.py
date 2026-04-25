from __future__ import annotations

import argparse
import csv
import math
import random
import sys
from collections import defaultdict
from dataclasses import dataclass
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
    q_mod: int
    current_mod: int

    @property
    def tail_one(self) -> bool:
        return self.tail == 1

    @property
    def expansive(self) -> bool:
        return self.local_log > 0.0


@dataclass
class BucketStats:
    partition: str
    bucket: str
    source: str
    count: int = 0
    tail_one_count: int = 0
    expansive_count: int = 0
    tail_sum: int = 0
    exit_v2_sum: int = 0
    local_log_sum: float = 0.0
    before_log_sum: float = 0.0
    after_log_sum: float = 0.0

    def add(self, step: ChainStep) -> None:
        self.count += 1
        if step.tail_one:
            self.tail_one_count += 1
        if step.expansive:
            self.expansive_count += 1
        self.tail_sum += step.tail
        self.exit_v2_sum += step.exit_v2
        self.local_log_sum += step.local_log
        self.before_log_sum += step.before_log
        self.after_log_sum += step.after_log

    def fraction(self, value: int) -> float:
        return value / self.count if self.count else 0.0

    def mean(self, value: float) -> float:
        return value / self.count if self.count else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Decompose the M14 survivor-chain residue: previous exit_v2 = 5, "
            "current block is interior, and current tail is compared real vs model."
        )
    )
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--mod-ks", default="4,5,6,7,8")
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m14_residue")
    return parser.parse_args()


def parse_mod_ks(raw: str) -> list[int]:
    values = sorted({int(part.strip()) for part in raw.split(",") if part.strip()})
    if not values:
        raise ValueError("at least one modulus exponent is required")
    if any(value < 1 for value in values):
        raise ValueError("modulus exponents must be positive")
    return values


def sample_geometric_half(rng: random.Random) -> int:
    value = 1
    while rng.random() < 0.5:
        value += 1
    return value


def sample_odd_residue(max_mod: int, rng: random.Random) -> int:
    return 2 * rng.randrange(max_mod // 2) + 1


def real_chain(start: int, max_blocks: int, max_mod: int) -> list[ChainStep]:
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
                q_mod=block.odd_factor % max_mod,
                current_mod=current % max_mod,
            )
        )

        current = next_odd
        if current == 1 or current < start:
            break
        before_log = after_log

    return steps


def model_chain(
    sample_id: int,
    max_blocks: int,
    max_mod: int,
    rng: random.Random,
    residue_rng: random.Random,
) -> list[ChainStep]:
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
        q_mod = sample_odd_residue(max_mod, residue_rng)
        current_mod = ((1 << tail) * q_mod - 1) % max_mod
        steps.append(
            ChainStep(
                block_index=block_index,
                tail=tail,
                exit_v2=exit_v2,
                local_log=local_log,
                before_log=before_log,
                after_log=after_log,
                q_mod=q_mod,
                current_mod=current_mod,
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


def prev_tail_bucket(tail: int) -> str:
    if tail <= 10:
        return f"prev_tail_{tail:02d}"
    return "prev_tail_11_plus"


def position_bucket(step_index: int, duration: int) -> str:
    if duration == 1:
        return "only_block"
    if step_index == 1:
        return "first_block"
    if step_index == duration:
        return "final_block"
    return "interior_block"


def bucket_key(partition: str, bucket: str, source: str) -> tuple[str, str, str]:
    return partition, bucket, source


def get_bucket(
    stats: dict[tuple[str, str, str], BucketStats],
    partition: str,
    bucket: str,
    source: str,
) -> BucketStats:
    key = bucket_key(partition, bucket, source)
    if key not in stats:
        stats[key] = BucketStats(partition=partition, bucket=bucket, source=source)
    return stats[key]


def add_transition(
    stats: dict[tuple[str, str, str], BucketStats],
    source: str,
    previous: ChainStep,
    current: ChainStep,
    mod_ks: list[int],
) -> None:
    buckets = [
        ("summary", "all"),
        ("depth", depth_bucket(current.block_index)),
        ("margin", margin_bucket(current.before_log)),
        ("prev_tail", prev_tail_bucket(previous.tail)),
    ]
    for k in mod_ks:
        modulus = 1 << k
        buckets.append((f"q_mod_2^{k}", str(current.q_mod % modulus)))
        buckets.append((f"current_mod_2^{k}", str(current.current_mod % modulus)))

    for partition, bucket in buckets:
        get_bucket(stats, partition, bucket, source).add(current)


def add_chain_to_stats(
    stats: dict[tuple[str, str, str], BucketStats],
    source: str,
    steps: list[ChainStep],
    mod_ks: list[int],
) -> None:
    duration = len(steps)
    for index in range(2, duration + 1):
        current_position = position_bucket(index, duration)
        if current_position != "interior_block":
            continue
        previous = steps[index - 2]
        current = steps[index - 1]
        if previous.exit_v2 != 5:
            continue
        add_transition(stats, source, previous, current, mod_ks)


def run_real(
    limit: int,
    max_blocks: int,
    max_mod: int,
    mod_ks: list[int],
    stats: dict[tuple[str, str, str], BucketStats],
) -> None:
    for start in range(3, limit + 1, 2):
        add_chain_to_stats(stats, "real", real_chain(start, max_blocks, max_mod), mod_ks)


def run_model(
    samples: int,
    max_blocks: int,
    max_mod: int,
    mod_ks: list[int],
    seed: int,
    stats: dict[tuple[str, str, str], BucketStats],
) -> None:
    rng = random.Random(seed)
    residue_rng = random.Random(seed ^ 0x5EED_4D14)
    for sample_id in range(samples):
        add_chain_to_stats(
            stats,
            "model",
            model_chain(sample_id, max_blocks, max_mod, rng, residue_rng),
            mod_ks,
        )


def binomial_diff(
    real_success: int,
    real_count: int,
    model_success: int,
    model_count: int,
) -> tuple[float, float, float, float, float]:
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


def compare_partition_rows(
    stats: dict[tuple[str, str, str], BucketStats],
    partition: str,
    total_real: BucketStats,
    total_model: BucketStats,
) -> list[dict[str, object]]:
    buckets = sorted({bucket for part, bucket, _ in stats if part == partition}, key=bucket_sort_key)
    rows = []

    for bucket in buckets:
        real = stats.get(bucket_key(partition, bucket, "real"))
        model = stats.get(bucket_key(partition, bucket, "model"))
        if real is None and model is None:
            continue

        real_count = real.count if real is not None else 0
        model_count = model.count if model is not None else 0
        real_tail_one = real.tail_one_count if real is not None else 0
        model_tail_one = model.tail_one_count if model is not None else 0
        real_expansive = real.expansive_count if real is not None else 0
        model_expansive = model.expansive_count if model is not None else 0
        tail_diff, tail_se, tail_low, tail_high, tail_z = binomial_diff(
            real_tail_one,
            real_count,
            model_tail_one,
            model_count,
        )
        exp_diff, exp_se, exp_low, exp_high, exp_z = binomial_diff(
            real_expansive,
            real_count,
            model_expansive,
            model_count,
        )
        real_success_share = real_tail_one / total_real.count if total_real.count else 0.0
        model_success_share = model_tail_one / total_model.count if total_model.count else 0.0

        rows.append(
            {
                "partition": partition,
                "bucket": bucket,
                "real_count": real_count,
                "model_count": model_count,
                "real_bucket_share": round(real_count / total_real.count, 10) if total_real.count else 0.0,
                "model_bucket_share": round(model_count / total_model.count, 10) if total_model.count else 0.0,
                "bucket_share_diff_real_minus_model": round(
                    (real_count / total_real.count if total_real.count else 0.0)
                    - (model_count / total_model.count if total_model.count else 0.0),
                    10,
                ),
                "real_tail_one_count": real_tail_one,
                "model_tail_one_count": model_tail_one,
                "real_tail_one_fraction": round(real_tail_one / real_count, 8) if real_count else 0.0,
                "model_tail_one_fraction": round(model_tail_one / model_count, 8) if model_count else 0.0,
                "tail_one_diff_real_minus_model": round(tail_diff, 8),
                "tail_one_diff_se": round(tail_se, 10),
                "tail_one_diff_ci95_low": round(tail_low, 8),
                "tail_one_diff_ci95_high": round(tail_high, 8),
                "tail_one_diff_z": round(tail_z, 6),
                "tail_one_success_share_real": round(real_success_share, 10),
                "tail_one_success_share_model": round(model_success_share, 10),
                "tail_one_success_share_diff": round(real_success_share - model_success_share, 10),
                "real_expansive_fraction": round(real_expansive / real_count, 8) if real_count else 0.0,
                "model_expansive_fraction": round(model_expansive / model_count, 8) if model_count else 0.0,
                "expansive_diff_real_minus_model": round(exp_diff, 8),
                "expansive_diff_se": round(exp_se, 10),
                "expansive_diff_ci95_low": round(exp_low, 8),
                "expansive_diff_ci95_high": round(exp_high, 8),
                "expansive_diff_z": round(exp_z, 6),
                "real_avg_tail": round(real.mean(float(real.tail_sum)), 8) if real is not None else 0.0,
                "model_avg_tail": round(model.mean(float(model.tail_sum)), 8) if model is not None else 0.0,
                "avg_tail_diff_real_minus_model": round(
                    (real.mean(float(real.tail_sum)) if real is not None else 0.0)
                    - (model.mean(float(model.tail_sum)) if model is not None else 0.0),
                    8,
                ),
                "real_avg_exit_v2": round(real.mean(float(real.exit_v2_sum)), 8) if real is not None else 0.0,
                "model_avg_exit_v2": round(model.mean(float(model.exit_v2_sum)), 8) if model is not None else 0.0,
                "real_avg_local_log": round(real.mean(real.local_log_sum), 12) if real is not None else 0.0,
                "model_avg_local_log": round(model.mean(model.local_log_sum), 12) if model is not None else 0.0,
                "real_avg_before_log": round(real.mean(real.before_log_sum), 12) if real is not None else 0.0,
                "model_avg_before_log": round(model.mean(model.before_log_sum), 12) if model is not None else 0.0,
            }
        )

    return rows


def bucket_sort_key(bucket: str) -> tuple[int, object]:
    try:
        return 0, int(bucket)
    except ValueError:
        return 1, bucket


def summary_rows(
    stats: dict[tuple[str, str, str], BucketStats],
    partitions: list[str],
    total_real: BucketStats,
    total_model: BucketStats,
) -> list[dict[str, object]]:
    rows = []
    tail_diff, tail_se, tail_low, tail_high, tail_z = binomial_diff(
        total_real.tail_one_count,
        total_real.count,
        total_model.tail_one_count,
        total_model.count,
    )
    rows.append(
        {
            "partition": "summary",
            "bucket_count": 1,
            "real_count": total_real.count,
            "model_count": total_model.count,
            "real_tail_one_fraction": round(total_real.fraction(total_real.tail_one_count), 8),
            "model_tail_one_fraction": round(total_model.fraction(total_model.tail_one_count), 8),
            "tail_one_diff_real_minus_model": round(tail_diff, 8),
            "tail_one_diff_ci95_low": round(tail_low, 8),
            "tail_one_diff_ci95_high": round(tail_high, 8),
            "tail_one_diff_z": round(tail_z, 6),
            "max_abs_success_share_diff": round(abs(tail_diff), 10),
            "max_abs_success_bucket": "all",
            "positive_success_share_diff_sum": round(max(0.0, tail_diff), 10),
            "negative_success_share_diff_sum": round(min(0.0, tail_diff), 10),
            "min_real_bucket_count": total_real.count,
            "min_model_bucket_count": total_model.count,
        }
    )

    for partition in partitions:
        rows_for_partition = compare_partition_rows(stats, partition, total_real, total_model)
        if not rows_for_partition:
            continue
        max_abs_row = max(
            rows_for_partition,
            key=lambda row: abs(float(row["tail_one_success_share_diff"])),
        )
        positive_sum = sum(
            float(row["tail_one_success_share_diff"])
            for row in rows_for_partition
            if float(row["tail_one_success_share_diff"]) > 0.0
        )
        negative_sum = sum(
            float(row["tail_one_success_share_diff"])
            for row in rows_for_partition
            if float(row["tail_one_success_share_diff"]) < 0.0
        )
        rows.append(
            {
                "partition": partition,
                "bucket_count": len(rows_for_partition),
                "real_count": total_real.count,
                "model_count": total_model.count,
                "real_tail_one_fraction": round(total_real.fraction(total_real.tail_one_count), 8),
                "model_tail_one_fraction": round(total_model.fraction(total_model.tail_one_count), 8),
                "tail_one_diff_real_minus_model": round(tail_diff, 8),
                "tail_one_diff_ci95_low": round(tail_low, 8),
                "tail_one_diff_ci95_high": round(tail_high, 8),
                "tail_one_diff_z": round(tail_z, 6),
                "max_abs_success_share_diff": max_abs_row["tail_one_success_share_diff"],
                "max_abs_success_bucket": max_abs_row["bucket"],
                "positive_success_share_diff_sum": round(positive_sum, 10),
                "negative_success_share_diff_sum": round(negative_sum, 10),
                "min_real_bucket_count": min(int(row["real_count"]) for row in rows_for_partition),
                "min_model_bucket_count": min(int(row["model_count"]) for row in rows_for_partition),
            }
        )

    return rows


def write_rows(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def combined_mod_rows(
    stats: dict[tuple[str, str, str], BucketStats],
    prefix: str,
    mod_ks: list[int],
    total_real: BucketStats,
    total_model: BucketStats,
) -> list[dict[str, object]]:
    rows = []
    for k in mod_ks:
        partition = f"{prefix}_2^{k}"
        for row in compare_partition_rows(stats, partition, total_real, total_model):
            row = dict(row)
            row["k"] = k
            row["modulus"] = 1 << k
            row["residue"] = int(row["bucket"])
            rows.append(row)
    return rows


def main() -> int:
    args = parse_args()
    mod_ks = parse_mod_ks(args.mod_ks)
    max_mod = 1 << max(mod_ks)
    samples = args.samples if args.samples is not None else (args.limit - 1) // 2
    stats: dict[tuple[str, str, str], BucketStats] = {}

    run_real(args.limit, args.max_blocks, max_mod, mod_ks, stats)
    run_model(samples, args.max_blocks, max_mod, mod_ks, args.seed, stats)

    total_real = stats.get(bucket_key("summary", "all", "real"))
    total_model = stats.get(bucket_key("summary", "all", "model"))
    if total_real is None or total_model is None:
        raise RuntimeError("target transition was not observed in both real and model samples")

    args.out_dir.mkdir(parents=True, exist_ok=True)

    base_compare_fields = [
        "partition",
        "bucket",
        "real_count",
        "model_count",
        "real_bucket_share",
        "model_bucket_share",
        "bucket_share_diff_real_minus_model",
        "real_tail_one_count",
        "model_tail_one_count",
        "real_tail_one_fraction",
        "model_tail_one_fraction",
        "tail_one_diff_real_minus_model",
        "tail_one_diff_se",
        "tail_one_diff_ci95_low",
        "tail_one_diff_ci95_high",
        "tail_one_diff_z",
        "tail_one_success_share_real",
        "tail_one_success_share_model",
        "tail_one_success_share_diff",
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
        "real_avg_exit_v2",
        "model_avg_exit_v2",
        "real_avg_local_log",
        "model_avg_local_log",
        "real_avg_before_log",
        "model_avg_before_log",
    ]
    mod_compare_fields = ["k", "modulus", "residue"] + base_compare_fields
    summary_fields = [
        "partition",
        "bucket_count",
        "real_count",
        "model_count",
        "real_tail_one_fraction",
        "model_tail_one_fraction",
        "tail_one_diff_real_minus_model",
        "tail_one_diff_ci95_low",
        "tail_one_diff_ci95_high",
        "tail_one_diff_z",
        "max_abs_success_share_diff",
        "max_abs_success_bucket",
        "positive_success_share_diff_sum",
        "negative_success_share_diff_sum",
        "min_real_bucket_count",
        "min_model_bucket_count",
    ]

    scalar_partitions = ["depth", "margin", "prev_tail"]
    mod_partitions = [
        *(f"q_mod_2^{k}" for k in mod_ks),
        *(f"current_mod_2^{k}" for k in mod_ks),
    ]
    write_rows(
        summary_rows(stats, scalar_partitions + mod_partitions, total_real, total_model),
        args.out_dir / f"{args.prefix}_summary.csv",
        summary_fields,
    )
    write_rows(
        compare_partition_rows(stats, "depth", total_real, total_model),
        args.out_dir / f"{args.prefix}_by_depth.csv",
        base_compare_fields,
    )
    write_rows(
        compare_partition_rows(stats, "margin", total_real, total_model),
        args.out_dir / f"{args.prefix}_by_margin.csv",
        base_compare_fields,
    )
    write_rows(
        compare_partition_rows(stats, "prev_tail", total_real, total_model),
        args.out_dir / f"{args.prefix}_by_prev_tail.csv",
        base_compare_fields,
    )
    write_rows(
        combined_mod_rows(stats, "q_mod", mod_ks, total_real, total_model),
        args.out_dir / f"{args.prefix}_by_q_mod.csv",
        mod_compare_fields,
    )
    write_rows(
        combined_mod_rows(stats, "current_mod", mod_ks, total_real, total_model),
        args.out_dir / f"{args.prefix}_by_current_mod.csv",
        mod_compare_fields,
    )

    print(f"limit={args.limit}")
    print(f"samples={samples}")
    print(f"seed={args.seed}")
    print(f"mod_ks={','.join(str(k) for k in mod_ks)}")
    print(f"target=prev_exit_v2=5,current_position=interior_block")
    print(f"summary={args.out_dir / f'{args.prefix}_summary.csv'}")
    print(f"by_depth={args.out_dir / f'{args.prefix}_by_depth.csv'}")
    print(f"by_margin={args.out_dir / f'{args.prefix}_by_margin.csv'}")
    print(f"by_prev_tail={args.out_dir / f'{args.prefix}_by_prev_tail.csv'}")
    print(f"by_q_mod={args.out_dir / f'{args.prefix}_by_q_mod.csv'}")
    print(f"by_current_mod={args.out_dir / f'{args.prefix}_by_current_mod.csv'}")
    print(
        "overall",
        f"real_count={total_real.count}",
        f"model_count={total_model.count}",
        f"real_tail_one_fraction={total_real.fraction(total_real.tail_one_count):.8f}",
        f"model_tail_one_fraction={total_model.fraction(total_model.tail_one_count):.8f}",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
