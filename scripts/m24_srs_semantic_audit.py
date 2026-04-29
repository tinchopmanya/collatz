from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Affine:
    scale: int
    offset: int

    def after(self, inner: "Affine") -> "Affine":
        """Return self(inner(x))."""
        return Affine(
            self.scale * inner.scale,
            self.scale * inner.offset + self.offset,
        )

    def value(self, x: int) -> int:
        return self.scale * x + self.offset


@dataclass(frozen=True)
class DynamicRuleAudit:
    paper_lhs: str
    paper_rhs: str
    ascii_lhs: str
    ascii_rhs: str
    residue_modulus: int
    residue: int
    s_case: str

    @property
    def ascii_rule(self) -> str:
        return f"{self.ascii_lhs} -> {self.ascii_rhs}"

    @property
    def paper_rule(self) -> str:
        return f"{self.paper_lhs} -> {self.paper_rhs}"


PAPER_SYMBOLS: dict[str, Affine] = {
    "f": Affine(2, 0),
    "t": Affine(2, 1),
    "0": Affine(3, 0),
    "1": Affine(3, 1),
    "2": Affine(3, 2),
    "*": Affine(2, 1),
}

PAPER_TO_ASCII = {
    "f": "a",
    "t": "b",
    "*": "d",
    "0": "e",
    "1": "f",
    "2": "g",
}

DYNAMIC_RULES: tuple[tuple[str, str, str], ...] = (
    ("ff*", "0*", "(3n+1)/4 if n == 1 mod 8"),
    ("tf*", "*", "(n-1)/4 if n == 5 mod 8"),
    ("t*", "2*", "(3n+1)/2 if n == 3 mod 4"),
)


def paper_word_affine(word: str) -> Affine:
    result = Affine(1, 0)
    for symbol in word:
        result = PAPER_SYMBOLS[symbol].after(result)
    return result


def paper_to_ascii(word: str) -> str:
    return "".join(PAPER_TO_ASCII[symbol] for symbol in word)


def audit_dynamic_rules() -> list[DynamicRuleAudit]:
    rows: list[DynamicRuleAudit] = []
    for lhs, rhs, s_case in DYNAMIC_RULES:
        lhs_affine = paper_word_affine(lhs)
        rows.append(
            DynamicRuleAudit(
                paper_lhs=lhs,
                paper_rhs=rhs,
                ascii_lhs=paper_to_ascii(lhs),
                ascii_rhs=paper_to_ascii(rhs),
                residue_modulus=lhs_affine.scale,
                residue=lhs_affine.offset,
                s_case=s_case,
            )
        )
    return rows


def s_case_value(row: DynamicRuleAudit, x: int) -> int:
    n = paper_word_affine(row.paper_lhs).value(x)
    if row.paper_lhs == "ff*":
        return (3 * n + 1) // 4
    if row.paper_lhs == "tf*":
        return (n - 1) // 4
    if row.paper_lhs == "t*":
        return (3 * n + 1) // 2
    raise ValueError(f"unknown dynamic lhs: {row.paper_lhs}")


def read_plain_srs_rules(path: Path) -> list[str]:
    rules: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped:
            rules.append(stripped)
    return rules


def audit_local_s2_files(root: Path) -> dict[str, object]:
    challenges = root / "reports" / "m19_rewriting_challenges"
    full_rules = read_plain_srs_rules(challenges / "m19_collatz_S_full.srs")
    s2_rules = read_plain_srs_rules(challenges / "m19_collatz_S2_without_tf_end_to_end.srs")
    dynamic = {row.ascii_rule for row in audit_dynamic_rules()}
    removed = sorted(set(full_rules) - set(s2_rules))
    return {
        "full_rule_count": len(full_rules),
        "s2_rule_count": len(s2_rules),
        "dynamic_rules_present": sorted(dynamic.intersection(full_rules)),
        "s2_removed_rules": removed,
        "s2_removes_only_bad": removed == ["bad -> d"],
        "s2_contains_bad": "bad -> d" in s2_rules,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit the S dynamic branch residues used by M24."
    )
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()

    for row in audit_dynamic_rules():
        print(
            f"{row.paper_rule} | {row.ascii_rule} | "
            f"n = {row.residue_modulus}*x + {row.residue} | {row.s_case}"
        )
    local = audit_local_s2_files(args.root)
    print(f"S2 removed rules: {local['s2_removed_rules']}")
    print(f"S2 removes only bad -> d: {local['s2_removes_only_bad']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
