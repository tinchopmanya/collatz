from __future__ import annotations

import argparse
import csv
import hashlib
import re
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence


EXPECTED_K = 16
EXPECTED_UNCOVERED_SHA256 = "bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210"
EXPECTED_CERTIFIED_SHA256 = "0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa"
DEFAULT_SELECTOR = "r mod 2^13 = 8189"
DEFAULT_CANDIDATES_CSV = Path("reports/m22_residual_stats_candidate_subfamilies.csv")
DEFAULT_UNCOVERED_CSV = Path("reports/m22_s2_k16_uncovered_residues.csv")
DEFAULT_CERTIFIED_CSV = Path("reports/m22_c1_rechecker.certified_residues.csv")
DEFAULT_PREFIX = "m24_microguard_8189"
GUARD_FORMAT_VERSION = "m24.microguard.v1"
CLAIM_SCOPE = "finite_residue_implication_only"
SRS_EQUIVALENCE_STATUS = "blocked_by_M24-SRS-SemanticAudit"
BLOCKED_BY = "M24-SRS-SemanticAudit"
SELECTOR_RE = re.compile(r"^r\s+mod\s+2\^(?P<bits>\d+)\s*=\s*(?P<residue>\d+)$")


@dataclass(frozen=True)
class Candidate:
    rank: int
    family_type: str
    selector: str
    selector_bits: int
    selector_residue: int
    residue_count: int
    selector_s2_branch_capacity: int
    selector_exact_for_u16: bool
    non_residual_s2_overinclude: int
    residues: tuple[int, ...]
    rationale: str


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str
    residues: tuple[int, ...] = ()


@dataclass(frozen=True)
class MicroGuardArtifact:
    name: str
    guard_format_version: str
    k: int
    modulus: int
    selector: str
    selector_bits: int
    selector_modulus: int
    selector_residue: int
    candidate_rank: int
    candidate_family_type: str
    candidate_residue_count: int
    selector_s2_branch_capacity: int
    accepted_count: int
    accepted_residues: tuple[int, ...]
    frozen_selector_count: int
    certified_overlap_count: int
    outside_s2_count: int
    accepted_sha256: str
    frozen_uncovered_sha256: str
    certified_sha256: str
    claim_scope: str
    srs_equivalence_status: str
    blocked_by: str
    contains_certificates: bool


def residue_digest(residues: Sequence[int]) -> str:
    payload = "\n".join(str(residue) for residue in residues) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def bits_msb(value: int, width: int) -> str:
    return format(value, f"0{width}b")


def bits_lsb(value: int, width: int) -> str:
    return bits_msb(value, width)[::-1]


def parse_bool(value: str) -> bool:
    if value == "True":
        return True
    if value == "False":
        return False
    raise ValueError(f"expected True/False boolean field, got {value!r}")


def parse_selector(selector: str) -> tuple[int, int]:
    match = SELECTOR_RE.match(selector.strip())
    if match is None:
        raise ValueError(f"unsupported selector format: {selector!r}")
    bits = int(match.group("bits"))
    residue = int(match.group("residue"))
    if bits < 0:
        raise ValueError("selector bit width must be non-negative")
    if residue < 0 or residue >= (1 << bits):
        raise ValueError(f"selector residue must be in [0, 2^{bits})")
    return bits, residue


def read_residue_csv(path: Path) -> tuple[int, ...]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "residue" not in reader.fieldnames:
            raise ValueError(f"{path} must contain a residue column")
        residues = tuple(int(row["residue"]) for row in reader)
    return residues


