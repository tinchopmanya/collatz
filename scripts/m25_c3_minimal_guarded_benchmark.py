from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from m24_microguard_design import (
    DEFAULT_CERTIFIED_CSV,
    DEFAULT_SELECTOR,
    DEFAULT_UNCOVERED_CSV,
    EXPECTED_K,
    Check,
    MicroGuardArtifact,
    bits_lsb,
    bits_msb,
    build_from_files as build_m24_microguard,
    parse_selector,
    read_residue_csv,
    selector_residues,
)
from m24_srs_semantic_audit import audit_dynamic_rules, audit_local_s2_files


FORMAT_VERSION = "m25.c3-minimal-guarded-benchmark.v1"
DEFAULT_PREFIX = "m25_c3_minimal_guarded_benchmark"
DEFAULT_CHALLENGE_DIR = Path("reports/m19_rewriting_challenges")
DEFAULT_CANDIDATE_CSV = Path("reports/m22_residual_stats_candidate_subfamilies.csv")
DEFAULT_OUT_DIR = Path("reports")
GUARDED_ASCII_RULE = "bad -> d"
GUARDED_PAPER_RULE = "tf* -> *"
GUARDED_BRANCH_CONDITION = "n mod 8 = 5"
C3_BUILD_STATUS = "blocked"
C3_BLOCKED_REASON = "guarded_srs_semantics_missing"
INSERTION_POINT_STATUS = "conceptual_anchor_only_not_materialized"
CLAIM_SCOPE = "finite_implication_and_insertion_metadata_only"


@dataclass(frozen=True)
class InsertionSite:
    base_srs: str
    comparison_s2_srs: str
    anchor_rule_ascii: str
    anchor_rule_paper: str
    branch_condition: str
    insertion_point_status: str
    conceptual_guard: str
    conceptual_location: str
    blocked_reason: str


@dataclass(frozen=True)
class C3BenchmarkMetadata:
    name: str
    format_version: str
    c3_build_status: str
    c3_blocked_reason: str
    claim_scope: str
    emits_srs: bool
    prover_calls: str
    selector: str
    selector_bits: int
    selector_residue: int
    selector_modulus: int
    k: int
    modulus: int
    accepted_residues: tuple[int, ...]
    accepted_count: int
    u16_selector_slice_count: int
    certified_overlap_count: int
    outside_u16_count: int
    outside_dynamic_branch_count: int
    accepted_sha256: str
    frozen_uncovered_sha256: str
    certified_sha256: str
    dynamic_rule_ascii: str
    dynamic_rule_paper: str
    dynamic_branch_condition: str
    insertion_site: InsertionSite


def _check(name: str, ok: bool, detail: str, residues: Sequence[int] = ()) -> Check:
    return Check(name=name, ok=ok, detail=detail, residues=tuple(residues))


def dynamic_bad_rule_check() -> tuple[dict[str, object], list[Check]]:
    dynamic_rows = audit_dynamic_rules()
    matches = [row for row in dynamic_rows if row.ascii_rule == GUARDED_ASCII_RULE]
    checks: list[Check] = [
        _check(
            "dynamic_bad_rule_unique",
            len(matches) == 1,
            f"matches={len(matches)}",
        )
    ]
    if len(matches) != 1:
        return {}, checks

    row = matches[0]
    checks.extend(
        [
            _check(
                "dynamic_bad_rule_paper_lhs",
                row.paper_lhs == "tf*" and row.paper_rhs == "*",
                row.paper_rule,
            ),
            _check(
                "dynamic_bad_rule_ascii",
                row.ascii_rule == GUARDED_ASCII_RULE,
                row.ascii_rule,
            ),
            _check(
                "dynamic_bad_rule_residue_class",
                row.residue_modulus == 8 and row.residue == 5,
                f"n = {row.residue_modulus}*x + {row.residue}",
            ),
        ]
    )
    return {
        "paper_rule": row.paper_rule,
        "ascii_rule": row.ascii_rule,
        "residue_modulus": row.residue_modulus,
        "residue": row.residue,
        "s_case": row.s_case,
    }, checks


def local_srs_anchor_checks(root: Path) -> tuple[dict[str, object], list[Check]]:
    audit = audit_local_s2_files(root)
    checks = [
        _check(
            "s_full_contains_bad_rule",
            GUARDED_ASCII_RULE in audit["dynamic_rules_present"],
            f"dynamic_rules_present={audit['dynamic_rules_present']}",
        ),
        _check(
            "s2_removes_only_bad_rule",
            audit["s2_removes_only_bad"] is True,
            f"s2_removed_rules={audit['s2_removed_rules']}",
        ),
        _check(
            "s2_does_not_contain_bad_rule",
            audit["s2_contains_bad"] is False,
            f"s2_contains_bad={audit['s2_contains_bad']}",
        ),
    ]
    return audit, checks


