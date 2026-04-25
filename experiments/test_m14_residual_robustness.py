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

from collatz import alternating_block, two_adic_valuation  # noqa: E402


@dataclass(frozen=True)
class ChainTarget:
    source: str
    chain_id: int
    count: int
    success: int


@dataclass
class SourceStats:
    source: str
    chains: int = 0
    target_chains: int = 0
    target_count: int = 0
    target_success: int = 0
    interior_count: int = 0
    interior_success: int = 0

    def add_chain(self, chain: ChainTarget, *, interior_count: int, interior_success: int) -> None:
        self.chains += 1
        self.interior_count += interior_count
        self.interior_success += interior_success
        if chain.count:
            self.target_chains += 1
            self.target_count += chain.count
            self.target_success += chain.success

    def target_fraction(self) -> float:
        return self.target_success / self.target_count if self.target_count else 0.0

    def interior_fraction(self) -> float:
        return self.interior_success / self.interior_count if self.interior_count else 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Confirm or destroy the M14 prev_exit_v2=5 interior-block residue."
    )
    parser.add_argument("--limit", type=int, default=5_000_000)
    parser.add_argument("--start", type=int, default=3)
    parser.add_argument("--samples", type=int, default=None)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--target-prev-exit-v2", type=int, default=5)
    parser.add_argument("--permutations", type=int, default=10_000)
    parser.add_argument("--seed", type=int, default=20260425)
    parser.add_argument("--extra-tests", type=int, default=546)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m14_residual_robustness")
    return parser.parse_args()


def sample_geometric_half(rng: random.Random) -> int:
    value = 1
    while rng.random() < 0.5:
        value += 1
    return value


def position_label(index: int, duration: int) -> str:
    if duration == 1:
        return "only_block"
    if index == 1:
        return "first_block"
    if index == duration:
        return "final_block"
    return "interior_block"


def real_chain_values(start: int, max_blocks: int) -> list[tuple[int, int]]:
    current = start
    values: list[tuple[int, int]] = []
    for _ in range(max_blocks):
        block = alternating_block(current)
        values.append((block.tail_length, block.exit_v2))
        current = block.next_odd
        if current == 1 or current < start:
            break
    return values


def model_chain_values(max_blocks: int, rng: random.Random) -> list[tuple[int, int]]:
    values: list[tuple[int, int]] = []
    cumulative_log = 0.0
    log_three_halves = math.log(1.5)
    log_two = math.log(2.0)

    for _ in range(max_blocks):
        tail = sample_geometric_half(rng)
        exit_v2 = sample_geometric_half(rng)
        cumulative_log += tail * log_three_halves - exit_v2 * log_two
        values.append((tail, exit_v2))
        if cumulative_log < 0.0:
            break

    return values


def summarize_chain(
    source: str,
    chain_id: int,
    values: list[tuple[int, int]],
    target_prev_exit_v2: int,
) -> tuple[ChainTarget, int, int]:
    target_count = 0
    target_success = 0
    interior_count = 0
    interior_success = 0
    duration = len(values)

    for index, (tail, _exit_v2) in enumerate(values, start=1):
        if position_label(index, duration) != "interior_block":
            continue
        interior_count += 1
        if tail == 1:
            interior_success += 1

        previous_exit_v2 = values[index - 2][1]
        if previous_exit_v2 != target_prev_exit_v2:
            continue
        target_count += 1
        if tail == 1:
            target_success += 1

    return (
        ChainTarget(source=source, chain_id=chain_id, count=target_count, success=target_success),
        interior_count,
        interior_success,
    )


def first_odd_at_least(value: int) -> int:
    return value if value % 2 else value + 1


