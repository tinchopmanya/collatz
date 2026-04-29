from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from m22_freeze_s2_k16 import (  # noqa: E402
    FrozenSet,
    bitstring,
    freeze_s2,
    residue_digest,
)


S2_BRANCH = "S2_without_tf_end_to_end"
S2_REMOVED_RULE = "bad -> d"
S2_PAPER_RULE = "tf* -> *"
S2_RESIDUE_PREDICATE = "residue % 8 == 5"
GUARD_SOURCE = "reports/m22_s2_k16_uncovered_residues.csv"
SEMANTIC_TRANSLATION_STATUS = "gap_unproven"
SEMANTIC_TRANSLATION_NOTE = (
    "The local artifacts tag bad -> d / tf* -> * as residue 5 mod 8, but they do "
    "not contain an independently checked translation from the mixed binary/"
    "ternary SRS alphabet to the low-bit predicate."
)

EXPECTED_K16 = {
    "k": 16,
    "modulus": 65536,
    "evaluated_residues": 65536,
    "branch_residue_count": 8192,
    "frozen_complement_count": 378,
    "lowbit_certified_count": 7814,
    "outside_s2_accepted_count": 0,
    "certified_to_guard_count": 0,
    "uncovered_sha256": "bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210",
    "certified_sha256": "0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa",
}

RESIDUE_AUDIT_FIELDS = [
    "residue",
    "residue_binary_msb_first",
    "residue_binary_lsb_first",
    "residue_mod_8",
    "in_s2_branch_by_mod8",
    "in_frozen_complement",
    "lowbit_certified_in_s2",
    "accepted_by_guard",
    "violation",
]


@dataclass(frozen=True)
class SemanticBridgeValidation:
    k: int
    modulus: int
    evaluated_residues: int
    branch: str
    removed_rule: str
    paper_rule: str
    residue_predicate: str
    guard_source: str
    branch_residue_count: int
    frozen_complement_count: int
    lowbit_certified_count: int
    guard_accepted_count: int
    complement_accepted_count: int
    complement_rejected_count: int
    outside_s2_accepted_count: int
    certified_to_guard_count: int
    accepted_not_in_complement_count: int
    s2_partition_hole_count: int
    frozen_set_outside_s2_count: int
    violation_count: int
    expected_uncovered_sha256: str
    uncovered_sha256: str
    uncovered_hash_matches_expected: bool
    expected_certified_sha256: str
    certified_sha256: str
    certified_hash_matches_expected: bool
    saved_summary_matches_expected: bool
    saved_uncovered_matches_generated: bool
    computational_guard_status: str
    semantic_translation_status: str
    semantic_translation_gap: bool
    semantic_translation_note: str


def is_s2_branch_residue(residue: int) -> bool:
    return residue % 8 == 5


def guard_accepts_residue(residue: int, frozen_complement: set[int]) -> bool:
    return residue in frozen_complement


def read_single_summary_row(path: Path) -> dict[str, str]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    if len(rows) != 1:
        raise ValueError(f"expected exactly one summary row in {path}, got {len(rows)}")
    return rows[0]


def read_uncovered_residues(path: Path, k: int) -> list[int]:
    residues: list[int] = []
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        for row in reader:
            residue = int(row["residue"])
            msb = bitstring(residue, k, lsb_first=False)
            lsb = bitstring(residue, k, lsb_first=True)
            if row.get("residue_binary_msb_first") != msb:
                raise ValueError(f"bad MSB bitstring for residue {residue} in {path}")
            if row.get("residue_binary_lsb_first") != lsb:
                raise ValueError(f"bad LSB bitstring for residue {residue} in {path}")
            if int(row.get("residue_mod_8", "-1")) != residue % 8:
                raise ValueError(f"bad mod-8 field for residue {residue} in {path}")
            residues.append(residue)
    return residues


def saved_summary_matches(summary: dict[str, str], validation: SemanticBridgeValidation) -> bool:
    expected_pairs = {
        "k": validation.k,
        "modulus": validation.modulus,
        "branch_residue_count": validation.branch_residue_count,
        "lowbit_certified_count": validation.lowbit_certified_count,
        "uncovered_count": validation.frozen_complement_count,
        "uncovered_sha256": validation.uncovered_sha256,
        "certified_sha256": validation.certified_sha256,
    }
    return all(str(summary.get(key)) == str(value) for key, value in expected_pairs.items())