def insertion_site(selector: str) -> InsertionSite:
    return InsertionSite(
        base_srs=str(DEFAULT_CHALLENGE_DIR / "m19_collatz_S_full.srs"),
        comparison_s2_srs=str(DEFAULT_CHALLENGE_DIR / "m19_collatz_S2_without_tf_end_to_end.srs"),
        anchor_rule_ascii=GUARDED_ASCII_RULE,
        anchor_rule_paper=GUARDED_PAPER_RULE,
        branch_condition=GUARDED_BRANCH_CONDITION,
        insertion_point_status=INSERTION_POINT_STATUS,
        conceptual_guard=selector,
        conceptual_location=(
            "Attach the guard to the dynamic contraction anchor `bad -> d` after the "
            "mixed-alphabet S word has exposed lhs `bad` and before that lhs is "
            "contracted to `d`; no guarded rewrite rule is emitted here."
        ),
        blocked_reason=(
            "A semantically honest SRS still needs a local definition for residue-state "
            "threading through auxiliary rules, bit orientation, and context handling."
        ),
    )


def validate_c3_metadata(
    *,
    microguard: MicroGuardArtifact,
    m24_checks: Sequence[Check],
    uncovered_residues: Sequence[int],
    certified_residues: Sequence[int],
    root: Path,
) -> tuple[C3BenchmarkMetadata, list[Check]]:
    selector_bits, selector_residue = parse_selector(microguard.selector)
    selector_modulus = 1 << selector_bits
    guard_residues = selector_residues(
        k=microguard.k,
        selector_bits=selector_bits,
        selector_residue=selector_residue,
    )
    uncovered_set = set(uncovered_residues)
    certified_set = set(certified_residues)
    u16_selector_slice = tuple(
        residue
        for residue in uncovered_residues
        if residue % selector_modulus == selector_residue
    )
    outside_u16 = tuple(residue for residue in guard_residues if residue not in uncovered_set)
    certified_overlap = tuple(residue for residue in guard_residues if residue in certified_set)
    outside_dynamic_branch = tuple(residue for residue in guard_residues if residue % 8 != 5)

    dynamic_info, dynamic_checks = dynamic_bad_rule_check()
    _srs_info, srs_checks = local_srs_anchor_checks(root)
    checks: list[Check] = []
    checks.extend(
        _check(
            f"m24_{check.name}",
            check.ok,
            check.detail,
            check.residues,
        )
        for check in m24_checks
    )
    checks.extend(dynamic_checks)
    checks.extend(srs_checks)
    checks.extend(
        [
            _check(
                "selector_matches_m24_microguard",
                microguard.selector == DEFAULT_SELECTOR,
                microguard.selector,
            ),
            _check(
                "microguard_exact_u16_selector_slice",
                microguard.accepted_residues == guard_residues
                and guard_residues == u16_selector_slice
                and microguard.frozen_selector_count == len(u16_selector_slice),
                (
                    f"guard_count={len(guard_residues)}, "
                    f"u16_selector_slice_count={len(u16_selector_slice)}"
                ),
                tuple(sorted(set(guard_residues).symmetric_difference(u16_selector_slice))),
            ),
            _check(
                "microguard_subset_u16",
                not outside_u16,
                f"outside_u16_count={len(outside_u16)}",
                outside_u16,
            ),
            _check(
                "microguard_no_certified_overlap",
                microguard.certified_overlap_count == 0 and not certified_overlap,
                f"certified_overlap_count={len(certified_overlap)}",
                certified_overlap,
            ),
            _check(
                "microguard_implies_bad_dynamic_branch",
                not outside_dynamic_branch,
                f"outside_dynamic_branch_count={len(outside_dynamic_branch)}",
                outside_dynamic_branch,
            ),
            _check(
                "c3_build_is_blocked",
                C3_BUILD_STATUS == "blocked",
                C3_BUILD_STATUS,
            ),
            _check(
                "no_srs_emitted",
                True,
                "metadata only; no .srs/.tpdb/.aprove.srs output",
            ),
        ]
    )

    metadata = C3BenchmarkMetadata(
        name="M25-C3-minimal-guarded-benchmark-rmod2p13-eq-8189",
        format_version=FORMAT_VERSION,
        c3_build_status=C3_BUILD_STATUS,
        c3_blocked_reason=C3_BLOCKED_REASON,
        claim_scope=CLAIM_SCOPE,
        emits_srs=False,
        prover_calls="none",
        selector=microguard.selector,
        selector_bits=selector_bits,
        selector_residue=selector_residue,
        selector_modulus=selector_modulus,
        k=microguard.k,
        modulus=microguard.modulus,
        accepted_residues=guard_residues,
        accepted_count=len(guard_residues),
        u16_selector_slice_count=len(u16_selector_slice),
        certified_overlap_count=len(certified_overlap),
        outside_u16_count=len(outside_u16),
        outside_dynamic_branch_count=len(outside_dynamic_branch),
        accepted_sha256=microguard.accepted_sha256,
        frozen_uncovered_sha256=microguard.frozen_uncovered_sha256,
        certified_sha256=microguard.certified_sha256,
        dynamic_rule_ascii=str(dynamic_info.get("ascii_rule", GUARDED_ASCII_RULE)),
        dynamic_rule_paper=str(dynamic_info.get("paper_rule", GUARDED_PAPER_RULE)),
        dynamic_branch_condition=GUARDED_BRANCH_CONDITION,
        insertion_site=insertion_site(microguard.selector),
    )
    return metadata, checks


