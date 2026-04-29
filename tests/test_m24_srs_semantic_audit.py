import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m24_srs_semantic_audit import (  # noqa: E402
    audit_dynamic_rules,
    audit_local_s2_files,
    paper_to_ascii,
    paper_word_affine,
    s_case_value,
)


class M24SRSSemanticAuditTests(unittest.TestCase):
    def test_tf_end_is_exactly_residue_5_mod_8(self) -> None:
        tf_end = paper_word_affine("tf*")

        self.assertEqual(8, tf_end.scale)
        self.assertEqual(5, tf_end.offset)
        for x in range(32):
            self.assertEqual(5, tf_end.value(x) % 8)

    def test_all_dynamic_s_branches_match_expected_residue_classes(self) -> None:
        rows = {row.paper_lhs: row for row in audit_dynamic_rules()}

        self.assertEqual((8, 1), (rows["ff*"].residue_modulus, rows["ff*"].residue))
        self.assertEqual((8, 5), (rows["tf*"].residue_modulus, rows["tf*"].residue))
        self.assertEqual((4, 3), (rows["t*"].residue_modulus, rows["t*"].residue))

    def test_ascii_translation_maps_bad_to_tf_end(self) -> None:
        self.assertEqual("aad", paper_to_ascii("ff*"))
        self.assertEqual("bad", paper_to_ascii("tf*"))
        self.assertEqual("bd", paper_to_ascii("t*"))

    def test_dynamic_rhs_matches_s_case_arithmetic(self) -> None:
        for row in audit_dynamic_rules():
            rhs = paper_word_affine(row.paper_rhs)
            for x in range(64):
                self.assertEqual(rhs.value(x), s_case_value(row, x))

    def test_local_s2_challenge_removes_only_bad_rule(self) -> None:
        audit = audit_local_s2_files(ROOT)

        self.assertEqual(12, audit["full_rule_count"])
        self.assertEqual(11, audit["s2_rule_count"])
        self.assertEqual(["bad -> d"], audit["s2_removed_rules"])
        self.assertTrue(audit["s2_removes_only_bad"])
        self.assertFalse(audit["s2_contains_bad"])


if __name__ == "__main__":
    unittest.main()
