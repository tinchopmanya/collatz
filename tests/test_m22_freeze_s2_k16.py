import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m22_freeze_s2_k16 import freeze_s2, residue_digest, summary_row  # noqa: E402


class M22FreezeS2K16Tests(unittest.TestCase):
    def test_freezes_expected_s2_k16_complement(self) -> None:
        frozen = freeze_s2(16)

        self.assertEqual(8192, len(frozen.branch_residues))
        self.assertEqual(7814, len(frozen.certified_residues))
        self.assertEqual(378, len(frozen.uncovered_residues))
        self.assertTrue(all(residue % 8 == 5 for residue in frozen.uncovered_residues))
        self.assertEqual(sorted(frozen.uncovered_residues), frozen.uncovered_residues)

    def test_digest_is_order_sensitive_and_stable(self) -> None:
        residues = freeze_s2(16).uncovered_residues

        self.assertEqual(residue_digest(residues), residue_digest(list(residues)))
        self.assertNotEqual(residue_digest(residues), residue_digest(list(reversed(residues))))

    def test_summary_has_smaller_lsb_first_trie(self) -> None:
        summary = summary_row(freeze_s2(16))

        self.assertEqual("378", str(summary["uncovered_count"]))
        self.assertLess(
            int(summary["lsb_first_trie_nodes"]),
            int(summary["msb_first_trie_nodes"]),
        )


if __name__ == "__main__":
    unittest.main()
