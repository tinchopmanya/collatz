from __future__ import annotations

import argparse
import csv
import hashlib
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


BRANCH_NAME = "S2_without_tf_end_to_end"
REMOVED_RULE = "bad -> d"
PAPER_RULE = "tf* -> *"
PREDICATE = "residue_mod_8_eq_5"


@dataclass(frozen=True)
class Prefix:
    value: int
    odd_steps: int


@dataclass(frozen=True)
class RecheckResult:
    k: int
    modulus: int
    branch_residues: tuple[int, ...]
    certified_residues: tuple[int, ...]
    uncovered_residues: tuple[int, ...]


@dataclass(frozen=True)
class ExhaustiveValidation:
    limit_exclusive: int
    checked_candidates: int
    false_positives: int


@dataclass(frozen=True)
class StratifiedAudit:
    audit_max_power: int
    residue_strata: int
    residues_per_stratum: int
    lifts_per_residue: int
    certified_residue_samples: int
    uncovered_residue_samples: int
    sampled_numbers: int
    max_lift_seen: int
    affine_failures: int
    certified_false_positives: int
    uncovered_sample_descents: int
    min_contraction_slack: int
    min_descent_slack: int


def accelerated_t(n: int) -> int:
    """Accelerated Collatz map T used by the low-bit certificate."""
    if n < 0:
        raise ValueError("n must be non-negative")
    if n % 2 == 0:
        return n // 2
    return (3 * n + 1) // 2


def iterate_prefix(n: int, steps: int) -> Prefix:
    if steps < 0:
        raise ValueError("steps must be non-negative")
    value = n
    odd_steps = 0
    for _ in range(steps):
        if value % 2:
            odd_steps += 1
        value = accelerated_t(value)
    return Prefix(value=value, odd_steps=odd_steps)


def s2_branch_contains(residue: int) -> bool:
    return residue % 8 == 5


def lowbit_certificate_holds(residue: int, k: int) -> bool:
    """Return whether residue modulo 2^k forces descent for every positive lift."""
    modulus = 1 << k
    prefix = iterate_prefix(residue, k)
    multiplier = 3**prefix.odd_steps
    contracts_all_lifts = multiplier < modulus
    residue_descends = residue == 0 or prefix.value < residue
    return contracts_all_lifts and residue_descends


def recheck_s2(k: int = 16) -> RecheckResult:
    if k < 3:
        raise ValueError("k must be at least 3 for the S2 mod-8 branch")
    modulus = 1 << k
    branch = tuple(residue for residue in range(modulus) if s2_branch_contains(residue))
    certified = tuple(residue for residue in branch if lowbit_certificate_holds(residue, k))
    certified_set = set(certified)
    uncovered = tuple(residue for residue in branch if residue not in certified_set)
    return RecheckResult(
        k=k,
        modulus=modulus,
        branch_residues=branch,
        certified_residues=certified,
        uncovered_residues=uncovered,
    )


def residue_digest(residues: Sequence[int]) -> str:
    payload = "\n".join(str(residue) for residue in residues) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def bitstring(residue: int, k: int, *, lsb_first: bool) -> str:
    bits = format(residue, f"0{k}b")
    return bits[::-1] if lsb_first else bits


def trie_node_count(words: Iterable[str]) -> int:
    trie: dict[str, dict[str, object]] = {}
    count = 1
    for word in words:
        node: dict[str, object] = trie
        for char in word:
            child = node.get(char)
            if child is None:
                child = {}
                node[char] = child
                count += 1
            node = child  # type: ignore[assignment]
    return count


