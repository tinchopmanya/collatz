import csv
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m24_microguard_design import (  # noqa: E402
    BLOCKED_BY,
    DEFAULT_SELECTOR,
    Candidate,
    build_from_files,
    guard_text,
    main,
    read_candidate,
    selector_residues,
    validate_microguard,
    write_outputs,
)


class M24MicroGuardDesignTests(unittest.TestCase):
    def test_8189_candidate_is_still_rank_one_and_exact(self) -> None:
        candidate = read_candidate(
            ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            DEFAULT_SELECTOR,
        )

        self.assertEqual(1, candidate.rank)
        self.assertEqual("low_mod_bucket", candidate.family_type)
        self.assertEqual(13, candidate.selector_bits)
        self.assertEqual(8189, candidate.selector_residue)
        self.assertTrue(candidate.selector_exact_for_u16)
        self.assertEqual(0, candidate.non_residual_s2_overinclude)
        self.assertEqual(
            (8189, 16381, 24573, 32765, 40957, 49149, 57341, 65533),
            candidate.residues,
        )

    def test_build_from_files_checks_finite_implication_only(self) -> None:
        artifact, checks = build_from_files(
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )

        self.assertTrue(all(check.ok for check in checks))
        self.assertEqual(8, artifact.accepted_count)
        self.assertEqual(8, artifact.frozen_selector_count)
        self.assertEqual(0, artifact.certified_overlap_count)
        self.assertEqual(0, artifact.outside_s2_count)
        self.assertEqual(BLOCKED_BY, artifact.blocked_by)
        self.assertEqual("blocked_by_M24-SRS-SemanticAudit", artifact.srs_equivalence_status)
        self.assertFalse(artifact.contains_certificates)

    def test_selector_residues_are_computed_not_trusted_from_csv(self) -> None:
        self.assertEqual(
            (8189, 16381, 24573, 32765, 40957, 49149, 57341, 65533),
            selector_residues(k=16, selector_bits=13, selector_residue=8189),
        )

    def test_rejects_guard_that_would_include_certified_residues(self) -> None:
        candidate = Candidate(
            rank=1,
            family_type="low_mod_bucket",
            selector="r mod 2^3 = 5",
            selector_bits=3,
            selector_residue=5,
            residue_count=2,
            selector_s2_branch_capacity=2,
            selector_exact_for_u16=True,
            non_residual_s2_overinclude=0,
            residues=(5, 13),
            rationale="test",
        )

        artifact, checks = validate_microguard(
            candidate=candidate,
            uncovered_residues=(13,),
            certified_residues=(5,),
            k=4,
            expected_uncovered_sha256=None,
            expected_certified_sha256=None,
        )

        failed = {check.name for check in checks if not check.ok}
        self.assertIn("guard_subset_frozen_complement", failed)
        self.assertIn("no_certified_residues", failed)
        self.assertEqual(1, artifact.certified_overlap_count)

    def test_writes_guard_summary_and_empty_violation_csv(self) -> None:
        artifact, checks = build_from_files(
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_outputs(artifact, checks, out_dir=Path(tmp), prefix="m24_test")

            for path in paths.values():
                self.assertTrue(path.exists(), msg=str(path))
            text = paths["guard"].read_text(encoding="utf-8")
            self.assertIn("no_srs_equivalence_claim: true", text)
            self.assertIn("contains_certificates: false", text)
            self.assertIn("prover_calls: none", text)
            self.assertNotIn("<certificationProblem", text)
            with paths["summary"].open("r", encoding="utf-8", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual("True", row["passed"])
            self.assertEqual("8", row["accepted_count"])
            self.assertEqual("0", row["certified_overlap_count"])
            with paths["violations"].open("r", encoding="utf-8", newline="") as handle:
                self.assertEqual("check,ok,detail,residues", handle.readline().strip())
                self.assertEqual("", handle.readline())

    def test_guard_text_keeps_non_claims_visible(self) -> None:
        artifact, checks = build_from_files(
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )

        text = guard_text(artifact)

        self.assertTrue(all(check.ok for check in checks))
        self.assertIn("does_not_generate_srs: true", text)
        self.assertIn("does_not_call_matchbox_or_aprove: true", text)
        self.assertIn("must_wait_for: M24-SRS-SemanticAudit", text)

    def test_cli_returns_zero_for_default_artifact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stdout(io.StringIO()) as stdout:
                code = main(
                    [
                        "--candidate-csv",
                        str(ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv"),
                        "--uncovered-csv",
                        str(ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv"),
                        "--certified-csv",
                        str(ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv"),
                        "--out-dir",
                        tmp,
                        "--prefix",
                        "m24_cli",
                    ]
                )

        self.assertEqual(0, code)
        self.assertIn("m24_microguard=PASS", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
