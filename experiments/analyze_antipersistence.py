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
class BlockSample:
    source: str
    chain_id: int
    block_index: int
    tail: int
    exit_v2: int
    local_log: float
    cumulative_log: float
    expansive: bool


@dataclass(frozen=True)
class ChainSummary:
    source: str
    chain_id: int
    status: str
    blocks: int
    max_expansive_run: int
    expansive_blocks: int
    final_log: float


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare real and modeled anti-persistence between Collatz odd-to-odd blocks."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--long-tail-threshold", type=int, default=8)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="antipersistence_limit_1000000")
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


def correlation(pairs: list[tuple[float, float]]) -> float | None:
    if len(pairs) < 2:
        return None

    xs = [pair[0] for pair in pairs]
    ys = [pair[1] for pair in pairs]
    mean_x = sum(xs) / len(xs)
    mean_y = sum(ys) / len(ys)
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in pairs)
    variance_x = sum((x - mean_x) ** 2 for x in xs)
    variance_y = sum((y - mean_y) ** 2 for y in ys)
    denominator = math.sqrt(variance_x * variance_y)
    if denominator == 0:
        return None
    return numerator / denominator


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


def analyze_real_chain(n: int, max_blocks: int) -> tuple[ChainSummary, list[BlockSample]]:
    current = n
    cumulative_log = 0.0
    current_run = 0
    max_run = 0
    expansive_blocks = 0
    blocks: list[BlockSample] = []

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        next_odd = block.next_odd
        local_log = math.log(next_odd / current)
        cumulative_log += local_log
        expansive = local_log > 0
        if expansive:
            current_run += 1
            expansive_blocks += 1
        else:
            current_run = 0
        max_run = max(max_run, current_run)

        blocks.append(
            BlockSample(
                source="real",
                chain_id=n,
                block_index=block_index,
                tail=block.tail_length,
                exit_v2=block.exit_v2,
                local_log=local_log,
                cumulative_log=cumulative_log,
                expansive=expansive,
            )
        )

        current = next_odd
        if current == 1:
            return (
                ChainSummary(
                    source="real",
                    chain_id=n,
                    status="one",
                    blocks=block_index,
                    max_expansive_run=max_run,
                    expansive_blocks=expansive_blocks,
                    final_log=cumulative_log,
                ),
                blocks,
            )
        if current < n:
            return (
                ChainSummary(
                    source="real",
                    chain_id=n,
                    status="drop",
                    blocks=block_index,
                    max_expansive_run=max_run,
                    expansive_blocks=expansive_blocks,
                    final_log=cumulative_log,
                ),
                blocks,
            )

    return (
        ChainSummary(
            source="real",
            chain_id=n,
            status="maxed",
            blocks=max_blocks,
            max_expansive_run=max_run,
            expansive_blocks=expansive_blocks,
            final_log=cumulative_log,
        ),
        blocks,
    )


def analyze_model_chain(
    sample_id: int,
    *,
    max_blocks: int,
    rng: random.Random,
) -> tuple[ChainSummary, list[BlockSample]]:
    cumulative_log = 0.0
    current_run = 0
    max_run = 0
    expansive_blocks = 0
    blocks: list[BlockSample] = []
    log_three_halves = math.log(1.5)
    log_two = math.log(2.0)

    for block_index in range(1, max_blocks + 1):
        tail = sample_geometric_half(rng)
        exit_v2 = sample_geometric_half(rng)
        local_log = tail * log_three_halves - exit_v2 * log_two
        cumulative_log += local_log
        expansive = local_log > 0
        if expansive:
            current_run += 1
            expansive_blocks += 1
        else:
            current_run = 0
        max_run = max(max_run, current_run)

        blocks.append(
            BlockSample(
                source="model",
                chain_id=sample_id,
                block_index=block_index,
                tail=tail,
                exit_v2=exit_v2,
                local_log=local_log,
                cumulative_log=cumulative_log,
                expansive=expansive,
            )
        )

        if cumulative_log < 0:
            return (
                ChainSummary(
                    source="model",
                    chain_id=sample_id,
                    status="drop",
                    blocks=block_index,
                    max_expansive_run=max_run,
                    expansive_blocks=expansive_blocks,
                    final_log=cumulative_log,
                ),
                blocks,
            )

    return (
        ChainSummary(
            source="model",
            chain_id=sample_id,
            status="maxed",
            blocks=max_blocks,
            max_expansive_run=max_run,
            expansive_blocks=expansive_blocks,
            final_log=cumulative_log,
        ),
        blocks,
    )


