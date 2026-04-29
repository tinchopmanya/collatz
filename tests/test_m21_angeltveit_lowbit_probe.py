import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m21_angeltveit_lowbit_probe import (  # noqa: E402
    audit_stratified_samples,
    collatz_t,
    count_residue_hits,
    iterate_prefix,
    lowbit_certified_residues,
    stratified_values,
)


class AngeltveitLowBitProbeTests(unittest.TestCase):
    def test_collatz_t_known_values(self) -> None:
        self.assertEqual(collatz_t(0), 0)
        self.assertEqual(collatz_t(1), 2)
        self.assertEqual(collatz_t(2), 1)
        self.assertEqual(collatz_t(3), 5)
        self.assertEqual(collatz_t(10), 5)

    def test_low_bits_determine_first_k_steps_affinely(self) -> None:
        for k in range(1, 9):
            modulus = 1 << k
            for residue in range(modulus):
                residue_prefix = iterate_prefix(residue, k)
                multiplier = 3 ** residue_prefix.odd_steps
                for lift in range(8):
                    n = residue + lift * modulus
                    lifted_prefix = iterate_prefix(n, k)
                    self.assertEqual(
                        lifted_prefix.value,
                        residue_prefix.value + multiplier * lift,
                        msg=f"k={k}, residue={residue}, lift={lift}",
                    )

    def test_certified_residues_have_no_small_false_positives(self) -> None:
        limit = 1 << 12
        for k in range(1, 11):
            certified = lowbit_certified_residues(k)
            modulus = 1 << k
            for n in range(1, limit):
                if n % modulus not in certified:
                    continue
                self.assertLess(iterate_prefix(n, k).value, n, msg=f"k={k}, n={n}")

    def test_residue_hit_count_matches_naive_count(self) -> None:
        for modulus in (2, 4, 8, 16, 32):
            residues = {0, 1, modulus - 1}
            for limit in range(1, 100):
                expected = sum(1 for n in range(1, limit) if n % modulus in residues)
                self.assertEqual(count_residue_hits(limit, modulus, residues), expected)

    def test_stratified_values_are_deterministic_boundary_samples(self) -> None:
        self.assertEqual(stratified_values(5, 5, 3), [5])
        self.assertEqual(stratified_values(0, 9, 1), [4])
        self.assertEqual(stratified_values(0, 9, 2), [0, 9])
        self.assertEqual(stratified_values(0, 9, 3), [0, 4, 9])

    def test_stratified_audit_catches_no_affine_failures_for_small_k(self) -> None:
        for k in range(2, 8):
            row = audit_stratified_samples(
                k,
                lowbit_certified_residues(k),
                max_power=10,
                residue_strata=4,
                residues_per_stratum=2,
                lifts_per_residue=3,
            )
            self.assertGreater(row["sampled_numbers"], 0)
            self.assertEqual(row["affine_failures"], 0)
            self.assertEqual(row["certified_false_positives"], 0)


if __name__ == "__main__":
    unittest.main()