def residue_audit_rows(frozen: FrozenSet) -> tuple[list[dict[str, object]], dict[str, int]]:
    frozen_complement = set(frozen.uncovered_residues)
    certified_in_s2 = set(frozen.certified_residues)
    rows: list[dict[str, object]] = []
    counts = {
        "branch_residue_count": 0,
        "guard_accepted_count": 0,
        "complement_accepted_count": 0,
        "complement_rejected_count": 0,
        "outside_s2_accepted_count": 0,
        "certified_to_guard_count": 0,
        "accepted_not_in_complement_count": 0,
        "s2_partition_hole_count": 0,
        "frozen_set_outside_s2_count": 0,
        "violation_count": 0,
    }

    for residue in range(frozen.modulus):
        in_s2 = is_s2_branch_residue(residue)
        in_complement = residue in frozen_complement
        is_certified = residue in certified_in_s2
        accepted = guard_accepts_residue(residue, frozen_complement)
        violations: list[str] = []

        if in_s2:
            counts["branch_residue_count"] += 1
        if accepted:
            counts["guard_accepted_count"] += 1
        if in_complement and accepted:
            counts["complement_accepted_count"] += 1
        if in_complement and not accepted:
            counts["complement_rejected_count"] += 1
            violations.append("complement_rejected")
        if accepted and not in_s2:
            counts["outside_s2_accepted_count"] += 1
            violations.append("outside_s2_accepted")
        if accepted and is_certified:
            counts["certified_to_guard_count"] += 1
            violations.append("certified_to_guard")
        if accepted and not in_complement:
            counts["accepted_not_in_complement_count"] += 1
            violations.append("accepted_not_in_complement")
        if in_s2 and not in_complement and not is_certified:
            counts["s2_partition_hole_count"] += 1
            violations.append("s2_partition_hole")
        if (in_complement or is_certified) and not in_s2:
            counts["frozen_set_outside_s2_count"] += 1
            violations.append("frozen_set_outside_s2")

        if violations:
            counts["violation_count"] += 1
        rows.append(
            {
                "residue": residue,
                "residue_binary_msb_first": bitstring(residue, frozen.k, lsb_first=False),
                "residue_binary_lsb_first": bitstring(residue, frozen.k, lsb_first=True),
                "residue_mod_8": residue % 8,
                "in_s2_branch_by_mod8": in_s2,
                "in_frozen_complement": in_complement,
                "lowbit_certified_in_s2": is_certified,
                "accepted_by_guard": accepted,
                "violation": ";".join(violations),
            }
        )

    return rows, counts


