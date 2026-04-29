from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path


def collatz_t(n: int) -> int:
    """Angeltveit's accelerated T map."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


@dataclass(frozen=True)
class OrbitPrefix:
    value: int
    odd_steps: int


def iterate_prefix(n: int, steps: int) -> OrbitPrefix:
    odd_steps = 0
    value = n
    for _ in range(steps):
        if value % 2:
            odd_steps += 1
        value = collatz_t(value)
    return OrbitPrefix(value=value, odd_steps=odd_steps)


def lowbit_certified_residues(k: int) -> set[int]:
    """Residues whose first k T-steps force descent for every positive lift."""
    modulus = 1 << k
    certified: set[int] = set()
    for residue in range(modulus):
        prefix = iterate_prefix(residue, k)
        contraction = 3 ** prefix.odd_steps < modulus
        residue_descends = residue == 0 or prefix.value < residue
        if contraction and residue_descends:
            certified.add(residue)
    return certified


def first_descent_time(n: int, max_steps: int) -> int | None:
    value = n
    for step in range(1, max_steps + 1):
        value = collatz_t(value)
        if value < n:
            return step
    return None


def has_lower_mod3_preimage(n: int) -> bool:
    """Safe one-step preimage sieve: if n == T(m) for m < n, n is redundant."""
    if n % 3 != 2:
        return False
    predecessor = (2 * n - 1) // 3
    return predecessor > 0 and predecessor < n and predecessor % 2 == 1


def validate_certificate(n: int, k: int) -> bool:
    return iterate_prefix(n, k).value < n


def analyze(max_power: int, ks: list[int], naive_steps: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    total_by_power: dict[int, int] = {power: (1 << power) - 1 for power in range(2, max_power + 1)}
    residue_cache = {k: lowbit_certified_residues(k) for k in ks}

    for power in range(2, max_power + 1):
        limit = 1 << power
        mod3_preimage = 0
        naive_descends = 0
        for n in range(1, limit):
            if has_lower_mod3_preimage(n):
                mod3_preimage += 1
            if first_descent_time(n, naive_steps) is not None:
                naive_descends += 1

        for k in ks:
            modulus = 1 << k
            certified_residues = residue_cache[k]
            certified_numbers = 0
            false_positives = 0
            for n in range(1, limit):
                if n % modulus not in certified_residues:
                    continue
                certified_numbers += 1
                if not validate_certificate(n, k):
                    false_positives += 1

            total = total_by_power[power]
            rows.append(
                {
                    "max_power": power,
                    "limit_exclusive": limit,
                    "k": k,
                    "total_positive_n": total,
                    "certified_residue_count": len(certified_residues),
                    "residue_modulus": modulus,
                    "lowbit_certified_n": certified_numbers,
                    "lowbit_certified_fraction": f"{certified_numbers / total:.12f}",
                    "false_positives": false_positives,
                    "mod3_preimage_n": mod3_preimage,
                    "mod3_preimage_fraction": f"{mod3_preimage / total:.12f}",
                    "naive_descends_within_steps": naive_descends,
                    "naive_steps": naive_steps,
                }
            )
    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = [
        "max_power",
        "limit_exclusive",
        "k",
        "total_positive_n",
        "certified_residue_count",
        "residue_modulus",
        "lowbit_certified_n",
        "lowbit_certified_fraction",
        "false_positives",
        "mod3_preimage_n",
        "mod3_preimage_fraction",
        "naive_descends_within_steps",
        "naive_steps",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    lines = [
        "# M21 Angeltveit low-bit probe",
        "",
        "This is a small independent probe of the low-bit descent idea, not a GPU reproduction",
        "and not a proof of Collatz. A row is useful only if `false_positives = 0`.",
        "",
        "| N | k | certified residues | certified n | certified fraction | false positives | mod3 preimage fraction |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {max_power} | {k} | {certified_residue_count}/{residue_modulus} | "
            "{lowbit_certified_n}/{total_positive_n} | {lowbit_certified_fraction} | "
            "{false_positives} | {mod3_preimage_fraction} |".format(**row)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Small low-bit descent probe inspired by Angeltveit 2026."
    )
    parser.add_argument("--max-power", type=int, default=20)
    parser.add_argument("--ks", default="8,10,12,14,16")
    parser.add_argument("--naive-steps", type=int, default=256)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m21_angeltveit_lowbit_probe")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.max_power < 2:
        raise ValueError("--max-power must be at least 2")
    ks = [int(part) for part in args.ks.split(",") if part.strip()]
    if not ks or min(ks) < 1:
        raise ValueError("--ks must contain positive integers")
    if max(ks) > 20:
        raise ValueError("This probe is intentionally small; keep k <= 20.")

    rows = analyze(max_power=args.max_power, ks=ks, naive_steps=args.naive_steps)
    csv_path = args.out_dir / f"{args.prefix}.csv"
    md_path = args.out_dir / f"{args.prefix}.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    max_false = max(int(row["false_positives"]) for row in rows)
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    print(f"rows={len(rows)}")
    print(f"max_false_positives={max_false}")
    return 0 if max_false == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