def count_odd_values(start: int, limit: int) -> int:
    first = first_odd_at_least(start)
    if first > limit:
        return 0
    return ((limit - first) // 2) + 1


def collect_real(
    start: int,
    limit: int,
    max_blocks: int,
    target_prev_exit_v2: int,
) -> tuple[SourceStats, list[ChainTarget]]:
    stats = SourceStats(source="real")
    targets: list[ChainTarget] = []

    for chain_start in range(first_odd_at_least(start), limit + 1, 2):
        chain, interior_count, interior_success = summarize_chain(
            "real",
            chain_start,
            real_chain_values(chain_start, max_blocks),
            target_prev_exit_v2,
        )
        stats.add_chain(chain, interior_count=interior_count, interior_success=interior_success)
        if chain.count:
            targets.append(chain)

    return stats, targets


def collect_model(
    samples: int,
    max_blocks: int,
    seed: int,
    target_prev_exit_v2: int,
) -> tuple[SourceStats, list[ChainTarget]]:
    stats = SourceStats(source="model")
    targets: list[ChainTarget] = []
    rng = random.Random(seed)

    for sample_id in range(samples):
        chain, interior_count, interior_success = summarize_chain(
            "model",
            sample_id,
            model_chain_values(max_blocks, rng),
            target_prev_exit_v2,
        )
        stats.add_chain(chain, interior_count=interior_count, interior_success=interior_success)
        if chain.count:
            targets.append(chain)

    return stats, targets


def normal_two_sided_p(z_score: float) -> float:
    return math.erfc(abs(z_score) / math.sqrt(2.0))


def two_proportion_z(success_a: int, count_a: int, success_b: int, count_b: int) -> tuple[float, float, float]:
    p_a = success_a / count_a if count_a else 0.0
    p_b = success_b / count_b if count_b else 0.0
    se = (
        math.sqrt(p_a * (1.0 - p_a) / count_a + p_b * (1.0 - p_b) / count_b)
        if count_a and count_b
        else 0.0
    )
    diff = p_a - p_b
    z_score = diff / se if se else 0.0
    return diff, se, z_score


def log_choose(n: int, k: int) -> float:
    if k < 0 or k > n:
        return float("-inf")
    return math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)


def logsumexp(values: list[float]) -> float:
    if not values:
        return float("-inf")
    maximum = max(values)
    return maximum + math.log(sum(math.exp(value - maximum) for value in values))


def hypergeometric_tail_p(population: int, successes: int, draws: int, observed_successes: int) -> tuple[float, float]:
    low = max(0, draws - (population - successes))
    high = min(draws, successes)
    denominator = log_choose(population, draws)

    upper_logs = [
        log_choose(successes, k) + log_choose(population - successes, draws - k) - denominator
        for k in range(observed_successes, high + 1)
    ]
    lower_logs = [
        log_choose(successes, k) + log_choose(population - successes, draws - k) - denominator
        for k in range(low, observed_successes + 1)
    ]
    upper = math.exp(logsumexp(upper_logs))
    lower = math.exp(logsumexp(lower_logs))
    return upper, min(1.0, 2.0 * min(upper, lower))


def ratio(success: int, count: int) -> float:
    return success / count if count else 0.0


def source_permutation_and_bootstrap(
    real_targets: list[ChainTarget],
    model_targets: list[ChainTarget],
    observed_diff: float,
    *,
    permutations: int,
    seed: int,
) -> list[dict[str, object]]:
    rng = random.Random(seed)
    combined = [(chain.count, chain.success) for chain in real_targets + model_targets]
    real_chain_count = len(real_targets)
    total_chain_count = len(combined)
    rows: list[dict[str, object]] = []

    for iteration in range(1, permutations + 1):
        real_indices = set(rng.sample(range(total_chain_count), real_chain_count))
        perm_real_count = 0
        perm_real_success = 0
        perm_model_count = 0
        perm_model_success = 0
        for index, (count, success) in enumerate(combined):
            if index in real_indices:
                perm_real_count += count
                perm_real_success += success
            else:
                perm_model_count += count
                perm_model_success += success

        bootstrap_real = [real_targets[rng.randrange(len(real_targets))] for _ in real_targets]
        bootstrap_model = [model_targets[rng.randrange(len(model_targets))] for _ in model_targets]
        boot_real_count = sum(chain.count for chain in bootstrap_real)
        boot_real_success = sum(chain.success for chain in bootstrap_real)
        boot_model_count = sum(chain.count for chain in bootstrap_model)
        boot_model_success = sum(chain.success for chain in bootstrap_model)

        permutation_diff = ratio(perm_real_success, perm_real_count) - ratio(
            perm_model_success,
            perm_model_count,
        )
        bootstrap_diff = ratio(boot_real_success, boot_real_count) - ratio(
            boot_model_success,
            boot_model_count,
        )
        rows.append(
            {
                "iteration": iteration,
                "source_permutation_diff": round(permutation_diff, 10),
                "source_permutation_abs_ge_observed": int(abs(permutation_diff) >= abs(observed_diff)),
                "bootstrap_diff": round(bootstrap_diff, 10),
            }
        )

    return rows


def percentile(sorted_values: list[float], fraction: float) -> float:
    if not sorted_values:
        return 0.0
    index = min(len(sorted_values) - 1, max(0, round(fraction * (len(sorted_values) - 1))))
    return sorted_values[index]