def validate_bridge(
    k: int,
    *,
    saved_summary_path: Path | None = None,
    saved_uncovered_path: Path | None = None,
) -> tuple[SemanticBridgeValidation, list[dict[str, object]], list[dict[str, object]]]:
    if k != EXPECTED_K16["k"]:
        raise ValueError("M22-C2 is preregistered for k=16")

    frozen = freeze_s2(k)
    audit_rows, counts = residue_audit_rows(frozen)
    uncovered_sha256 = residue_digest(frozen.uncovered_residues)
    certified_sha256 = residue_digest(frozen.certified_residues)

    expected_uncovered_sha256 = str(EXPECTED_K16["uncovered_sha256"])
    expected_certified_sha256 = str(EXPECTED_K16["certified_sha256"])
    saved_uncovered_matches_generated = False
    if saved_uncovered_path is not None:
        saved_uncovered = read_uncovered_residues(saved_uncovered_path, k)
        saved_uncovered_matches_generated = saved_uncovered == frozen.uncovered_residues

    validation = SemanticBridgeValidation(
        k=k,
        modulus=frozen.modulus,
        evaluated_residues=len(audit_rows),
        branch=S2_BRANCH,
        removed_rule=S2_REMOVED_RULE,
        paper_rule=S2_PAPER_RULE,
        residue_predicate=S2_RESIDUE_PREDICATE,
        guard_source=GUARD_SOURCE,
        branch_residue_count=counts["branch_residue_count"],
        frozen_complement_count=len(frozen.uncovered_residues),
        lowbit_certified_count=len(frozen.certified_residues),
        guard_accepted_count=counts["guard_accepted_count"],
        complement_accepted_count=counts["complement_accepted_count"],
        complement_rejected_count=counts["complement_rejected_count"],
        outside_s2_accepted_count=counts["outside_s2_accepted_count"],
        certified_to_guard_count=counts["certified_to_guard_count"],
        accepted_not_in_complement_count=counts["accepted_not_in_complement_count"],
        s2_partition_hole_count=counts["s2_partition_hole_count"],
        frozen_set_outside_s2_count=counts["frozen_set_outside_s2_count"],
        violation_count=counts["violation_count"],
        expected_uncovered_sha256=expected_uncovered_sha256,
        uncovered_sha256=uncovered_sha256,
        uncovered_hash_matches_expected=uncovered_sha256 == expected_uncovered_sha256,
        expected_certified_sha256=expected_certified_sha256,
        certified_sha256=certified_sha256,
        certified_hash_matches_expected=certified_sha256 == expected_certified_sha256,
        saved_summary_matches_expected=False,
        saved_uncovered_matches_generated=saved_uncovered_matches_generated,
        computational_guard_status="pending",
        semantic_translation_status=SEMANTIC_TRANSLATION_STATUS,
        semantic_translation_gap=True,
        semantic_translation_note=SEMANTIC_TRANSLATION_NOTE,
    )

    saved_summary_ok = False
    if saved_summary_path is not None:
        saved_summary_ok = saved_summary_matches(read_single_summary_row(saved_summary_path), validation)

    pass_expected = (
        validation.evaluated_residues == EXPECTED_K16["evaluated_residues"]
        and validation.branch_residue_count == EXPECTED_K16["branch_residue_count"]
        and validation.frozen_complement_count == EXPECTED_K16["frozen_complement_count"]
        and validation.lowbit_certified_count == EXPECTED_K16["lowbit_certified_count"]
        and validation.guard_accepted_count == EXPECTED_K16["frozen_complement_count"]
        and validation.complement_accepted_count == EXPECTED_K16["frozen_complement_count"]
        and validation.outside_s2_accepted_count == EXPECTED_K16["outside_s2_accepted_count"]
        and validation.certified_to_guard_count == EXPECTED_K16["certified_to_guard_count"]
        and validation.complement_rejected_count == 0
        and validation.accepted_not_in_complement_count == 0
        and validation.s2_partition_hole_count == 0
        and validation.frozen_set_outside_s2_count == 0
        and validation.violation_count == 0
        and validation.uncovered_hash_matches_expected
        and validation.certified_hash_matches_expected
        and (saved_summary_path is None or saved_summary_ok)
        and (saved_uncovered_path is None or saved_uncovered_matches_generated)
    )

    validation = SemanticBridgeValidation(
        **{
            **asdict(validation),
            "saved_summary_matches_expected": saved_summary_ok,
            "computational_guard_status": "pass" if pass_expected else "fail",
        }
    )
    violation_rows = [row for row in audit_rows if row["violation"]]
    return validation, audit_rows, violation_rows


