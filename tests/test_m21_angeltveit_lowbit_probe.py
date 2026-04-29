import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m21_angeltveit_lowbit_probe import (  # noqa: E402
    collatz_t,
    iterate_prefix,
    lowbit_certified_residues,
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


if __name__ == "__main__":
    unittest.main()