def write_csv(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def count_m13_tests(out_dir: Path) -> tuple[int, list[dict[str, object]]]:
    rows = []
    total = 0
    for path in sorted(out_dir.glob("survival_bias_limit_5000000_*_compare.csv")):
        with path.open(newline="", encoding="utf-8") as handle:
            row_count = sum(1 for _ in csv.DictReader(handle))
        metric_tests = 2 * row_count
        total += metric_tests
        rows.append(
            {
                "source": "m13_compare_csv",
                "file": path.name,
                "rows": row_count,
                "metric_tests": metric_tests,
            }
        )
    return total, rows


def algebraic_local_rows(target_prev_exit_v2: int, max_power: int = 12) -> list[dict[str, object]]:
    rows = []
    for power in range(7, max_power + 1):
        modulus = 1 << power
        period = 1 << max(1, power - 2)
        count = 0
        tail_one_count = 0
        for s in range(1, period + 1):
            three_power = pow(3, s, modulus)
            for q in range(1, modulus, 2):
                value = (three_power * q - 1) % modulus
                if value == 0:
                    valuation = power
                else:
                    valuation = two_adic_valuation(value)
                if valuation != target_prev_exit_v2:
                    continue
                current = ((three_power * q - 1) >> target_prev_exit_v2) % (1 << (power - target_prev_exit_v2))
                count += 1
                if (current + 1) % 4 == 2:
                    tail_one_count += 1
        rows.append(
            {
                "modulus_power": power,
                "modulus": modulus,
                "s_period_used": period,
                "classes_with_prev_exit": count,
                "tail_one_classes": tail_one_count,
                "tail_one_fraction": round(ratio(tail_one_count, count), 8),
            }
        )
    return rows


def main() -> None:
    args = parse_args()
    samples = args.samples if args.samples is not None else count_odd_values(args.start, args.limit)

    real_stats, real_targets = collect_real(args.start, args.limit, args.max_blocks, args.target_prev_exit_v2)
    model_stats, model_targets = collect_model(samples, args.max_blocks, args.seed, args.target_prev_exit_v2)

    observed_diff, observed_se, observed_z = two_proportion_z(
        real_stats.target_success,
        real_stats.target_count,
        model_stats.target_success,
        model_stats.target_count,
    )
    raw_p_two_sided = normal_two_sided_p(observed_z)

    m13_tests, test_count_rows = count_m13_tests(args.out_dir)
    total_tests_conservative = m13_tests + args.extra_tests
    bonferroni_m13 = min(1.0, raw_p_two_sided * m13_tests)
    bonferroni_conservative = min(1.0, raw_p_two_sided * total_tests_conservative)

    real_internal_upper_p, real_internal_two_sided_p = hypergeometric_tail_p(
        real_stats.interior_count,
        real_stats.interior_success,
        real_stats.target_count,
        real_stats.target_success,
    )

    permutation_rows = source_permutation_and_bootstrap(
        real_targets,
        model_targets,
        observed_diff,
        permutations=args.permutations,
        seed=args.seed + 1,
    )
    source_permutation_p = (
        1
        + sum(int(row["source_permutation_abs_ge_observed"]) for row in permutation_rows)
    ) / (args.permutations + 1)
    bootstrap_diffs = sorted(float(row["bootstrap_diff"]) for row in permutation_rows)

    algebra_rows = algebraic_local_rows(args.target_prev_exit_v2)

    summary_rows = [
        {
            "metric": "start",
            "value": args.start,
            "note": "first odd start is adjusted upward if needed",
        },
        {
            "metric": "limit",
            "value": args.limit,
            "note": "odd starts up to limit",
        },
        {
            "metric": "samples",
            "value": samples,
            "note": "independent model chains",
        },
        {
            "metric": "target_condition",
            "value": f"prev_exit_v2={args.target_prev_exit_v2}; current position=interior_block",
            "note": "post-hoc candidate from M13",
        },
        {
            "metric": "real_target_count",
            "value": real_stats.target_count,
            "note": "target transitions",
        },
        {
            "metric": "model_target_count",
            "value": model_stats.target_count,
            "note": "target transitions",
        },
        {
            "metric": "real_tail_one_fraction",
            "value": round(real_stats.target_fraction(), 10),
            "note": "target transitions",
        },
        {
            "metric": "model_tail_one_fraction",
            "value": round(model_stats.target_fraction(), 10),
            "note": "target transitions",
        },
        {
            "metric": "diff_real_minus_model",
            "value": round(observed_diff, 10),
            "note": "tail_one fraction difference",
        },
        {
            "metric": "normal_z",
            "value": round(observed_z, 8),
            "note": "two-proportion normal approximation",
        },
        {
            "metric": "normal_two_sided_p",
            "value": f"{raw_p_two_sided:.12g}",
            "note": "unadjusted p-value",
        },
        {
            "metric": "m13_metric_tests",
            "value": m13_tests,
            "note": "rows in M13 compare CSVs times two metrics",
        },
        {
            "metric": "extra_exploratory_tests",
            "value": args.extra_tests,
            "note": "default is bucket count from codex-hijo/m14-residuos summary",
        },
        {
            "metric": "total_tests_conservative",
            "value": total_tests_conservative,
            "note": "M13 tests plus extra exploratory tests",
        },
        {
            "metric": "bonferroni_m13_p",
            "value": f"{bonferroni_m13:.12g}",
            "note": "normal p times M13 metric tests",
        },
        {
            "metric": "bonferroni_conservative_p",
            "value": f"{bonferroni_conservative:.12g}",
            "note": "normal p times M13 plus extra exploratory tests",
        },
        {
            "metric": "source_chain_permutation_p",
            "value": f"{source_permutation_p:.12g}",
            "note": "permutes real/model labels among target-containing chains",
        },
        {
            "metric": "bootstrap_diff_ci95_low",
            "value": round(percentile(bootstrap_diffs, 0.025), 10),
            "note": "cluster bootstrap over target-containing chains",
        },
        {
            "metric": "bootstrap_diff_ci95_high",
            "value": round(percentile(bootstrap_diffs, 0.975), 10),
            "note": "cluster bootstrap over target-containing chains",
        },
        {
            "metric": "real_internal_hypergeom_upper_p",
            "value": f"{real_internal_upper_p:.12g}",
            "note": "P(X>=observed) among real interior transitions",
        },
        {
            "metric": "real_internal_hypergeom_two_sided_p",
            "value": f"{real_internal_two_sided_p:.12g}",
            "note": "tests whether target is special inside real interior transitions",
        },
        {
            "metric": "algebra_local_tail_one_fraction_mod_128",
            "value": algebra_rows[0]["tail_one_fraction"],
            "note": "unconditional local congruence prediction",
        },
    ]

    args.out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        args.out_dir / f"{args.prefix}_summary.csv",
        summary_rows,
        ["metric", "value", "note"],
    )
    write_csv(
        args.out_dir / f"{args.prefix}_test_counts.csv",
        test_count_rows
        + [
            {
                "source": "codex_hijo_branch_summary",
                "file": "codex-hijo/m14-residuos:reports/m14_residue_summary.csv",
                "rows": args.extra_tests,
                "metric_tests": args.extra_tests,
            }
        ],
        ["source", "file", "rows", "metric_tests"],
    )
    write_csv(
        args.out_dir / f"{args.prefix}_permutation.csv",
        permutation_rows,
        ["iteration", "source_permutation_diff", "source_permutation_abs_ge_observed", "bootstrap_diff"],
    )
    write_csv(
        args.out_dir / f"{args.prefix}_algebra.csv",
        algebra_rows,
        [
            "modulus_power",
            "modulus",
            "s_period_used",
            "classes_with_prev_exit",
            "tail_one_classes",
            "tail_one_fraction",
        ],
    )

    print(f"limit={args.limit}")
    print(f"start={args.start}")
    print(f"samples={samples}")
    print(f"target_prev_exit_v2={args.target_prev_exit_v2}")
    print(f"real={real_stats.target_success}/{real_stats.target_count}={real_stats.target_fraction():.8f}")
    print(f"model={model_stats.target_success}/{model_stats.target_count}={model_stats.target_fraction():.8f}")
    print(f"diff={observed_diff:.8f}")
    print(f"normal_two_sided_p={raw_p_two_sided:.12g}")
    print(f"bonferroni_m13_p={bonferroni_m13:.12g}")
    print(f"bonferroni_conservative_p={bonferroni_conservative:.12g}")
    print(f"source_chain_permutation_p={source_permutation_p:.12g}")
    print(
        "bootstrap_ci95="
        f"[{percentile(bootstrap_diffs, 0.025):.8f}, {percentile(bootstrap_diffs, 0.975):.8f}]"
    )
    print(f"real_internal_hypergeom_upper_p={real_internal_upper_p:.12g}")
    print(f"algebra_local_mod128_tail_one_fraction={algebra_rows[0]['tail_one_fraction']}")


if __name__ == "__main__":
    main()