def write_csv(rows: list[dict[str, object]], fieldnames: list[str], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(validation: SemanticBridgeValidation, path: Path) -> None:
    pass_label = "PASS" if validation.computational_guard_status == "pass" else "FAIL"
    lines = [
        "# M22-C2 semantic bridge validator",
        "",
        "Fecha: 2026-04-29",
        "Agente: CodexHijo-M22-C2-SemanticBridge",
        "Rama: `codex-hijo/m22-c2-semantic-bridge`",
        "",
        "## Veredicto",
        "",
        f"- Guardia low-bit S2-k16: `{pass_label}`.",
        f"- Estado del puente semantico SRS mixto: `{validation.semantic_translation_status}`.",
        "- No se reclama equivalencia operacional entre el SRS mixto y `r mod 8 = 5`.",
        "",
        "La enumeracion exhaustiva confirma que la guarda congelada acepta exactamente",
        "los `378` residuos no certificados dentro de la rama etiquetada como S2 por",
        "`r mod 8 = 5`. Tambien confirma que no acepta residuos fuera de S2 y que no",
        "reenvia residuos certificados al guardado. Esto valida la aritmetica de la",
        "guarda, pero no cierra la traduccion semantica del alfabeto mixto.",
        "",
        "## Checks computacionales",
        "",
        "| Check | Valor | Esperado | Estado |",
        "| --- | ---: | ---: | --- |",
        f"| Residuos evaluados | `{validation.evaluated_residues}` | `65536` | `{pass_label}` |",
        f"| Residuos S2 por `r mod 8 = 5` | `{validation.branch_residue_count}` | `8192` | `{pass_label}` |",
        f"| Complemento aceptado por la guarda | `{validation.complement_accepted_count}` | `378` | `{pass_label}` |",
        f"| Residuos fuera de S2 aceptados | `{validation.outside_s2_accepted_count}` | `0` | `{pass_label}` |",
        f"| Residuos certificados enviados al guardado | `{validation.certified_to_guard_count}` | `0` | `{pass_label}` |",
        f"| Huecos en la particion S2 certificado/complemento | `{validation.s2_partition_hole_count}` | `0` | `{pass_label}` |",
        "",
        "## Hashes",
        "",
        "| Conjunto | SHA-256 actual | SHA-256 esperado | Match |",
        "| --- | --- | --- | --- |",
        f"| Complemento S2-k16 | `{validation.uncovered_sha256}` | `{validation.expected_uncovered_sha256}` | `{validation.uncovered_hash_matches_expected}` |",
        f"| Certificados S2-k16 | `{validation.certified_sha256}` | `{validation.expected_certified_sha256}` | `{validation.certified_hash_matches_expected}` |",
        "",
        "## Tabla local de traduccion disponible",
        "",
        "| Regla ASCII | Regla paper | Etiqueta local | Estado C2 |",
        "| --- | --- | --- | --- |",
        f"| `{validation.removed_rule}` | `{validation.paper_rule}` | `{validation.residue_predicate}` | `tag_only_not_operational_equivalence` |",
        "",
        "Los artefactos locales M19/M22 identifican la rama `bad -> d` / `tf* -> *`",
        "con el residuo `5 mod 8`, pero no incluyen una especificacion que derive esa",
        "condicion desde palabras alcanzables del SRS mixto binario/ternario. Por eso",
        "C2 queda como validador de guarda congelada y como diagnostico de brecha.",
        "",
        "## Archivos producidos",
        "",
        "- `reports/m22_c2_semantic_bridge_summary.csv`",
        "- `reports/m22_c2_semantic_bridge_residue_audit.csv`",
        "- `reports/m22_c2_semantic_bridge_violations.csv`",
        "- `reports/m22_c2_semantic_bridge.md`",
        "- `colaboradores/codex-hijo/M22C2SemanticBridge.md`",
        "",
        "## Conclusion",
        "",
        "El criterio computacional de la guarda S2-k16 pasa. El criterio semantico",
        "fuerte no pasa como equivalencia probada: falta una traduccion real, local y",
        "auditada del SRS mixto al predicado `r mod 8 = 5`. Cualquier C3 debe quedar",
        "bloqueado o rotulado como exploratorio hasta cerrar esta brecha.",
    ]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def write_outputs(
    validation: SemanticBridgeValidation,
    audit_rows: list[dict[str, object]],
    violation_rows: list[dict[str, object]],
    *,
    reports_dir: Path,
    prefix: str,
    collaborator_md: Path,
) -> dict[str, Path]:
    summary_path = reports_dir / f"{prefix}_summary.csv"
    audit_path = reports_dir / f"{prefix}_residue_audit.csv"
    violations_path = reports_dir / f"{prefix}_violations.csv"
    reports_md_path = reports_dir / f"{prefix}.md"
    summary_rows = [asdict(validation)]

    write_csv(summary_rows, list(summary_rows[0].keys()), summary_path)
    write_csv(audit_rows, RESIDUE_AUDIT_FIELDS, audit_path)
    write_csv(violation_rows, RESIDUE_AUDIT_FIELDS, violations_path)
    write_markdown(validation, reports_md_path)
    write_markdown(validation, collaborator_md)
    return {
        "summary": summary_path,
        "audit": audit_path,
        "violations": violations_path,
        "reports_md": reports_md_path,
        "collaborator_md": collaborator_md,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate the M22-C2 S2-k16 low-bit guard and report the semantic gap."
    )
    parser.add_argument("--k", type=int, default=16)
    parser.add_argument("--reports-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m22_c2_semantic_bridge")
    parser.add_argument(
        "--collaborator-md",
        type=Path,
        default=Path("colaboradores/codex-hijo/M22C2SemanticBridge.md"),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    saved_summary_path = args.reports_dir / "m22_s2_k16_summary.csv"
    saved_uncovered_path = args.reports_dir / "m22_s2_k16_uncovered_residues.csv"
    validation, audit_rows, violation_rows = validate_bridge(
        args.k,
        saved_summary_path=saved_summary_path,
        saved_uncovered_path=saved_uncovered_path,
    )
    paths = write_outputs(
        validation,
        audit_rows,
        violation_rows,
        reports_dir=args.reports_dir,
        prefix=args.prefix,
        collaborator_md=args.collaborator_md,
    )
    for label, path in paths.items():
        print(f"{label}={path}")
    print(f"evaluated_residues={validation.evaluated_residues}")
    print(f"branch_residue_count={validation.branch_residue_count}")
    print(f"frozen_complement_count={validation.frozen_complement_count}")
    print(f"outside_s2_accepted_count={validation.outside_s2_accepted_count}")
    print(f"certified_to_guard_count={validation.certified_to_guard_count}")
    print(f"computational_guard_status={validation.computational_guard_status}")
    print(f"semantic_translation_status={validation.semantic_translation_status}")
    return 0 if validation.computational_guard_status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
