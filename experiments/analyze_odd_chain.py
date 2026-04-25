from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from collatz import alternating_block, mersenne_tail_length  # noqa: E402


@dataclass(frozen=True)
class ChainResult:
    n: int
    initial_tail: int
    status: str
    blocks: int
    expansive_blocks: int
    long_tail_hits: int
    max_tail_seen: int
    terminal_odd: int
    max_odd_ratio: float
    max_peak_ratio: float


@dataclass
class InitialTailStats:
    initial_tail: int
    count: int = 0
    drop_count: int = 0
    one_count: int = 0
    maxed_count: int = 0
    blocks_sum: int = 0
    expansive_blocks_sum: int = 0
    long_tail_hits_sum: int = 0
    max_tail_seen_sum: int = 0
    max_odd_ratio_sum: float = 0.0
    max_peak_ratio_sum: float = 0.0
    max_blocks: int = -1
    argmax_blocks: int = -1
    max_odd_ratio_record: float = -1.0
    argmax_max_odd_ratio: int = -1
    max_peak_ratio_record: float = -1.0
    argmax_max_peak_ratio: int = -1
    max_tail_seen_record: int = -1
    argmax_max_tail_seen: int = -1

    def add(self, result: ChainResult) -> None:
        self.count += 1
        if result.status == "drop":
            self.drop_count += 1
        elif result.status == "one":
            self.one_count += 1
        elif result.status == "maxed":
            self.maxed_count += 1

        self.blocks_sum += result.blocks
        self.expansive_blocks_sum += result.expansive_blocks
        self.long_tail_hits_sum += result.long_tail_hits
        self.max_tail_seen_sum += result.max_tail_seen
        self.max_odd_ratio_sum += result.max_odd_ratio
        self.max_peak_ratio_sum += result.max_peak_ratio

        if result.blocks > self.max_blocks:
            self.max_blocks = result.blocks
            self.argmax_blocks = result.n

        if result.max_odd_ratio > self.max_odd_ratio_record:
            self.max_odd_ratio_record = result.max_odd_ratio
            self.argmax_max_odd_ratio = result.n

        if result.max_peak_ratio > self.max_peak_ratio_record:
            self.max_peak_ratio_record = result.max_peak_ratio
            self.argmax_max_peak_ratio = result.n

        if result.max_tail_seen > self.max_tail_seen_record:
            self.max_tail_seen_record = result.max_tail_seen
            self.argmax_max_tail_seen = result.n

    def as_row(self) -> dict[str, object]:
        return {
            "initial_tail": self.initial_tail,
            "count": self.count,
            "drop_fraction": round(self.drop_count / self.count, 8),
            "one_fraction": round(self.one_count / self.count, 8),
            "maxed_fraction": round(self.maxed_count / self.count, 8),
            "avg_blocks": round(self.blocks_sum / self.count, 6),
            "avg_expansive_blocks": round(self.expansive_blocks_sum / self.count, 6),
            "avg_long_tail_hits": round(self.long_tail_hits_sum / self.count, 6),
            "avg_max_tail_seen": round(self.max_tail_seen_sum / self.count, 6),
            "avg_max_odd_ratio": round(self.max_odd_ratio_sum / self.count, 6),
            "avg_max_peak_ratio": round(self.max_peak_ratio_sum / self.count, 6),
            "max_blocks": self.max_blocks,
            "argmax_blocks": self.argmax_blocks,
            "max_odd_ratio_record": round(self.max_odd_ratio_record, 6),
            "argmax_max_odd_ratio": self.argmax_max_odd_ratio,
            "max_peak_ratio_record": round(self.max_peak_ratio_record, 6),
            "argmax_max_peak_ratio": self.argmax_max_peak_ratio,
            "max_tail_seen_record": self.max_tail_seen_record,
            "argmax_max_tail_seen": self.argmax_max_tail_seen,
        }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Analyze odd-to-odd chains built from alternating Collatz blocks."
    )
    parser.add_argument("--limit", type=int, default=1_000_000)
    parser.add_argument("--max-blocks", type=int, default=256)
    parser.add_argument("--long-tail-threshold", type=int, default=9)
    parser.add_argument("--records", type=int, default=40)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="odd_chain_limit_1000000")
    return parser.parse_args()


