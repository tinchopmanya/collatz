import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m22_c2_semantic_bridge import (  # noqa: E402
    EXPECTED_K16,
    RESIDUE_AUDIT_FIELDS,
    SEMANTIC_TRANSLATION_STATUS,
    guard_accepts_residue,
    is_s2_branch_residue,
    validate_bridge,
    write_outputs,
)
from m22_freeze_s2_k16 import freeze_s2  # noqa: E402


class M22C2SemanticBridgeTests(unittest.TestCase):
    def test_validates_expected_s2_k16_guard_counts_and_hashes(self) -> None:
        validation, _audit_rows, violation_rows = validate_bridge(
            16,
            saved_summary_path=ROOT / "reports" / "m22_s2_k16_summary.csv",
            saved_uncovered_path=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
        )

        self.assertEqual(EXPECTED_K16["evaluated_residues"], validation.evaluated_residues)
        self.assertEqual(EXPECTED_K16["branch_residue_count"], validation.branch_residue_count)
        self.assertEqual(EXPECTED_K16["frozen_complement_count"], validation.frozen_complement_count)
        self.assertEqual(EXPECTED_K16["lowbit_certified_count"], validation.lowbit_certified_count)
        self.assertEqual(EXPECTED_K16["frozen_complement_count"], validation.complement_accepted_count)
        self.assertEqual(0, validation.outside_s2_accepted_count)
        self.assertEqual(0, validation.certified_to_guard_count)
        self.assertEqual(0, validation.violation_count)
        self.assertEqual([], violation_rows)
        self.assertTrue(validation.uncovered_hash_matches_expected)
        self.assertTrue(validation.certified_hash_matches_expected)
        self.assertTrue(validation.saved_summary_matches_expected)
        self.assertTrue(validation.saved_uncovered_matches_generated)
        self.assertEqual("pass", validation.computational_guard_status)

    def test_marks_mixed_srs_translation_as_unproved_gap(self) -> None:
        validation, _audit_rows, _violation_rows = validate_bridge(16)

        self.assertEqual(SEMANTIC_TRANSLATION_STATUS, validation.semantic_translation_status)
        self.assertTrue(validation.semantic_translation_gap)
        self.assertIn("do not contain", validation.semantic_translation_note)

    def test_guard_accepts_exactly_the_frozen_complement_inside_s2(self) -> None:
        frozen = freeze_s2(16)
        complement = set(frozen.uncovered_residues)
        certified = set(frozen.certified_residues)

        for residue in range(frozen.modulus):
            accepted = guard_accepts_residue(residue, complement)
            self.assertEqual(residue in complement, accepted)
            if accepted:
                self.assertTrue(is_s2_branch_residue(residue))
                self.assertNotIn(residue, certified)

    def test_writes_summary_audit_violations_and_markdown(self) -> None:
        validation, audit_rows, violation_rows = validate_bridge(16)
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            paths = write_outputs(
                validation,
                audit_rows,
                violation_rows,
                reports_dir=root / "reports",
                prefix="m22_c2_semantic_bridge",
                collaborator_md=root / "colaboradores" / "codex-hijo" / "M22C2SemanticBridge.md",
            )

            self.assertTrue(paths["summary"].exists())
            self.assertTrue(paths["audit"].exists())
            self.assertTrue(paths["violations"].exists())
            self.assertTrue(paths["reports_md"].exists())
            self.assertTrue(paths["collaborator_md"].exists())
            self.assertIn(
                "gap_unproven",
                paths["collaborator_md"].read_text(encoding="utf-8"),
            )
            with paths["violations"].open("r", encoding="utf-8", newline="") as handle:
                header = handle.readline().strip().split(",")
                self.assertEqual(RESIDUE_AUDIT_FIELDS, header)
                self.assertEqual("", handle.readline())


if __name__ == "__main__":
    unittest.main()
