"""Minimal executable notes for Kevin Knight's 2026 Collatz rule.

Source: Kevin Knight, "A Small Collatz Rule without the Plus One",
Complex Systems 35(1), 2026, doi:10.25088/ComplexSystems.35.1.1.

The script records only the rule table printed in the paper and checks the
basic simulation claim on small Collatz terms encoded as powers of two.
"""

from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction


@dataclass(frozen=True)
class Branch:
    name: str
    residues_mod_30: tuple[int, ...]
    multiplier: Fraction
    exponent_delta: tuple[int, int, int]
    intended_state: str


BRANCHES: tuple[Branch, ...] = (
    Branch(
        "A",
        (2, 8),
        Fraction(375, 2),
        (-1, +1, +3),
        "odd Collatz term: pure 2^(2a+1)",
    ),
    Branch(
        "B",
        (0,),
        Fraction(125, 2),
        (-1, 0, +3),
        "odd-term inner loop: 2^a 3^b 5^c",
    ),
    Branch(
        "C",
        (3, 9, 15, 21, 27),
        Fraction(5, 3),
        (0, -1, +1),
        "3-to-5 transit, also supplies the odd +1 effect",
    ),
    Branch(
        "D",
        (5, 10, 20, 25),
        Fraction(2, 5),
        (+1, 0, -1),
        "5-to-2 transit",
    ),
    Branch(
        "E",
        (4, 6, 12, 16, 18, 24),
        Fraction(3, 4),
        (-2, +1, 0),
        "even Collatz term: 2-to-3 transit",
    ),
)

BRANCH_BY_RESIDUE = {
    residue: branch for branch in BRANCHES for residue in branch.residues_mod_30
}


def collatz_c(n: int) -> int:
    if n < 1:
        raise ValueError("Collatz terms must be positive")
    return n // 2 if n % 2 == 0 else 3 * n + 1


def k_step(n: int) -> tuple[int, Branch]:
    residue = n % 30
    branch = BRANCH_BY_RESIDUE.get(residue)
    if branch is None:
        raise ValueError(f"K is undefined for residue {residue} mod 30")
    next_n = n * branch.multiplier
    if next_n.denominator != 1:
        raise AssertionError(f"non-integral K step: {n} via {branch}")
    return next_n.numerator, branch


def is_power_of_two(n: int) -> bool:
    return n > 0 and n & (n - 1) == 0


def log2_power(n: int) -> int:
    if not is_power_of_two(n):
        raise ValueError(f"{n} is not a power of two")
    return n.bit_length() - 1


def k_until_next_power_of_two(collatz_term: int, max_steps: int = 100_000) -> tuple[int, list[str]]:
    start = 1 << collatz_term
    n = start
    branches: list[str] = []
    for _ in range(max_steps):
        n, branch = k_step(n)
        branches.append(branch.name)
        if is_power_of_two(n):
            return log2_power(n), branches
    raise RuntimeError(f"did not reach a power of two within {max_steps} K steps")


def expected_k_steps(collatz_term: int) -> int:
    if collatz_term % 2 == 1:
        # Knight writes 8m+6 for odd 2m+1; it also matches term 1.
        return 4 * collatz_term + 2
    return 3 * (collatz_term // 2)


def verify_rule_table() -> None:
    covered = sorted(BRANCH_BY_RESIDUE)
    if len(covered) != 18:
        raise AssertionError(f"expected 18 active residues, found {len(covered)}")
    if len(set(covered)) != len(covered):
        raise AssertionError("duplicate residues in Knight branch table")

    # The 30-condition K rule is not an integer-valued generalized Collatz map
    # on every raw representative of these residues. Knight explicitly notes
    # that a 60-condition K' variant is needed for that. Here we only assert
    # that each listed residue has at least one reachable 2^x 3^y 5^z witness
    # for which the branch is integral.
    witnesses: dict[int, int] = {}
    for x in range(0, 16):
        for y in range(0, 16):
            for z in range(0, 16):
                n = (2**x) * (3**y) * (5**z)
                residue = n % 30
                branch = BRANCH_BY_RESIDUE.get(residue)
                if branch is None or residue in witnesses:
                    continue
                value = n * branch.multiplier
                if value.denominator == 1:
                    witnesses[residue] = n
    missing = sorted(set(covered) - set(witnesses))
    if missing:
        raise AssertionError(f"no integral 2^x3^y5^z witness for residues {missing}")


def verify_simulation(limit: int) -> None:
    for term in range(1, limit + 1):
        projected, branches = k_until_next_power_of_two(term)
        expected = collatz_c(term)
        if projected != expected:
            raise AssertionError(
                f"term {term}: K projected to {projected}, expected C(term)={expected}"
            )
        expected_steps = expected_k_steps(term)
        if len(branches) != expected_steps:
            raise AssertionError(
                f"term {term}: K used {len(branches)} steps, expected {expected_steps}"
            )


def print_summary(limit: int) -> None:
    print("# M20 Knight rule executable notes")
    print()
    print("Active residues modulo 30:")
    for branch in BRANCHES:
        residues = ", ".join(str(r) for r in branch.residues_mod_30)
        print(
            f"- {branch.name}: residues {{{residues}}}, "
            f"multiply by {branch.multiplier}, delta {branch.exponent_delta}"
        )
    print()
    print(f"Verified K projection to Collatz C(n) for encoded terms 1..{limit}.")
    print()
    print("Sample term 3:")
    projected, branches = k_until_next_power_of_two(3)
    print(f"- 2^3 reaches 2^{projected} using {len(branches)} K steps")
    print(f"- branch word: {''.join(branches)}")


def main() -> None:
    limit = 40
    verify_rule_table()
    verify_simulation(limit)
    print_summary(limit)


if __name__ == "__main__":
    main()
