from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Rule:
    lhs: str
    rhs: str
    paper: str
    role: str


SYMBOL_MAP = {
    "a": "f",
    "b": "t",
    "c": "left marker",
    "d": "end marker",
    "e": "0",
    "f": "1",
    "g": "2",
}

COLLATZ_S_RULES = [
    Rule("aad", "ed", "ff* -> 0*", "dynamic S, residue 1 mod 8"),
    Rule("bad", "d", "tf* -> *", "dynamic S, residue 5 mod 8"),
    Rule("bd", "gd", "t* -> 2*", "dynamic S, residue 3 mod 4"),
    Rule("ae", "ea", "f0 -> 0f", "auxiliary A"),
    Rule("af", "eb", "f1 -> 0t", "auxiliary A"),
    Rule("ag", "fa", "f2 -> 1f", "auxiliary A"),
    Rule("be", "fb", "t0 -> 1t", "auxiliary A"),
    Rule("bf", "ga", "t1 -> 2f", "auxiliary A"),
    Rule("bg", "gb", "t2 -> 2t", "auxiliary A"),
    Rule("ce", "cb", "left 0 -> left t", "auxiliary B"),
    Rule("cf", "caa", "left 1 -> left ff", "auxiliary B"),
    Rule("cg", "cab", "left 2 -> left ft", "auxiliary B"),
]

CHALLENGES = {
    "S_full": {
        "filename": "m19_collatz_S_full.srs",
        "removed": None,
        "description": "Full accelerated S system from Yolcu-Aaronson-Heule.",
    },
    "S1_without_ff_end_to_0_end": {
        "filename": "m19_collatz_S1_without_ff_end_to_0_end.srs",
        "removed": "aad",
        "description": "Challenge S1: S without paper rule ff* -> 0*.",
    },
    "S2_without_tf_end_to_end": {
        "filename": "m19_collatz_S2_without_tf_end_to_end.srs",
        "removed": "bad",
        "description": "Challenge S2: S without paper rule tf* -> *.",
    },
}


def spaced(word: str) -> str:
    return " ".join(word)


def write_srs(rules: list[Rule], path: Path) -> None:
    path.write_text("\n".join(f"{rule.lhs} -> {rule.rhs}" for rule in rules) + "\n", encoding="utf-8")


def write_tpdb(rules: list[Rule], path: Path) -> None:
    lines = ["(RULES"]
    for index, rule in enumerate(rules):
        comma = "," if index < len(rules) - 1 else ""
        lines.append(f"  {spaced(rule.lhs)} -> {spaced(rule.rhs)} {comma}")
    lines.append(")")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_manifest(output_dir: Path, generated: list[tuple[str, Path, Path, list[Rule], Rule | None]]) -> None:
    lines = [
        "# M19 rewriting challenge files",
        "",
        "Date: 2026-04-27",
        "",
        "These files materialize the two explicit S-system challenges from Yolcu-Aaronson-Heule in the ASCII alphabet used by `rewriting-collatz`.",
        "",
        "## Symbol Map",
        "",
        "| ASCII | Paper symbol |",
        "| --- | --- |",
    ]
    for ascii_symbol, paper_symbol in SYMBOL_MAP.items():
        lines.append(f"| `{ascii_symbol}` | `{paper_symbol}` |")

    lines.extend(
        [
            "",
            "## Generated Files",
            "",
            "| Challenge | SRS | TPDB | Removed rule | Meaning |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for name, srs_path, tpdb_path, _rules, removed in generated:
        removed_text = "`none`" if removed is None else f"`{removed.lhs} -> {removed.rhs}`"
        meaning = "full S" if removed is None else removed.paper
        lines.append(
            f"| `{name}` | `{srs_path.name}` | `{tpdb_path.name}` | {removed_text} | {meaning} |"
        )

    lines.extend(
        [
            "",
            "## Rule Inventory",
            "",
            "| ASCII rule | Paper meaning | Role |",
            "| --- | --- | --- |",
        ]
    )
    for rule in COLLATZ_S_RULES:
        lines.append(f"| `{rule.lhs} -> {rule.rhs}` | {rule.paper} | {rule.role} |")

    lines.extend(
        [
            "",
            "## Research Status",
            "",
            "- These files do not prove termination.",
            "- They only make the two published open challenges concrete and reproducible.",
            "- Next step: run established termination tools against the TPDB files before inventing custom search.",
        ]
    )
    (output_dir / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate concrete S1/S2 rewriting challenge files for M19."
    )
    parser.add_argument("--out-dir", type=Path, default=Path("reports/m19_rewriting_challenges"))
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    generated: list[tuple[str, Path, Path, list[Rule], Rule | None]] = []

    for name, config in CHALLENGES.items():
        removed_lhs = config["removed"]
        rules = [rule for rule in COLLATZ_S_RULES if rule.lhs != removed_lhs]
        removed = next((rule for rule in COLLATZ_S_RULES if rule.lhs == removed_lhs), None)
        srs_path = args.out_dir / config["filename"]
        tpdb_path = srs_path.with_suffix(".tpdb")
        write_srs(rules, srs_path)
        write_tpdb(rules, tpdb_path)
        generated.append((name, srs_path, tpdb_path, rules, removed))

    write_manifest(args.out_dir, generated)
    for _name, srs_path, tpdb_path, rules, _removed in generated:
        print(f"{srs_path} rules={len(rules)}")
        print(f"{tpdb_path} rules={len(rules)}")
    print(args.out_dir / "README.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