def validate_residue_list(
    residues: Sequence[int],
    *,
    k: int,
    name: str,
    require_s2: bool,
) -> list[Check]:
    modulus = 1 << k
    checks: list[Check] = []
    checks.append(
        Check(
            f"{name}_sorted",
            tuple(sorted(residues)) == tuple(residues),
            f"{name} residues are sorted" if tuple(sorted(residues)) == tuple(residues) else f"{name} residues are not sorted",
        )
    )
    duplicate_count = len(residues) - len(set(residues))
    checks.append(
        Check(
            f"{name}_unique",
            duplicate_count == 0,
            f"{name} duplicate_count={duplicate_count}",
        )
    )
    out_of_range = tuple(residue for residue in residues if residue < 0 or residue >= modulus)
    checks.append(
        Check(
            f"{name}_range",
            not out_of_range,
            f"{name} out_of_range_count={len(out_of_range)}",
            out_of_range,
        )
    )
    outside_s2 = tuple(residue for residue in residues if residue % 8 != 5)
    checks.append(
        Check(
            f"{name}_s2_mod8",
            (not require_s2) or not outside_s2,
            f"{name} outside_s2_count={len(outside_s2)}",
            outside_s2,
        )
    )
    return checks


def read_candidate(candidate_csv: Path, selector: str, *, require_rank_one: bool = True) -> Candidate:
    selector_bits, selector_residue = parse_selector(selector)
    with candidate_csv.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    matches = [row for row in rows if row.get("selector") == selector]
    if len(matches) != 1:
        raise ValueError(f"expected exactly one candidate for {selector!r}, got {len(matches)}")
    row = matches[0]
    rank = int(row["rank"])
    if require_rank_one and rank != 1:
        best = rows[0]["selector"] if rows else "<none>"
        raise ValueError(f"{selector!r} is no longer rank 1; current rank={rank}, best={best!r}")
    if int(row["selector_bits"]) != selector_bits:
        raise ValueError("candidate selector_bits does not match selector syntax")

    residues = tuple(int(token) for token in row["residues"].split())
    return Candidate(
        rank=rank,
        family_type=row["family_type"],
        selector=row["selector"],
        selector_bits=selector_bits,
        selector_residue=selector_residue,
        residue_count=int(row["residue_count"]),
        selector_s2_branch_capacity=int(row["selector_s2_branch_capacity"]),
        selector_exact_for_u16=parse_bool(row["selector_exact_for_u16"]),
        non_residual_s2_overinclude=int(row["non_residual_s2_overinclude"]),
        residues=residues,
        rationale=row["rationale"],
    )


def selector_residues(*, k: int, selector_bits: int, selector_residue: int) -> tuple[int, ...]:
    if selector_bits > k:
        raise ValueError("selector_bits cannot exceed k")
    selector_modulus = 1 << selector_bits
    return tuple(
        residue
        for residue in range(1 << k)
        if residue % selector_modulus == selector_residue
    )


