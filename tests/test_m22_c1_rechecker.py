import csv
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = ROOT / "scripts" / "m22_c1_rechecker.py"
sys.path.insert(0, str(ROOT / "scripts"))

from m22_c1_rechecker import (  # noqa: E402
    audit_stratified,
    accelerated_t,
    iterate_prefix,
    recheck_s2,
    residue_digest,
    validate_exhaustive,
    write_reports,
)


EXPECTED_UNCOVERED_SHA256 = "bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210"
EXPECTED_CERTIFIED_SHA256 = "0e8d2a804d7cc129a5fc6eec295250fd2a57786c25f2764e1bbd5100be01c7fa"


class M22C1RecheckerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.result = recheck_s2(16)

    def test_central_script_does_not_import_prior_m21_m22_logic(self) -> None:
        source = SCRIPT_PATH.read_text(encoding="utf-8")
        forbidden_imports = [
            "import m21_angeltveit_lowbit_probe",
            "from m21_angeltveit_lowbit_probe",
            "import m22_bridge_lowbit_rewriting",
            "from m22_bridge_lowbit_rewriting",
            "import m22_freeze_s2_k16",
            "from m22_freeze_s2_k16",
        ]
        for token in forbidden_imports:
            self.assertNotIn(token, source)

    def test_accelerated_t_known_values(self) -> None:
        self.assertEqual(accelerated_t(0), 0)
        self.assertEqual(accelerated_t(1), 2)
        self.assertEqual(accelerated_t(2), 1)
        self.assertEqual(accelerated_t(3), 5)
        self.assertEqual(accelerated_t(10), 5)

    def test_low_bits_determine_first_k_steps_affinely(self) -> None:
        for k in range(1, 9):
            modulus = 1 << k
            for residue in range(modulus):
                prefix = iterate_prefix(residue, k)
                multiplier = 3**prefix.odd_steps
                for lift in range(8):
                    n = residue + lift * modulus
                    lifted = iterate_prefix(n, k)
                    self.assertEqual(
                        prefix.value + multiplier * lift,
                        lifted.value,
                        msg=f"k={k}, residue={residue}, lift={lift}",
                    )

    def test_recomputes_expected_s2_k16_residue_sets(self) -> None:
        self.assertEqual(len(self.result.branch_residues), 8192)
        self.assertEqual(len(self.result.certified_residues), 7814)
        self.assertEqual(len(self.result.uncovered_residues), 378)
        self.assertTrue(all(residue % 8 == 5 for residue in self.result.branch_residues))
        self.assertTrue(all(residue % 8 == 5 for residue in self.result.uncovered_residues))
        self.assertEqual(tuple(sorted(self.result.uncovered_residues)), self.result.uncovered_residues)
        self.assertEqual(residue_digest(self.result.uncovered_residues), EXPECTED_UNCOVERED_SHA256)
        self.assertEqual(residue_digest(self.result.certified_residues), EXPECTED_CERTIFIED_SHA256)

    def test_exhaustive_validation_to_2_20_has_no_false_positives(self) -> None:
        validation = validate_exhaustive(self.result, limit_exclusive=1 << 20)
        self.assertEqual(validation.checked_candidates, 7814 * 16)
        self.assertEqual(validation.false_positives, 0)

    def test_stratified_audit_meets_m22_c1_thresholds(self) -> None:
        audit = audit_stratified(self.result)
        self.assertGreaterEqual(audit.sampled_numbers, 288)
        self.assertGreaterEqual(audit.max_lift_seen, 255)
        self.assertEqual(audit.affine_failures, 0)
        self.assertEqual(audit.certified_false_positives, 0)

    def test_write_reports_emits_summary_and_residue_artifacts(self) -> None:
        validation = validate_exhaustive(self.result, limit_exclusive=1 << 12)
        audit = audit_stratified(
            self.result,
            audit_max_power=20,
            residue_strata=8,
            residues_per_stratum=2,
            lifts_per_residue=2,
        )
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_reports(
                self.result,
                validation,
                audit,
                out_dir=Path(tmp),
                prefix="m22_c1_rechecker",
            )
            for path in paths.values():
                self.assertTrue(path.exists(), msg=str(path))
            with paths["summary_csv"].open(encoding="utf-8", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual(row["branch_residue_count"], "8192")
            self.assertEqual(row["lowbit_certified_count"], "7814")
            self.assertEqual(row["uncovered_count"], "378")
            self.assertEqual(row["false_positives"], "0")


if __name__ == "__main__":
    unittest.main()
