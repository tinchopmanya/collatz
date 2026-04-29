import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m22_bridge_lowbit_rewriting import (  # noqa: E402
    BRANCHES,
    branch_rows,
    uncovered_sample_rows,
)


class M22BridgeLowBitRewritingTests(unittest.TestCase):
    def test_branch_predicates_partition_dynamic_mod8_roles(self) -> None:
        by_name = {branch.name: branch for branch in BRANCHES}
        self.assertTrue(by_name["S1_without_ff_end_to_0_end"].contains(1))
        self.assertFalse(by_name["S1_without_ff_end_to_0_end"].contains(5))
        self.assertTrue(by_name["S2_without_tf_end_to_end"].contains(5))
        self.assertFalse(by_name["S2_without_tf_end_to_end"].contains(1))
        self.assertTrue(by_name["S3_without_t_end_to_2_end"].contains(3))
        self.assertTrue(by_name["S3_without_t_end_to_2_end"].contains(7))
        self.assertFalse(by_name["S3_without_t_end_to_2_end"].contains(5))

    def test_branch_rows_have_expected_modular_denominators(self) -> None:
        rows = branch_rows([8])
        by_branch = {row["branch"]: row for row in rows}
        self.assertEqual(by_branch["S1_without_ff_end_to_0_end"]["branch_residues"], 32)
        self.assertEqual(by_branch["S2_without_tf_end_to_end"]["branch_residues"], 32)
        self.assertEqual(by_branch["S3_without_t_end_to_2_end"]["branch_residues"], 64)
        for row in rows:
            covered = int(row["lowbit_certified"])
            uncovered = int(row["uncovered_residues"])
            total = int(row["branch_residues"])
            self.assertEqual(covered + uncovered, total)

    def test_uncovered_samples_respect_branch_predicates(self) -> None:
        rows = uncovered_sample_rows(8, 4)
        self.assertGreater(len(rows), 0)
        by_name = {branch.name: branch for branch in BRANCHES}
        for row in rows:
            self.assertTrue(by_name[str(row["branch"])].contains(int(row["residue"])))


if __name__ == "__main__":
    unittest.main()