def build_from_files(
    *,
    root: Path = Path.cwd(),
    candidate_csv: Path = DEFAULT_CANDIDATE_CSV,
    uncovered_csv: Path = DEFAULT_UNCOVERED_CSV,
    certified_csv: Path = DEFAULT_CERTIFIED_CSV,
    selector: str = DEFAULT_SELECTOR,
    k: int = EXPECTED_K,
) -> tuple[C3BenchmarkMetadata, list[Check]]:
    microguard, m24_checks = build_m24_microguard(
        candidate_csv=candidate_csv,
        uncovered_csv=uncovered_csv,
        certified_csv=certified_csv,
        selector=selector,
        k=k,
    )
    uncovered_residues = read_residue_csv(uncovered_csv)
    certified_residues = read_residue_csv(certified_csv)
    return validate_c3_metadata(
        microguard=microguard,
        m24_checks=m24_checks,
        uncovered_residues=uncovered_residues,
        certified_residues=certified_residues,
        root=root,
    )


def failure_rows(checks: Sequence[Check]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for check in checks:
        if check.ok:
            continue
        rows.append(
            {
                "check": check.name,
                "ok": check.ok,
                "detail": check.detail,
                "residues": " ".join(str(residue) for residue in check.residues),
            }
        )
    return rows


def summary_row(metadata: C3BenchmarkMetadata, checks: Sequence[Check]) -> dict[str, object]:
    return {
        "name": metadata.name,
        "format_version": metadata.format_version,
        "c3_build_status": metadata.c3_build_status,
        "c3_blocked_reason": metadata.c3_blocked_reason,
        "implication_checks_passed": all(check.ok for check in checks),
        "claim_scope": metadata.claim_scope,
        "emits_srs": metadata.emits_srs,
        "prover_calls": metadata.prover_calls,
        "selector": metadata.selector,
        "selector_bits": metadata.selector_bits,
        "selector_residue": metadata.selector_residue,
        "selector_modulus": metadata.selector_modulus,
        "k": metadata.k,
        "modulus": metadata.modulus,
        "accepted_count": metadata.accepted_count,
        "u16_selector_slice_count": metadata.u16_selector_slice_count,
        "certified_overlap_count": metadata.certified_overlap_count,
        "outside_u16_count": metadata.outside_u16_count,
        "outside_dynamic_branch_count": metadata.outside_dynamic_branch_count,
        "accepted_sha256": metadata.accepted_sha256,
        "frozen_uncovered_sha256": metadata.frozen_uncovered_sha256,
        "certified_sha256_checked_not_embedded": metadata.certified_sha256,
        "dynamic_rule_ascii": metadata.dynamic_rule_ascii,
        "dynamic_rule_paper": metadata.dynamic_rule_paper,
        "dynamic_branch_condition": metadata.dynamic_branch_condition,
        "insertion_anchor_rule": metadata.insertion_site.anchor_rule_ascii,
        "insertion_point_status": metadata.insertion_site.insertion_point_status,
    }


def write_csv(rows: Sequence[dict[str, object]], path: Path, fieldnames: Sequence[str] | None = None) -> None:
    if not rows and fieldnames is None:
        raise ValueError("fieldnames are required when writing an empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    headers = list(fieldnames or rows[0].keys())
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=headers, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def metadata_text(metadata: C3BenchmarkMetadata) -> str:
    lines = [
        f"# {FORMAT_VERSION}",
        f"name: {metadata.name}",
        f"claim_scope: {metadata.claim_scope}",
        f"c3_build_status: {metadata.c3_build_status}",
        f"c3_blocked_reason: {metadata.c3_blocked_reason}",
        f"emits_srs: {str(metadata.emits_srs).lower()}",
        f"prover_calls: {metadata.prover_calls}",
        "termination_claim: none",
        "collatz_claim: none",
        "",
        "[microguard]",
        f"universe: r modulo 2^{metadata.k}",
        f"selector: {metadata.selector}",
        f"selector_bits: {metadata.selector_bits}",
        f"selector_modulus: {metadata.selector_modulus}",
        f"selector_residue: {metadata.selector_residue}",
        f"accepted_count: {metadata.accepted_count}",
        f"exact_subset_statement: G_8189 = U_16 intersection {{r | {metadata.selector}}}",
        f"u16_selector_slice_count: {metadata.u16_selector_slice_count}",
        f"certified_overlap_count: {metadata.certified_overlap_count}",
        f"outside_u16_count: {metadata.outside_u16_count}",
        "",
        "[dynamic_branch]",
        f"ascii_rule: {metadata.dynamic_rule_ascii}",
        f"paper_rule: {metadata.dynamic_rule_paper}",
        f"branch_condition: {metadata.dynamic_branch_condition}",
        f"guard_implies_branch: outside_dynamic_branch_count={metadata.outside_dynamic_branch_count}",
        "",
        "[guard_insertion_site]",
        f"base_srs: {metadata.insertion_site.base_srs}",
        f"comparison_s2_srs: {metadata.insertion_site.comparison_s2_srs}",
        f"anchor_rule_ascii: {metadata.insertion_site.anchor_rule_ascii}",
        f"anchor_rule_paper: {metadata.insertion_site.anchor_rule_paper}",
        f"branch_condition: {metadata.insertion_site.branch_condition}",
        f"insertion_point_status: {metadata.insertion_site.insertion_point_status}",
        f"conceptual_guard: {metadata.insertion_site.conceptual_guard}",
        f"conceptual_location: {metadata.insertion_site.conceptual_location}",
        f"blocked_reason: {metadata.insertion_site.blocked_reason}",
        "",
        "[accepted_residues]",
    ]
    for residue in metadata.accepted_residues:
        lines.append(f"{residue} msb={bits_msb(residue, metadata.k)} lsb={bits_lsb(residue, metadata.k)}")
    lines.extend(
        [
            "",
            "[hashes]",
            f"accepted_residues_sha256: {metadata.accepted_sha256}",
            f"frozen_uncovered_sha256: {metadata.frozen_uncovered_sha256}",
            f"certified_set_sha256_checked_not_embedded: {metadata.certified_sha256}",
            "",
            "[non_claims]",
            "does_not_emit_srs: true",
            "does_not_emit_tpdb: true",
            "does_not_call_matchbox: true",
            "does_not_call_aprove: true",
            "does_not_claim_termination: true",
            "does_not_claim_collatz: true",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(
    metadata: C3BenchmarkMetadata,
    checks: Sequence[Check],
    *,
    out_dir: Path,
    prefix: str = DEFAULT_PREFIX,
) -> dict[str, Path]:
    metadata_path = out_dir / f"{prefix}.metadata.txt"
    summary_path = out_dir / f"{prefix}_summary.csv"
    violations_path = out_dir / f"{prefix}_violations.csv"
    out_dir.mkdir(parents=True, exist_ok=True)
    with metadata_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(metadata_text(metadata))
    write_csv([summary_row(metadata, checks)], summary_path)
    write_csv(
        failure_rows(checks),
        violations_path,
        fieldnames=["check", "ok", "detail", "residues"],
    )
    return {"metadata": metadata_path, "summary": summary_path, "violations": violations_path}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Build the M25 C3 minimal guarded benchmark metadata/checker. "
            "This intentionally emits no SRS and calls no termination prover."
        )
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--candidate-csv", type=Path, default=DEFAULT_CANDIDATE_CSV)
    parser.add_argument("--uncovered-csv", type=Path, default=DEFAULT_UNCOVERED_CSV)
    parser.add_argument("--certified-csv", type=Path, default=DEFAULT_CERTIFIED_CSV)
    parser.add_argument("--selector", default=DEFAULT_SELECTOR)
    parser.add_argument("--k", type=int, default=EXPECTED_K)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    metadata, checks = build_from_files(
        root=args.root,
        candidate_csv=args.candidate_csv,
        uncovered_csv=args.uncovered_csv,
        certified_csv=args.certified_csv,
        selector=args.selector,
        k=args.k,
    )
    paths = write_outputs(metadata, checks, out_dir=args.out_dir, prefix=args.prefix)
    passed = all(check.ok for check in checks)
    print(f"m25_c3_minimal_guarded_benchmark={'PASS' if passed else 'FAIL'}")
    print(f"c3_build_status={metadata.c3_build_status}")
    print(f"c3_blocked_reason={metadata.c3_blocked_reason}")
    print(f"metadata={paths['metadata']}")
    print(f"summary={paths['summary']}")
    print(f"violations={paths['violations']}")
    print(f"accepted_count={metadata.accepted_count}")
    print(f"certified_overlap_count={metadata.certified_overlap_count}")
    print(f"dynamic_rule={metadata.dynamic_rule_ascii}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
