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


def count_residue_hits(limit_exclusive: int, modulus: int, residues: set[int]) -> int:
    """Count positive n < limit_exclusive whose residue modulo modulus is selected."""
    if limit_exclusive <= 1:
        return 0
    top = limit_exclusive - 1
    hits = 0
    for residue in residues:
        if residue == 0:
            hits += top // modulus
        elif residue <= top:
            hits += ((top - residue) // modulus) + 1
    return hits


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


def stratified_values(low: int, high: int, count: int) -> list[int]:
    """Deterministic low/mid/high-ish samples from an inclusive interval."""
    if count <= 0 or low > high:
        return []
    if count == 1:
        return [(low + high) // 2]
    if count == 2:
        return sorted({low, high})
    if low == high:
        return [low]
    return sorted({low + ((high - low) * index) // (count - 1) for index in range(count)})


def select_residue_samples(
    modulus: int,
    selected: set[int],
    *,
    want_selected: bool,
    strata: int,
    per_stratum: int,
) -> list[int]:
    """Sample residues from each interval stratum, split by certificate status."""
    samples: set[int] = set()
    for stratum in range(strata):
        low = (stratum * modulus) // strata
        high = (((stratum + 1) * modulus) // strata) - 1
        matches = [
            residue
            for residue in range(low, high + 1)
            if (residue in selected) == want_selected
        ]
        for index in stratified_values(0, len(matches) - 1, per_stratum):
            samples.add(matches[index])
    return sorted(samples)


def audit_stratified_samples(
    k: int,
    certified_residues: set[int],
    *,
    max_power: int,
    residue_strata: int,
    residues_per_stratum: int,
    lifts_per_residue: int,
) -> dict[str, object]:
    """Check affine low-bit invariants on certified and uncertified strata."""
    modulus = 1 << k
    limit = 1 << max_power
    certified_samples = select_residue_samples(
        modulus,
        certified_residues,
        want_selected=True,
        strata=residue_strata,
        per_stratum=residues_per_stratum,
    )
    uncertified_samples = select_residue_samples(
        modulus,
        certified_residues,
        want_selected=False,
        strata=residue_strata,
        per_stratum=residues_per_stratum,
    )

    affine_failures = 0
    certified_false_positives = 0
    uncertified_sample_descents = 0
    sampled_numbers = 0
    max_lift_seen = 0

    for is_certified, residues in ((True, certified_samples), (False, uncertified_samples)):
        for residue in residues:
            max_lift = (limit - 1 - residue) // modulus
            min_lift = 1 if residue == 0 else 0
            if max_lift < min_lift:
                continue
            prefix = iterate_prefix(residue, k)
            multiplier = 3 ** prefix.odd_steps
            for lift in stratified_values(min_lift, max_lift, lifts_per_residue):
                n = residue + lift * modulus
                lifted = iterate_prefix(n, k)
                expected = prefix.value + multiplier * lift
                sampled_numbers += 1
                max_lift_seen = max(max_lift_seen, lift)
                if lifted.value != expected:
                    affine_failures += 1
                descends = lifted.value < n
                if is_certified and not descends:
                    certified_false_positives += 1
                if not is_certified and descends:
                    uncertified_sample_descents += 1

    certified_slacks = []
    descent_slacks = []
    for residue in certified_residues:
        prefix = iterate_prefix(residue, k)
        certified_slacks.append(modulus - (3 ** prefix.odd_steps))
        if residue > 0:
            descent_slacks.append(residue - prefix.value)

    return {
        "k": k,
        "audit_max_power": max_power,
        "residue_strata": residue_strata,
        "residues_per_stratum": residues_per_stratum,
        "lifts_per_residue": lifts_per_residue,
        "certified_residue_samples": len(certified_samples),
        "uncertified_residue_samples": len(uncertified_samples),
        "sampled_numbers": sampled_numbers,
        "max_lift_seen": max_lift_seen,
        "affine_failures": affine_failures,
        "certified_false_positives": certified_false_positives,
        "uncertified_sample_descents": uncertified_sample_descents,
        "min_contraction_slack": min(certified_slacks) if certified_slacks else "",
        "min_descent_slack": min(descent_slacks) if descent_slacks else "",
    }


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
            certified_numbers = count_residue_hits(limit, modulus, certified_residues)
            false_positives = 0
            for n in range(1, limit):
                if n % modulus not in certified_residues:
                    continue
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
                    "certified_residue_fraction": f"{len(certified_residues) / modulus:.12f}",
                    "lowbit_certified_n": certified_numbers,
                    "lowbit_certified_fraction": f"{certified_numbers / total:.12f}",
                    "false_positives": false_positives,
                    "mod3_preimage_n": mod3_preimage,
                    "mod3_preimage_fraction": f"{mod3_preimage / total:.12f}",
                    "naive_descends_within_steps": naive_descends,
                    "naive_steps": naive_steps,
                    "residue_evaluations": modulus,
                    "residue_orbit_steps": k * modulus,
                    "coverage_count_terms": len(certified_residues),
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
        "certified_residue_fraction",
        "lowbit_certified_n",
        "lowbit_certified_fraction",
        "false_positives",
        "mod3_preimage_n",
        "mod3_preimage_fraction",
        "naive_descends_within_steps",
        "naive_steps",
        "residue_evaluations",
        "residue_orbit_steps",
        "coverage_count_terms",
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
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def write_audit_csv(rows: list[dict[str, object]], path: Path) -> None:
    fieldnames = [
        "k",
        "audit_max_power",
        "residue_strata",
        "residues_per_stratum",
        "lifts_per_residue",
        "certified_residue_samples",
        "uncertified_residue_samples",
        "sampled_numbers",
        "max_lift_seen",
        "affine_failures",
        "certified_false_positives",
        "uncertified_sample_descents",
        "min_contraction_slack",
        "min_descent_slack",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_audit_markdown(rows: list[dict[str, object]], path: Path) -> None:
    lines = [
        "# M21 Angeltveit low-bit stratified audit",
        "",
        "Deterministic second-layer audit for the low-bit certificate. It samples certified",
        "and uncertified residue strata, then checks the affine invariant",
        "`T^k(r + a 2^k) = T^k(r) + 3^f a` on low/mid/high lifts.",
        "",
        "This raises reproducibility and catches implementation mistakes; it is not a new",
        "Collatz proof and not a reproduction of the full Angeltveit GPU search.",
        "",
        "| k | residue samples C/U | n samples | max lift | affine failures | certified false positives | uncertified sampled descents | min contraction slack | min descent slack |",
        "| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {k} | {certified_residue_samples}/{uncertified_residue_samples} | "
            "{sampled_numbers} | {max_lift_seen} | {affine_failures} | "
            "{certified_false_positives} | {uncertified_sample_descents} | "
            "{min_contraction_slack} | {min_descent_slack} |".format(**row)
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Small low-bit descent probe inspired by Angeltveit 2026."
    )
    parser.add_argument("--max-power", type=int, default=20)
    parser.add_argument("--ks", default="8,10,12,14,16,18,20")
    parser.add_argument("--naive-steps", type=int, default=256)
    parser.add_argument("--audit-max-power", type=int, default=24)
    parser.add_argument("--residue-strata", type=int, default=16)
    parser.add_argument("--residues-per-stratum", type=int, default=3)
    parser.add_argument("--lifts-per-residue", type=int, default=3)
    parser.add_argument("--no-audit", action="store_true")
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
    if args.audit_max_power < max(ks):
        raise ValueError("--audit-max-power must be at least max(k) so sampled lifts exist.")

    rows = analyze(max_power=args.max_power, ks=ks, naive_steps=args.naive_steps)
    csv_path = args.out_dir / f"{args.prefix}.csv"
    md_path = args.out_dir / f"{args.prefix}.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    max_false = max(int(row["false_positives"]) for row in rows)
    audit_max_false = 0
    audit_max_affine = 0
    if not args.no_audit:
        residue_cache = {k: lowbit_certified_residues(k) for k in ks}
        audit_rows = [
            audit_stratified_samples(
                k,
                residue_cache[k],
                max_power=args.audit_max_power,
                residue_strata=args.residue_strata,
                residues_per_stratum=args.residues_per_stratum,
                lifts_per_residue=args.lifts_per_residue,
            )
            for k in ks
        ]
        audit_csv_path = args.out_dir / f"{args.prefix}_audit.csv"
        audit_md_path = args.out_dir / f"{args.prefix}_audit.md"
        write_audit_csv(audit_rows, audit_csv_path)
        write_audit_markdown(audit_rows, audit_md_path)
        audit_max_false = max(int(row["certified_false_positives"]) for row in audit_rows)
        audit_max_affine = max(int(row["affine_failures"]) for row in audit_rows)
        print(f"audit_csv={audit_csv_path}")
        print(f"audit_md={audit_md_path}")
        print(f"audit_rows={len(audit_rows)}")
        print(f"audit_affine_failures={audit_max_affine}")
        print(f"audit_certified_false_positives={audit_max_false}")
    print(f"csv={csv_path}")
    print(f"md={md_path}")
    print(f"rows={len(rows)}")
    print(f"max_false_positives={max_false}")
    return 0 if max_false == 0 and audit_max_false == 0 and audit_max_affine == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