def stratified_values(low: int, high: int, count: int) -> list[int]:
    if count <= 0 or low > high:
        return []
    if low == high:
        return [low]
    if count == 1:
        return [(low + high) // 2]
    return sorted({low + ((high - low) * index) // (count - 1) for index in range(count)})


def select_residue_samples(
    candidates: Sequence[int],
    *,
    modulus: int,
    strata: int,
    per_stratum: int,
) -> tuple[int, ...]:
    if strata <= 0:
        raise ValueError("strata must be positive")
    by_stratum: list[list[int]] = [[] for _ in range(strata)]
    for residue in candidates:
        index = min((residue * strata) // modulus, strata - 1)
        by_stratum[index].append(residue)

    samples: set[int] = set()
    for matches in by_stratum:
        for index in stratified_values(0, len(matches) - 1, per_stratum):
            samples.add(matches[index])
    return tuple(sorted(samples))


def validate_exhaustive(
    result: RecheckResult,
    *,
    limit_exclusive: int = 1 << 20,
) -> ExhaustiveValidation:
    if limit_exclusive <= 1:
        return ExhaustiveValidation(
            limit_exclusive=limit_exclusive,
            checked_candidates=0,
            false_positives=0,
        )
    certified = set(result.certified_residues)
    checked = 0
    false_positives = 0
    for n in range(1, limit_exclusive):
        if n % result.modulus not in certified:
            continue
        checked += 1
        if iterate_prefix(n, result.k).value >= n:
            false_positives += 1
    return ExhaustiveValidation(
        limit_exclusive=limit_exclusive,
        checked_candidates=checked,
        false_positives=false_positives,
    )


def audit_stratified(
    result: RecheckResult,
    *,
    audit_max_power: int = 24,
    residue_strata: int = 32,
    residues_per_stratum: int = 3,
    lifts_per_residue: int = 3,
) -> StratifiedAudit:
    if audit_max_power < result.k:
        raise ValueError("audit_max_power must be at least k")

    limit = 1 << audit_max_power
    certified_samples = select_residue_samples(
        result.certified_residues,
        modulus=result.modulus,
        strata=residue_strata,
        per_stratum=residues_per_stratum,
    )
    uncovered_samples = select_residue_samples(
        result.uncovered_residues,
        modulus=result.modulus,
        strata=residue_strata,
        per_stratum=residues_per_stratum,
    )

    sampled_numbers = 0
    max_lift_seen = 0
    affine_failures = 0
    certified_false_positives = 0
    uncovered_sample_descents = 0

    for is_certified, residues in (
        (True, certified_samples),
        (False, uncovered_samples),
    ):
        for residue in residues:
            prefix = iterate_prefix(residue, result.k)
            multiplier = 3**prefix.odd_steps
            max_lift = (limit - 1 - residue) // result.modulus
            min_lift = 1 if residue == 0 else 0
            for lift in stratified_values(min_lift, max_lift, lifts_per_residue):
                n = residue + lift * result.modulus
                lifted = iterate_prefix(n, result.k)
                expected = prefix.value + multiplier * lift
                sampled_numbers += 1
                max_lift_seen = max(max_lift_seen, lift)
                if lifted.value != expected:
                    affine_failures += 1
                descends = lifted.value < n
                if is_certified and not descends:
                    certified_false_positives += 1
                if not is_certified and descends:
                    uncovered_sample_descents += 1

    contraction_slacks: list[int] = []
    descent_slacks: list[int] = []
    for residue in result.certified_residues:
        prefix = iterate_prefix(residue, result.k)
        contraction_slacks.append(result.modulus - (3**prefix.odd_steps))
        descent_slacks.append(residue - prefix.value)

    return StratifiedAudit(
        audit_max_power=audit_max_power,
        residue_strata=residue_strata,
        residues_per_stratum=residues_per_stratum,
        lifts_per_residue=lifts_per_residue,
        certified_residue_samples=len(certified_samples),
        uncovered_residue_samples=len(uncovered_samples),
        sampled_numbers=sampled_numbers,
        max_lift_seen=max_lift_seen,
        affine_failures=affine_failures,
        certified_false_positives=certified_false_positives,
        uncovered_sample_descents=uncovered_sample_descents,
        min_contraction_slack=min(contraction_slacks),
        min_descent_slack=min(descent_slacks),
    )


def summary_row(
    result: RecheckResult,
    validation: ExhaustiveValidation,
    audit: StratifiedAudit,
) -> dict[str, object]:
    lsb_words = [bitstring(residue, result.k, lsb_first=True) for residue in result.uncovered_residues]
    msb_words = [bitstring(residue, result.k, lsb_first=False) for residue in result.uncovered_residues]
    return {
        "branch": BRANCH_NAME,
        "removed_rule": REMOVED_RULE,
        "paper_rule": PAPER_RULE,
        "predicate": PREDICATE,
        "k": result.k,
        "modulus": result.modulus,
        "branch_residue_count": len(result.branch_residues),
        "lowbit_certified_count": len(result.certified_residues),
        "uncovered_count": len(result.uncovered_residues),
        "certified_fraction": f"{len(result.certified_residues) / len(result.branch_residues):.12f}",
        "uncovered_fraction": f"{len(result.uncovered_residues) / len(result.branch_residues):.12f}",
        "uncovered_sha256": residue_digest(result.uncovered_residues),
        "certified_sha256": residue_digest(result.certified_residues),
        "lsb_first_trie_nodes": trie_node_count(lsb_words),
        "msb_first_trie_nodes": trie_node_count(msb_words),
        "validation_limit_exclusive": validation.limit_exclusive,
        "validation_checked_candidates": validation.checked_candidates,
        "false_positives": validation.false_positives,
        "audit_max_power": audit.audit_max_power,
        "audit_residue_strata": audit.residue_strata,
        "audit_residues_per_stratum": audit.residues_per_stratum,
        "audit_lifts_per_residue": audit.lifts_per_residue,
        "audit_certified_residue_samples": audit.certified_residue_samples,
        "audit_uncovered_residue_samples": audit.uncovered_residue_samples,
        "audit_sampled_numbers": audit.sampled_numbers,
        "max_lift_seen": audit.max_lift_seen,
        "affine_failures": audit.affine_failures,
        "audit_certified_false_positives": audit.certified_false_positives,
        "audit_uncovered_sample_descents": audit.uncovered_sample_descents,
        "min_contraction_slack": audit.min_contraction_slack,
        "min_descent_slack": audit.min_descent_slack,
    }


def residue_rows(residues: Sequence[int], k: int) -> list[dict[str, object]]:
    return [
        {
            "residue": residue,
            "residue_binary_msb_first": bitstring(residue, k, lsb_first=False),
            "residue_binary_lsb_first": bitstring(residue, k, lsb_first=True),
            "residue_mod_8": residue % 8,
        }
        for residue in residues
    ]


def validation_rows(validation: ExhaustiveValidation) -> list[dict[str, object]]:
    return [
        {
            "validation_limit_exclusive": validation.limit_exclusive,
            "validation_checked_candidates": validation.checked_candidates,
            "false_positives": validation.false_positives,
        }
    ]


def audit_rows(audit: StratifiedAudit) -> list[dict[str, object]]:
    return [
        {
            "audit_max_power": audit.audit_max_power,
            "residue_strata": audit.residue_strata,
            "residues_per_stratum": audit.residues_per_stratum,
            "lifts_per_residue": audit.lifts_per_residue,
            "certified_residue_samples": audit.certified_residue_samples,
            "uncovered_residue_samples": audit.uncovered_residue_samples,
            "sampled_numbers": audit.sampled_numbers,
            "max_lift_seen": audit.max_lift_seen,
            "affine_failures": audit.affine_failures,
            "certified_false_positives": audit.certified_false_positives,
            "uncovered_sample_descents": audit.uncovered_sample_descents,
            "min_contraction_slack": audit.min_contraction_slack,
            "min_descent_slack": audit.min_descent_slack,
        }
    ]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        raise ValueError("cannot write empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(
    result: RecheckResult,
    validation: ExhaustiveValidation,
    audit: StratifiedAudit,
    row: dict[str, object],
    path: Path,
) -> None:
    lines = [
        "# M22-C1 independent S2-k16 rechecker",
        "",
        "This artifact recomputes the S2 low-bit complement from first principles in",
        "`scripts/m22_c1_rechecker.py`. The central logic does not import earlier M21/M22",
        "scripts; earlier artifacts are useful only as external comparison material.",
        "",
        "| Field | Value |",
        "| --- | ---: |",
    ]
    for key in [
        "k",
        "modulus",
        "branch_residue_count",
        "lowbit_certified_count",
        "uncovered_count",
        "certified_fraction",
        "uncovered_fraction",
        "lsb_first_trie_nodes",
        "msb_first_trie_nodes",
    ]:
        lines.append(f"| `{key}` | `{row[key]}` |")

    lines.extend(
        [
            "",
            f"- Uncovered SHA-256: `{row['uncovered_sha256']}`",
            f"- Certified SHA-256: `{row['certified_sha256']}`",
            f"- Exhaustive validation: `1 <= n < {validation.limit_exclusive}`, "
            f"`checked_candidates = {validation.checked_candidates}`, "
            f"`false_positives = {validation.false_positives}`.",
            f"- Stratified audit: `sampled_numbers = {audit.sampled_numbers}`, "
            f"`affine_failures = {audit.affine_failures}`, "
            f"`max_lift_seen = {audit.max_lift_seen}`.",
            "",
            "Interpretation:",
            "",
            "- The rechecker verifies the finite S2-k16 data slice; it is not a proof of Collatz.",
            "- Certified residues are discharged by the low-bit descent condition "
            "`T^k(r + a 2^k) = T^k(r) + 3^f a`, with `3^f < 2^k` and descent at `r`.",
            "- Uncovered residues are the remaining S2 branch residues to keep for any guarded rewriting experiment.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_reports(
    result: RecheckResult,
    validation: ExhaustiveValidation,
    audit: StratifiedAudit,
    *,
    out_dir: Path,
    prefix: str,
) -> dict[str, Path]:
    row = summary_row(result, validation, audit)
    paths = {
        "summary_csv": out_dir / f"{prefix}.csv",
        "markdown": out_dir / f"{prefix}.md",
        "uncovered_csv": out_dir / f"{prefix}.uncovered_residues.csv",
        "certified_csv": out_dir / f"{prefix}.certified_residues.csv",
        "audit_csv": out_dir / f"{prefix}.audit.csv",
        "validation_csv": out_dir / f"{prefix}.validation.csv",
    }
    write_csv([row], paths["summary_csv"])
    write_csv(residue_rows(result.uncovered_residues, result.k), paths["uncovered_csv"])
    write_csv(residue_rows(result.certified_residues, result.k), paths["certified_csv"])
    write_csv(audit_rows(audit), paths["audit_csv"])
    write_csv(validation_rows(validation), paths["validation_csv"])
    write_markdown(result, validation, audit, row, paths["markdown"])
    return paths


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Independent M22-C1 rechecker for S2-k16.")
    parser.add_argument("--k", type=int, default=16)
    parser.add_argument("--validation-power", type=int, default=20)
    parser.add_argument("--audit-max-power", type=int, default=24)
    parser.add_argument("--audit-residue-strata", type=int, default=32)
    parser.add_argument("--audit-residues-per-stratum", type=int, default=3)
    parser.add_argument("--audit-lifts-per-residue", type=int, default=3)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m22_c1_rechecker")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.validation_power < 1:
        raise ValueError("--validation-power must be positive")
    result = recheck_s2(args.k)
    validation = validate_exhaustive(result, limit_exclusive=1 << args.validation_power)
    audit = audit_stratified(
        result,
        audit_max_power=args.audit_max_power,
        residue_strata=args.audit_residue_strata,
        residues_per_stratum=args.audit_residues_per_stratum,
        lifts_per_residue=args.audit_lifts_per_residue,
    )
    paths = write_reports(result, validation, audit, out_dir=args.out_dir, prefix=args.prefix)
    row = summary_row(result, validation, audit)

    for name, path in paths.items():
        print(f"{name}={path}")
    for key in [
        "branch_residue_count",
        "lowbit_certified_count",
        "uncovered_count",
        "uncovered_sha256",
        "certified_sha256",
        "false_positives",
        "affine_failures",
        "audit_sampled_numbers",
        "max_lift_seen",
    ]:
        print(f"{key}={row[key]}")

    ok = (
        validation.false_positives == 0
        and audit.affine_failures == 0
        and audit.certified_false_positives == 0
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