def validate_microguard(
    *,
    candidate: Candidate,
    uncovered_residues: Sequence[int],
    certified_residues: Sequence[int],
    k: int = EXPECTED_K,
    expected_uncovered_sha256: str | None = EXPECTED_UNCOVERED_SHA256,
    expected_certified_sha256: str | None = EXPECTED_CERTIFIED_SHA256,
) -> tuple[MicroGuardArtifact, list[Check]]:
    modulus = 1 << k
    selector_modulus = 1 << candidate.selector_bits
    guard_residues = selector_residues(
        k=k,
        selector_bits=candidate.selector_bits,
        selector_residue=candidate.selector_residue,
    )
    uncovered_set = set(uncovered_residues)
    certified_set = set(certified_residues)
    frozen_selector = tuple(
        residue
        for residue in uncovered_residues
        if residue % selector_modulus == candidate.selector_residue
    )
    certified_overlap = tuple(residue for residue in guard_residues if residue in certified_set)
    outside_s2 = tuple(residue for residue in guard_residues if residue % 8 != 5)
    not_in_frozen = tuple(residue for residue in guard_residues if residue not in uncovered_set)

    uncovered_sha = residue_digest(tuple(uncovered_residues))
    certified_sha = residue_digest(tuple(certified_residues))
    accepted_sha = residue_digest(guard_residues)
    checks: list[Check] = []
    checks.extend(
        validate_residue_list(uncovered_residues, k=k, name="frozen_uncovered", require_s2=True)
    )
    checks.extend(validate_residue_list(certified_residues, k=k, name="certified", require_s2=True))
    checks.extend(validate_residue_list(candidate.residues, k=k, name="candidate", require_s2=True))
    checks.append(
        Check(
            "expected_uncovered_sha256",
            expected_uncovered_sha256 is None or uncovered_sha == expected_uncovered_sha256,
            f"uncovered_sha256={uncovered_sha}",
        )
    )
    checks.append(
        Check(
            "expected_certified_sha256",
            expected_certified_sha256 is None or certified_sha == expected_certified_sha256,
            f"certified_sha256={certified_sha}",
        )
    )
    checks.append(
        Check(
            "candidate_declares_exact",
            candidate.selector_exact_for_u16 and candidate.non_residual_s2_overinclude == 0,
            (
                "selector_exact_for_u16=True and non_residual_s2_overinclude=0"
                if candidate.selector_exact_for_u16 and candidate.non_residual_s2_overinclude == 0
                else (
                    f"selector_exact_for_u16={candidate.selector_exact_for_u16}, "
                    f"non_residual_s2_overinclude={candidate.non_residual_s2_overinclude}"
                )
            ),
        )
    )
    checks.append(
        Check(
            "candidate_count_matches_row",
            len(candidate.residues) == candidate.residue_count,
            f"listed={len(candidate.residues)}, row={candidate.residue_count}",
        )
    )
    checks.append(
        Check(
            "candidate_residues_equal_guard",
            tuple(candidate.residues) == guard_residues,
            f"candidate_count={len(candidate.residues)}, guard_count={len(guard_residues)}",
            tuple(sorted(set(candidate.residues).symmetric_difference(guard_residues))),
        )
    )
    checks.append(
        Check(
            "guard_count_matches_capacity",
            len(guard_residues) == candidate.selector_s2_branch_capacity,
            f"guard_count={len(guard_residues)}, capacity={candidate.selector_s2_branch_capacity}",
        )
    )
    checks.append(
        Check(
            "guard_subset_frozen_complement",
            not not_in_frozen,
            f"not_in_frozen_count={len(not_in_frozen)}",
            not_in_frozen,
        )
    )
    checks.append(
        Check(
            "guard_equals_frozen_selector_intersection",
            guard_residues == frozen_selector,
            f"guard_count={len(guard_residues)}, frozen_selector_count={len(frozen_selector)}",
            tuple(sorted(set(guard_residues).symmetric_difference(frozen_selector))),
        )
    )
    checks.append(
        Check(
            "no_certified_residues",
            not certified_overlap,
            f"certified_overlap_count={len(certified_overlap)}",
            certified_overlap,
        )
    )
    checks.append(
        Check(
            "guard_implies_s2_mod8",
            not outside_s2,
            f"outside_s2_count={len(outside_s2)}",
            outside_s2,
        )
    )
    checks.append(
        Check(
            "no_srs_equivalence_claim",
            SRS_EQUIVALENCE_STATUS == "blocked_by_M24-SRS-SemanticAudit",
            SRS_EQUIVALENCE_STATUS,
        )
    )

    artifact = MicroGuardArtifact(
        name="M24-S2-k16-rmod2p13-eq-8189",
        guard_format_version=GUARD_FORMAT_VERSION,
        k=k,
        modulus=modulus,
        selector=candidate.selector,
        selector_bits=candidate.selector_bits,
        selector_modulus=selector_modulus,
        selector_residue=candidate.selector_residue,
        candidate_rank=candidate.rank,
        candidate_family_type=candidate.family_type,
        candidate_residue_count=candidate.residue_count,
        selector_s2_branch_capacity=candidate.selector_s2_branch_capacity,
        accepted_count=len(guard_residues),
        accepted_residues=guard_residues,
        frozen_selector_count=len(frozen_selector),
        certified_overlap_count=len(certified_overlap),
        outside_s2_count=len(outside_s2),
        accepted_sha256=accepted_sha,
        frozen_uncovered_sha256=uncovered_sha,
        certified_sha256=certified_sha,
        claim_scope=CLAIM_SCOPE,
        srs_equivalence_status=SRS_EQUIVALENCE_STATUS,
        blocked_by=BLOCKED_BY,
        contains_certificates=False,
    )
    return artifact, checks