def write_csv(rows: list[dict[str, object]], path: Path, fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def analyze_start(
    n: int,
    *,
    max_blocks: int,
    long_tail_threshold: int,
    transitions: Counter[tuple[int, int]],
) -> ChainResult:
    initial_tail = mersenne_tail_length(n)
    current = n
    max_odd = n
    max_peak = n
    max_tail_seen = initial_tail
    expansive_blocks = 0
    long_tail_hits = 1 if initial_tail >= long_tail_threshold else 0

    for block_index in range(1, max_blocks + 1):
        block = alternating_block(current)
        next_odd = block.next_odd
        next_tail = mersenne_tail_length(next_odd)
        transitions[(block.tail_length, next_tail)] += 1

        if next_odd > current:
            expansive_blocks += 1
        if next_tail >= long_tail_threshold:
            long_tail_hits += 1

        current = next_odd
        max_odd = max(max_odd, current)
        max_peak = max(max_peak, block.block_peak)
        max_tail_seen = max(max_tail_seen, next_tail)

        if current == 1:
            return ChainResult(
                n=n,
                initial_tail=initial_tail,
                status="one",
                blocks=block_index,
                expansive_blocks=expansive_blocks,
                long_tail_hits=long_tail_hits,
                max_tail_seen=max_tail_seen,
                terminal_odd=current,
                max_odd_ratio=max_odd / n,
                max_peak_ratio=max_peak / n,
            )

        if current < n:
            return ChainResult(
                n=n,
                initial_tail=initial_tail,
                status="drop",
                blocks=block_index,
                expansive_blocks=expansive_blocks,
                long_tail_hits=long_tail_hits,
                max_tail_seen=max_tail_seen,
                terminal_odd=current,
                max_odd_ratio=max_odd / n,
                max_peak_ratio=max_peak / n,
            )

    return ChainResult(
        n=n,
        initial_tail=initial_tail,
        status="maxed",
        blocks=max_blocks,
        expansive_blocks=expansive_blocks,
        long_tail_hits=long_tail_hits,
        max_tail_seen=max_tail_seen,
        terminal_odd=current,
        max_odd_ratio=max_odd / n,
        max_peak_ratio=max_peak / n,
    )


def analyze(
    *,
    limit: int,
    max_blocks: int,
    long_tail_threshold: int,
    record_count: int,
) -> tuple[
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
    list[dict[str, object]],
]:
    if limit < 3:
        raise ValueError("limit must be at least 3")
    if max_blocks < 1:
        raise ValueError("max_blocks must be positive")
    if long_tail_threshold < 1:
        raise ValueError("long_tail_threshold must be positive")

    by_initial_tail: dict[int, InitialTailStats] = {}
    block_counts: Counter[tuple[str, int]] = Counter()
    transitions: Counter[tuple[int, int]] = Counter()
    results: list[ChainResult] = []

    for n in range(3, limit + 1, 2):
        result = analyze_start(
            n,
            max_blocks=max_blocks,
            long_tail_threshold=long_tail_threshold,
            transitions=transitions,
        )
        by_initial_tail.setdefault(
            result.initial_tail,
            InitialTailStats(initial_tail=result.initial_tail),
        ).add(result)
        block_counts[(result.status, result.blocks)] += 1
        results.append(result)

    by_initial_tail_rows = [
        by_initial_tail[key].as_row()
        for key in sorted(by_initial_tail)
    ]

    total = len(results)
    block_count_rows = [
        {
            "status": status,
            "blocks": blocks,
            "count": count,
            "fraction": round(count / total, 8),
        }
        for (status, blocks), count in sorted(block_counts.items(), key=lambda item: (item[0][0], item[0][1]))
    ]

    transition_total = sum(transitions.values())
    transition_rows = [
        {
            "tail": tail,
            "next_tail": next_tail,
            "count": count,
            "fraction": round(count / transition_total, 8),
        }
        for (tail, next_tail), count in sorted(transitions.items())
    ]

    record_specs = [
        (
            "blocks",
            lambda row: (
                row.blocks,
                row.max_peak_ratio,
                row.max_odd_ratio,
                row.max_tail_seen,
            ),
        ),
        (
            "max_peak_ratio",
            lambda row: (
                row.max_peak_ratio,
                row.max_odd_ratio,
                row.blocks,
                row.max_tail_seen,
            ),
        ),
        (
            "max_odd_ratio",
            lambda row: (
                row.max_odd_ratio,
                row.max_peak_ratio,
                row.blocks,
                row.max_tail_seen,
            ),
        ),
        (
            "max_tail_seen",
            lambda row: (
                row.max_tail_seen,
                row.blocks,
                row.max_peak_ratio,
                row.max_odd_ratio,
            ),
        ),
    ]
    record_rows = []
    for metric, key_func in record_specs:
        for rank, result in enumerate(
            sorted(results, key=key_func, reverse=True)[:record_count],
            start=1,
        ):
            record_rows.append(
                {
                    "rank_metric": metric,
                    "rank": rank,
                    "n": result.n,
                    "initial_tail": result.initial_tail,
                    "status": result.status,
                    "blocks": result.blocks,
                    "expansive_blocks": result.expansive_blocks,
                    "long_tail_hits": result.long_tail_hits,
                    "max_tail_seen": result.max_tail_seen,
                    "terminal_odd": result.terminal_odd,
                    "max_odd_ratio": round(result.max_odd_ratio, 6),
                    "max_peak_ratio": round(result.max_peak_ratio, 6),
                }
            )

    return by_initial_tail_rows, block_count_rows, transition_rows, record_rows


def main() -> int:
    args = parse_args()
    by_tail_rows, block_count_rows, transition_rows, record_rows = analyze(
        limit=args.limit,
        max_blocks=args.max_blocks,
        long_tail_threshold=args.long_tail_threshold,
        record_count=args.records,
    )

    by_tail_path = args.out_dir / f"{args.prefix}_by_initial_tail.csv"
    blocks_path = args.out_dir / f"{args.prefix}_blocks_to_stop.csv"
    transitions_path = args.out_dir / f"{args.prefix}_tail_transitions.csv"
    records_path = args.out_dir / f"{args.prefix}_records.csv"

    write_csv(
        by_tail_rows,
        by_tail_path,
        [
            "initial_tail",
            "count",
            "drop_fraction",
            "one_fraction",
            "maxed_fraction",
            "avg_blocks",
            "avg_expansive_blocks",
            "avg_long_tail_hits",
            "avg_max_tail_seen",
            "avg_max_odd_ratio",
            "avg_max_peak_ratio",
            "max_blocks",
            "argmax_blocks",
            "max_odd_ratio_record",
            "argmax_max_odd_ratio",
            "max_peak_ratio_record",
            "argmax_max_peak_ratio",
            "max_tail_seen_record",
            "argmax_max_tail_seen",
        ],
    )
    write_csv(block_count_rows, blocks_path, ["status", "blocks", "count", "fraction"])
    write_csv(transition_rows, transitions_path, ["tail", "next_tail", "count", "fraction"])
    write_csv(
        record_rows,
        records_path,
        [
            "rank_metric",
            "rank",
            "n",
            "initial_tail",
            "status",
            "blocks",
            "expansive_blocks",
            "long_tail_hits",
            "max_tail_seen",
            "terminal_odd",
            "max_odd_ratio",
            "max_peak_ratio",
        ],
    )

    print(f"limit={args.limit}")
    print(f"max_blocks={args.max_blocks}")
    print(f"by_initial_tail={by_tail_path}")
    print(f"blocks_to_stop={blocks_path}")
    print(f"tail_transitions={transitions_path}")
    print(f"records={records_path}")

    for row in by_tail_rows[:12]:
        print(
            f"s={row['initial_tail']} count={row['count']} "
            f"avg_blocks={row['avg_blocks']} max_blocks={row['max_blocks']} "
            f"avg_peak={row['avg_max_peak_ratio']} max_tail={row['max_tail_seen_record']}"
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