def pair_blocks(blocks: list[BlockSample]) -> list[tuple[BlockSample, BlockSample]]:
    by_chain: dict[tuple[str, int], list[BlockSample]] = {}
    for block in blocks:
        by_chain.setdefault((block.source, block.chain_id), []).append(block)

    pairs = []
    for chain_blocks in by_chain.values():
        chain_blocks.sort(key=lambda block: block.block_index)
        pairs.extend(zip(chain_blocks, chain_blocks[1:]))
    return pairs


def summarize_source(
    source: str,
    chains: list[ChainSummary],
    blocks: list[BlockSample],
    *,
    long_tail_threshold: int,
) -> dict[str, object]:
    pairs = pair_blocks(blocks)
    log_pairs = [(left.local_log, right.local_log) for left, right in pairs]
    tail_pairs = [(float(left.tail), float(right.tail)) for left, right in pairs]
    run_values = sorted(float(chain.max_expansive_run) for chain in chains)
    status_counts = Counter(chain.status for chain in chains)

    after_expansive = [right for left, right in pairs if left.expansive]
    after_non_expansive = [right for left, right in pairs if not left.expansive]
    after_long_tail = [right for left, right in pairs if left.tail >= long_tail_threshold]
    after_short_tail = [right for left, right in pairs if left.tail < long_tail_threshold]

    def fraction_expansive(values: list[BlockSample]) -> float:
        if not values:
            return 0.0
        return sum(1 for block in values if block.expansive) / len(values)

    def avg_log(values: list[BlockSample]) -> float:
        if not values:
            return 0.0
        return sum(block.local_log for block in values) / len(values)

    def avg_tail(values: list[BlockSample]) -> float:
        if not values:
            return 0.0
        return sum(block.tail for block in values) / len(values)

    log_corr = correlation(log_pairs)
    tail_corr = correlation(tail_pairs)

    return {
        "source": source,
        "chains": len(chains),
        "blocks": len(blocks),
        "pairs": len(pairs),
        "drop_fraction": round(status_counts["drop"] / len(chains), 8),
        "one_fraction": round(status_counts["one"] / len(chains), 8),
        "maxed_fraction": round(status_counts["maxed"] / len(chains), 8),
        "expansive_fraction": round(sum(1 for block in blocks if block.expansive) / len(blocks), 8),
        "mean_local_log": round(sum(block.local_log for block in blocks) / len(blocks), 12),
        "log_pair_correlation": "" if log_corr is None else round(log_corr, 12),
        "tail_pair_correlation": "" if tail_corr is None else round(tail_corr, 12),
        "p_next_exp_after_exp": round(fraction_expansive(after_expansive), 8),
        "p_next_exp_after_nonexp": round(fraction_expansive(after_non_expansive), 8),
        "avg_next_log_after_exp": round(avg_log(after_expansive), 12),
        "avg_next_log_after_nonexp": round(avg_log(after_non_expansive), 12),
        "p_next_exp_after_long_tail": round(fraction_expansive(after_long_tail), 8),
        "p_next_exp_after_short_tail": round(fraction_expansive(after_short_tail), 8),
        "avg_next_tail_after_long_tail": round(avg_tail(after_long_tail), 8),
        "avg_next_tail_after_short_tail": round(avg_tail(after_short_tail), 8),
        "mean_max_expansive_run": round(sum(run_values) / len(run_values), 8),
        "p99_max_expansive_run": round(quantile(run_values, 0.99), 6),
        "max_expansive_run": int(max(run_values)),
    }


def run_distribution_rows(real_chains: list[ChainSummary], model_chains: list[ChainSummary]) -> list[dict[str, object]]:
    real_counts = Counter(chain.max_expansive_run for chain in real_chains)
    model_counts = Counter(chain.max_expansive_run for chain in model_chains)
    total_real = len(real_chains)
    total_model = len(model_chains)
    rows = []
    for run_length in range(max(max(real_counts), max(model_counts)) + 1):
        real_count = real_counts[run_length]
        model_count = model_counts[run_length]
        real_fraction = real_count / total_real
        model_fraction = model_count / total_model
        rows.append(
            {
                "max_expansive_run": run_length,
                "real_count": real_count,
                "model_count": model_count,
                "real_fraction": round(real_fraction, 8),
                "model_fraction": round(model_fraction, 8),
                "fraction_diff_real_minus_model": round(real_fraction - model_fraction, 8),
            }
        )
    return rows