def failure_rows(checks: Sequence[Check]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for check in checks:
        if check.ok:
            continue
        residue_text = " ".join(str(residue) for residue in check.residues)
        rows.append(
            {
                "check": check.name,
                "ok": check.ok,
                "detail": check.detail,
                "residues": residue_text,
            }
        )
    return rows


def summary_row(artifact: MicroGuardArtifact, checks: Sequence[Check]) -> dict[str, object]:
    return {
        "name": artifact.name,
        "guard_format_version": artifact.guard_format_version,
        "k": artifact.k,
        "modulus": artifact.modulus,
        "selector": artifact.selector,
        "selector_bits": artifact.selector_bits,
        "selector_modulus": artifact.selector_modulus,
        "selector_residue": artifact.selector_residue,
        "candidate_rank": artifact.candidate_rank,
        "candidate_family_type": artifact.candidate_family_type,
        "candidate_residue_count": artifact.candidate_residue_count,
        "selector_s2_branch_capacity": artifact.selector_s2_branch_capacity,
        "accepted_count": artifact.accepted_count,
        "frozen_selector_count": artifact.frozen_selector_count,
        "certified_overlap_count": artifact.certified_overlap_count,
        "outside_s2_count": artifact.outside_s2_count,
        "accepted_sha256": artifact.accepted_sha256,
        "frozen_uncovered_sha256": artifact.frozen_uncovered_sha256,
        "certified_sha256": artifact.certified_sha256,
        "passed": all(check.ok for check in checks),
        "claim_scope": artifact.claim_scope,
        "srs_equivalence_status": artifact.srs_equivalence_status,
        "blocked_by": artifact.blocked_by,
        "contains_certificates": artifact.contains_certificates,
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


def guard_text(artifact: MicroGuardArtifact) -> str:
    lines = [
        f"# {GUARD_FORMAT_VERSION}",
        f"name: {artifact.name}",
        f"scope: {artifact.claim_scope}",
        f"srs_equivalence_status: {artifact.srs_equivalence_status}",
        f"blocked_by: {artifact.blocked_by}",
        "no_srs_equivalence_claim: true",
        f"contains_certificates: {str(artifact.contains_certificates).lower()}",
        "prover_calls: none",
        "",
        "[universe]",
        f"k: {artifact.k}",
        f"modulus: {artifact.modulus}",
        "branch_tag: S2_without_tf_end_to_end",
        "branch_tag_status: tag_only_not_operational_equivalence",
        "",
        "[guard]",
        f"expression: {artifact.selector}",
        f"selector_bits: {artifact.selector_bits}",
        f"selector_modulus: {artifact.selector_modulus}",
        f"selector_residue: {artifact.selector_residue}",
        "",
        "[checked_implications]",
        f"forall_r_mod_2^{artifact.k}: guard(r) => r in frozen_S2_k16_complement",
        f"forall_r_mod_2^{artifact.k}: guard(r) => r not in lowbit_certified_S2_k16",
        f"forall_r_mod_2^{artifact.k}: guard(r) => r mod 8 = 5",
        "",
        "[accepted_residues]",
    ]
    for residue in artifact.accepted_residues:
        lines.append(
            f"{residue} msb={bits_msb(residue, artifact.k)} lsb={bits_lsb(residue, artifact.k)}"
        )
    lines.extend(
        [
            "",
            "[hashes]",
            f"accepted_residues_sha256: {artifact.accepted_sha256}",
            f"frozen_uncovered_sha256: {artifact.frozen_uncovered_sha256}",
            f"certified_set_sha256_checked_not_embedded: {artifact.certified_sha256}",
            "",
            "[non_claims]",
            "does_not_generate_srs: true",
            "does_not_call_matchbox_or_aprove: true",
            "does_not_claim_termination: true",
            "does_not_claim_collatz: true",
            "must_wait_for: M24-SRS-SemanticAudit",
        ]
    )
    return "\n".join(lines) + "\n"


def write_outputs(
    artifact: MicroGuardArtifact,
    checks: Sequence[Check],
    *,
    out_dir: Path,
    prefix: str = DEFAULT_PREFIX,
) -> dict[str, Path]:
    guard_path = out_dir / f"{prefix}.guard.txt"
    summary_path = out_dir / f"{prefix}_summary.csv"
    violations_path = out_dir / f"{prefix}_violations.csv"
    out_dir.mkdir(parents=True, exist_ok=True)
    with guard_path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(guard_text(artifact))
    write_csv([summary_row(artifact, checks)], summary_path)
    write_csv(
        failure_rows(checks),
        violations_path,
        fieldnames=["check", "ok", "detail", "residues"],
    )
    return {
        "guard": guard_path,
        "summary": summary_path,
        "violations": violations_path,
    }


def build_from_files(
    *,
    candidate_csv: Path = DEFAULT_CANDIDATES_CSV,
    uncovered_csv: Path = DEFAULT_UNCOVERED_CSV,
    certified_csv: Path = DEFAULT_CERTIFIED_CSV,
    selector: str = DEFAULT_SELECTOR,
    k: int = EXPECTED_K,
    require_rank_one: bool = True,
    expected_uncovered_sha256: str | None = EXPECTED_UNCOVERED_SHA256,
    expected_certified_sha256: str | None = EXPECTED_CERTIFIED_SHA256,
) -> tuple[MicroGuardArtifact, list[Check]]:
    candidate = read_candidate(candidate_csv, selector, require_rank_one=require_rank_one)
    uncovered = read_residue_csv(uncovered_csv)
    certified = read_residue_csv(certified_csv)
    return validate_microguard(
        candidate=candidate,
        uncovered_residues=uncovered,
        certified_residues=certified,
        k=k,
        expected_uncovered_sha256=expected_uncovered_sha256,
        expected_certified_sha256=expected_certified_sha256,
    )


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate and check the M24 textual microguard. This is not an SRS generator "
            "and does not call Matchbox, AProVE, or any termination prover."
        )
    )
    parser.add_argument("--candidate-csv", type=Path, default=DEFAULT_CANDIDATES_CSV)
    parser.add_argument("--uncovered-csv", type=Path, default=DEFAULT_UNCOVERED_CSV)
    parser.add_argument("--certified-csv", type=Path, default=DEFAULT_CERTIFIED_CSV)
    parser.add_argument("--selector", default=DEFAULT_SELECTOR)
    parser.add_argument("--k", type=int, default=EXPECTED_K)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default=DEFAULT_PREFIX)
    parser.add_argument(
        "--allow-non-top",
        action="store_true",
        help="Allow the selected candidate even if it is no longer rank 1.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    artifact, checks = build_from_files(
        candidate_csv=args.candidate_csv,
        uncovered_csv=args.uncovered_csv,
        certified_csv=args.certified_csv,
        selector=args.selector,
        k=args.k,
        require_rank_one=not args.allow_non_top,
    )
    paths = write_outputs(artifact, checks, out_dir=args.out_dir, prefix=args.prefix)
    passed = all(check.ok for check in checks)
    print(f"m24_microguard={'PASS' if passed else 'FAIL'}")
    print(f"guard={paths['guard']}")
    print(f"summary={paths['summary']}")
    print(f"violations={paths['violations']}")
    print(f"accepted_count={artifact.accepted_count}")
    print(f"certified_overlap_count={artifact.certified_overlap_count}")
    print(f"srs_equivalence_status={artifact.srs_equivalence_status}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
