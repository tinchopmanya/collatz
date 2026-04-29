import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m22_residual_stats import (  # noqa: E402
    EXPECTED_UNCOVERED_SHA256,
    block_rows,
    build_residual_set,
    c1_c2_gate_rows,
    distribution_rows,
    load_or_regenerate_residual_set,
    prioritized_candidate_rows,
    symmetry_rows,
)


class M22ResidualStatsTests(unittest.TestCase):
    def mini_residual(self):
        return build_residual_set(
            [5, 13, 21, 45, 53],
            k=6,
            source="test",
            expected_sha256=None,
        )

    def test_loads_frozen_s2_k16_with_expected_sha(self) -> None:
        residual = load_or_regenerate_residual_set(
            source_csv=ROOT / "reports" / "m22_s2_k16_uncovered_residues.csv"
        )

        self.assertEqual(16, residual.k)
        self.assertEqual(378, len(residual.residues))
        self.assertEqual(EXPECTED_UNCOVERED_SHA256, residual.sha256)
        self.assertTrue(all(residue % 8 == 5 for residue in residual.residues))

    def test_regenerates_when_frozen_csv_is_missing(self) -> None:
        residual = load_or_regenerate_residual_set(
            source_csv=ROOT / "reports" / "missing_m22_s2_k16_uncovered_residues.csv"
        )

        self.assertEqual(378, len(residual.residues))
        self.assertEqual(EXPECTED_UNCOVERED_SHA256, residual.sha256)
        self.assertEqual("regenerated:m22_freeze_s2_k16.freeze_s2", residual.source)

    def test_distribution_rows_partition_each_modulus(self) -> None:
        rows = distribution_rows(self.mini_residual(), min_j=3, max_j=4)

        counts_by_j: dict[int, int] = {}
        for row in rows:
            counts_by_j.setdefault(int(row["j"]), 0)
            counts_by_j[int(row["j"])] += int(row["count"])

        self.assertEqual({3: 5, 4: 5}, counts_by_j)
        j4 = {row["residue_mod"]: row for row in rows if row["j"] == 4}
        self.assertEqual(3, j4[5]["count"])
        self.assertEqual(2, j4[13]["count"])
        self.assertEqual(4, j4[5]["s2_branch_capacity"])

    def test_block_rows_use_contiguous_s2_branch_indices(self) -> None:
        rows = block_rows(self.mini_residual())

        self.assertEqual(2, len(rows))
        self.assertEqual(0, rows[0]["start_branch_index"])
        self.assertEqual(2, rows[0]["end_branch_index"])
        self.assertEqual(3, rows[0]["length"])
        self.assertEqual(5, rows[1]["start_branch_index"])
        self.assertEqual(6, rows[1]["end_branch_index"])
        self.assertEqual(2, rows[1]["gap_from_previous_branch_indices"])

    def test_symmetry_rows_measure_bit_toggle_overlap(self) -> None:
        residual = build_residual_set(
            [5, 13, 21, 29],
            k=5,
            source="test",
            expected_sha256=None,
        )
        by_name = {row["name"]: row for row in symmetry_rows(residual)}

        self.assertEqual(4, by_name["xor_residue_bit_3"]["forward_hits"])
        self.assertEqual(2, by_name["xor_residue_bit_3"]["hit_orbits_if_involutive"])
        self.assertTrue(by_name["xor_residue_bit_3"]["preserves_s2_mod8"])

    def test_candidate_rows_are_ranked_and_small(self) -> None:
        rows = prioritized_candidate_rows(self.mini_residual(), max_family_size=4, max_rows=6)

        self.assertGreaterEqual(len(rows), 2)
        self.assertEqual(list(range(1, len(rows) + 1)), [row["rank"] for row in rows])
        self.assertEqual("low_mod_bucket", rows[0]["family_type"])
        self.assertTrue(rows[0]["selector_exact_for_u16"])
        self.assertEqual("C2-exact microbenchmark after C1 recheck", rows[0]["m22_c1_c2_use"])
        self.assertTrue(all(int(row["residue_count"]) <= 4 for row in rows))

    def test_rejects_wrong_expected_digest(self) -> None:
        with self.assertRaises(ValueError):
            build_residual_set(
                [5, 13],
                k=4,
                source="test",
                expected_sha256=EXPECTED_UNCOVERED_SHA256,
            )

    def test_c1_c2_gate_rows_separate_size_from_semantics(self) -> None:
        residual = self.mini_residual()
        rows = c1_c2_gate_rows(
            residual,
            distribution_rows(residual, min_j=3, max_j=6),
            block_rows(residual),
            symmetry_rows(residual),
        )
        by_gate = {row["gate"]: row for row in rows}

        self.assertEqual("M22-C1", by_gate["rechecker_independence"]["criterion"])
        self.assertEqual(
            "not_satisfied_by_this_script",
            by_gate["rechecker_independence"]["status"],
        )
        self.assertEqual("partial_support", by_gate["hash_count_anchor"]["status"])
        self.assertEqual("M22-C2", by_gate["exact_guard_feasibility"]["criterion"])
        self.assertEqual(
            "partial_support_needs_semantic_validator",
            by_gate["exact_guard_feasibility"]["status"],
        )
        self.assertEqual("kill_if_used_alone", by_gate["coarse_selector_semantics"]["status"])


if __name__ == "__main__":
    unittest.main()
