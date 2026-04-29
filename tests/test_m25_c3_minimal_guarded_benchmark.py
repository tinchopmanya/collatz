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
    DEFAULT_SELECTOR,
    build_from_files as build_m24_microguard,
    read_residue_csv,
)
from m25_c3_minimal_guarded_benchmark import (  # noqa: E402
    C3_BUILD_STATUS,
    DEFAULT_PREFIX,
    GUARDED_ASCII_RULE,
    build_from_files,
    dynamic_bad_rule_check,
    local_srs_anchor_checks,
    main,
    metadata_text,
    validate_c3_metadata,
    write_outputs,
)


class M25C3MinimalGuardedBenchmarkTests(unittest.TestCase):
    def test_default_build_passes_implication_checks_but_c3_is_blocked(self) -> None:
        metadata, checks = build_from_files(
            root=ROOT,
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )

        self.assertTrue(all(check.ok for check in checks))
        self.assertEqual("blocked", metadata.c3_build_status)
        self.assertEqual(C3_BUILD_STATUS, metadata.c3_build_status)
        self.assertFalse(metadata.emits_srs)
        self.assertEqual("none", metadata.prover_calls)
        self.assertEqual(DEFAULT_SELECTOR, metadata.selector)
        self.assertEqual(8, metadata.accepted_count)
        self.assertEqual(8, metadata.u16_selector_slice_count)
        self.assertEqual(0, metadata.certified_overlap_count)
        self.assertEqual(0, metadata.outside_u16_count)
        self.assertEqual(0, metadata.outside_dynamic_branch_count)

    def test_bad_rule_is_the_guarded_dynamic_branch_anchor(self) -> None:
        dynamic_info, dynamic_checks = dynamic_bad_rule_check()
        srs_info, srs_checks = local_srs_anchor_checks(ROOT)

        self.assertTrue(all(check.ok for check in dynamic_checks))
        self.assertTrue(all(check.ok for check in srs_checks))
        self.assertEqual("tf* -> *", dynamic_info["paper_rule"])
        self.assertEqual(GUARDED_ASCII_RULE, dynamic_info["ascii_rule"])
        self.assertEqual(8, dynamic_info["residue_modulus"])
        self.assertEqual(5, dynamic_info["residue"])
        self.assertEqual(["bad -> d"], srs_info["s2_removed_rules"])
        self.assertFalse(srs_info["s2_contains_bad"])

    def test_exact_u16_subset_is_checked_against_frozen_csv(self) -> None:
        microguard, m24_checks = build_m24_microguard(
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )
        uncovered = read_residue_csv(ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv")
        certified = read_residue_csv(ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv")

        metadata, checks = validate_c3_metadata(
            microguard=microguard,
            m24_checks=m24_checks,
            uncovered_residues=uncovered,
            certified_residues=certified,
            root=ROOT,
        )

        self.assertTrue(all(check.ok for check in checks))
        self.assertEqual(
            (8189, 16381, 24573, 32765, 40957, 49149, 57341, 65533),
            metadata.accepted_residues,
        )
        self.assertTrue(all(residue in set(uncovered) for residue in metadata.accepted_residues))
        self.assertTrue(all(residue not in set(certified) for residue in metadata.accepted_residues))
        self.assertTrue(all(residue % 8 == 5 for residue in metadata.accepted_residues))

    def test_rejects_microguard_when_u16_selector_slice_is_not_exact(self) -> None:
        microguard, m24_checks = build_m24_microguard(
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )
        uncovered = tuple(
            residue
            for residue in read_residue_csv(ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv")
            if residue != 8189
        )
        certified = read_residue_csv(ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv")

        _metadata, checks = validate_c3_metadata(
            microguard=microguard,
            m24_checks=m24_checks,
            uncovered_residues=uncovered,
            certified_residues=certified,
            root=ROOT,
        )

        failed = {check.name for check in checks if not check.ok}
        self.assertIn("microguard_exact_u16_selector_slice", failed)
        self.assertIn("microguard_subset_u16", failed)

    def test_metadata_text_documents_insertion_site_and_non_claims(self) -> None:
        metadata, checks = build_from_files(
            root=ROOT,
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )

        text = metadata_text(metadata)

        self.assertTrue(all(check.ok for check in checks))
        self.assertIn("c3_build_status: blocked", text)
        self.assertIn("exact_subset_statement: G_8189 = U_16 intersection", text)
        self.assertIn("anchor_rule_ascii: bad -> d", text)
        self.assertIn("insertion_point_status: conceptual_anchor_only_not_materialized", text)
        self.assertIn("does_not_emit_srs: true", text)
        self.assertIn("does_not_call_matchbox: true", text)
        self.assertNotIn("(RULES", text)

    def test_writes_only_metadata_summary_and_violations(self) -> None:
        metadata, checks = build_from_files(
            root=ROOT,
            candidate_csv=ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv",
            uncovered_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv",
            certified_csv=ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv",
        )
        with tempfile.TemporaryDirectory() as tmp:
            paths = write_outputs(metadata, checks, out_dir=Path(tmp), prefix=DEFAULT_PREFIX)
            emitted_names = {path.name for path in paths.values()}
            all_names = {path.name for path in Path(tmp).iterdir()}

            self.assertEqual(emitted_names, all_names)
            self.assertTrue(paths["metadata"].name.endswith(".metadata.txt"))
            self.assertTrue(paths["summary"].name.endswith("_summary.csv"))
            self.assertTrue(paths["violations"].name.endswith("_violations.csv"))
            self.assertFalse(any(name.endswith((".srs", ".tpdb", ".aprove.srs")) for name in all_names))
            with paths["summary"].open("r", encoding="utf-8", newline="") as handle:
                row = next(csv.DictReader(handle))
            self.assertEqual("blocked", row["c3_build_status"])
            self.assertEqual("True", row["implication_checks_passed"])
            self.assertEqual("False", row["emits_srs"])
            with paths["violations"].open("r", encoding="utf-8", newline="") as handle:
                self.assertEqual("check,ok,detail,residues", handle.readline().strip())
                self.assertEqual("", handle.readline())

    def test_cli_returns_zero_for_implication_checker(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            with redirect_stdout(io.StringIO()) as stdout:
                code = main(
                    [
                        "--root",
                        str(ROOT),
                        "--candidate-csv",
                        str(ROOT / "reports" / "m22_residual_stats_candidate_subfamilies.csv"),
                        "--uncovered-csv",
                        str(ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv"),
                        "--certified-csv",
                        str(ROOT / "reports" / "m22_c1_rechecker.certified_residues.csv"),
                        "--out-dir",
                        tmp,
                    ]
                )

        self.assertEqual(0, code)
        self.assertIn("m25_c3_minimal_guarded_benchmark=PASS", stdout.getvalue())
        self.assertIn("c3_build_status=blocked", stdout.getvalue())


if __name__ == "__main__":
    unittest.main()