def conditional_rows(source: str, pairs: list[tuple[BlockSample, BlockSample]]) -> list[dict[str, object]]:
    conditions = [
        ("prev_expansive", lambda left: left.expansive),
        ("prev_nonexpansive", lambda left: not left.expansive),
        ("prev_tail_ge_8", lambda left: left.tail >= 8),
        ("prev_tail_lt_8", lambda left: left.tail < 8),
        ("prev_exit_v2_le_2", lambda left: left.exit_v2 <= 2),
        ("prev_exit_v2_ge_5", lambda left: left.exit_v2 >= 5),
    ]
    rows = []
    for name, predicate in conditions:
        selected = [right for left, right in pairs if predicate(left)]
        if not selected:
            rows.append(
                {
                    "source": source,
                    "condition": name,
                    "count": 0,
                    "next_expansive_fraction": 0.0,
                    "avg_next_log": 0.0,
                    "avg_next_tail": 0.0,
                    "avg_next_exit_v2": 0.0,
                }
            )
            continue

        rows.append(
            {
                "source": source,
                "condition": name,
                "count": len(selected),
                "next_expansive_fraction": round(sum(1 for block in selected if block.expansive) / len(selected), 8),
                "avg_next_log": round(sum(block.local_log for block in selected) / len(selected), 12),
                "avg_next_tail": round(sum(block.tail for block in selected) / len(selected), 8),
                "avg_next_exit_v2": round(sum(block.exit_v2 for block in selected) / len(selected), 8),
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

    real_chains: list[ChainSummary] = []
    real_blocks: list[BlockSample] = []
    for n in range(3, args.limit + 1, 2):
        chain, blocks = analyze_real_chain(n, args.max_blocks)
        real_chains.append(chain)
        real_blocks.extend(blocks)

    model_chains: list[ChainSummary] = []
    model_blocks: list[BlockSample] = []
    for sample_id in range(1, sample_count + 1):
        chain, blocks = analyze_model_chain(sample_id, max_blocks=args.max_blocks, rng=rng)
        model_chains.append(chain)
        model_blocks.extend(blocks)

    real_pairs = pair_blocks(real_blocks)
    model_pairs = pair_blocks(model_blocks)

    summary_rows = [
        summarize_source(
            "real",
            real_chains,
            real_blocks,
            long_tail_threshold=args.long_tail_threshold,
        ),
        summarize_source(
            "model",
            model_chains,
            model_blocks,
            long_tail_threshold=args.long_tail_threshold,
        ),
    ]
    conditional = conditional_rows("real", real_pairs) + conditional_rows("model", model_pairs)
    runs = run_distribution_rows(real_chains, model_chains)

    summary_path = args.out_dir / f"{args.prefix}_summary.csv"
    conditional_path = args.out_dir / f"{args.prefix}_conditional.csv"
    runs_path = args.out_dir / f"{args.prefix}_runs.csv"

    write_csv(
        summary_rows,
        summary_path,
        [
            "source",
            "chains",
            "blocks",
            "pairs",
            "drop_fraction",
            "one_fraction",
            "maxed_fraction",
            "expansive_fraction",
            "mean_local_log",
            "log_pair_correlation",
            "tail_pair_correlation",
            "p_next_exp_after_exp",
            "p_next_exp_after_nonexp",
            "avg_next_log_after_exp",
            "avg_next_log_after_nonexp",
            "p_next_exp_after_long_tail",
            "p_next_exp_after_short_tail",
            "avg_next_tail_after_long_tail",
            "avg_next_tail_after_short_tail",
            "mean_max_expansive_run",
            "p99_max_expansive_run",
            "max_expansive_run",
        ],
    )
    write_csv(
        conditional,
        conditional_path,
        [
            "source",
            "condition",
            "count",
            "next_expansive_fraction",
            "avg_next_log",
            "avg_next_tail",
            "avg_next_exit_v2",
        ],
    )
    write_csv(
        runs,
        runs_path,
        [
            "max_expansive_run",
            "real_count",
            "model_count",
            "real_fraction",
            "model_fraction",
            "fraction_diff_real_minus_model",
        ],
    )

    print(f"limit={args.limit}")
    print(f"samples={sample_count}")
    print(f"seed={args.seed}")
    print(f"summary={summary_path}")
    print(f"conditional={conditional_path}")
    print(f"runs={runs_path}")
    for row in summary_rows:
        print(
            f"{row['source']}: corr_log={row['log_pair_correlation']} "
            f"p_next_exp_after_exp={row['p_next_exp_after_exp']} "
            f"max_run={row['max_expansive_run']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
