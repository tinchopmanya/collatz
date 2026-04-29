from __future__ import annotations

import argparse
import csv
import hashlib
import sys
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from m21_angeltveit_lowbit_probe import lowbit_certified_residues  # noqa: E402


@dataclass(frozen=True)
class FrozenSet:
    k: int
    modulus: int
    branch_residues: list[int]
    certified_residues: list[int]
    uncovered_residues: list[int]


def residue_digest(residues: list[int]) -> str:
    payload = "\n".join(str(residue) for residue in residues) + "\n"
    return hashlib.sha256(payload.encode("ascii")).hexdigest()


def bitstring(residue: int, k: int, *, lsb_first: bool) -> str:
    bits = format(residue, f"0{k}b")
    return bits[::-1] if lsb_first else bits


def trie_node_count(words: list[str]) -> int:
    trie: dict[str, object] = {}
    count = 1
    for word in words:
        node = trie
        for char in word:
            if char not in node:
                node[char] = {}
                count += 1
            node = node[char]  # type: ignore[assignment]
    return count


def freeze_s2(k: int) -> FrozenSet:
    if k < 3:
        raise ValueError("k must be at least 3 for the S2 mod-8 branch")
    modulus = 1 << k
    certified = lowbit_certified_residues(k)
    branch_residues = [residue for residue in range(modulus) if residue % 8 == 5]
    certified_residues = [residue for residue in branch_residues if residue in certified]
    uncovered_residues = [residue for residue in branch_residues if residue not in certified]
    return FrozenSet(
        k=k,
        modulus=modulus,
        branch_residues=branch_residues,
        certified_residues=certified_residues,
        uncovered_residues=uncovered_residues,
    )


def summary_row(frozen: FrozenSet) -> dict[str, object]:
    lsb_words = [bitstring(residue, frozen.k, lsb_first=True) for residue in frozen.uncovered_residues]
    msb_words = [bitstring(residue, frozen.k, lsb_first=False) for residue in frozen.uncovered_residues]
    return {
        "branch": "S2_without_tf_end_to_end",
        "removed_rule": "bad -> d",
        "paper_rule": "tf* -> *",
        "predicate": "residue_mod_8_eq_5",
        "k": frozen.k,
        "modulus": frozen.modulus,
        "branch_residue_count": len(frozen.branch_residues),
        "lowbit_certified_count": len(frozen.certified_residues),
        "uncovered_count": len(frozen.uncovered_residues),
        "certified_fraction": f"{len(frozen.certified_residues) / len(frozen.branch_residues):.12f}",
        "uncovered_fraction": f"{len(frozen.uncovered_residues) / len(frozen.branch_residues):.12f}",
        "uncovered_sha256": residue_digest(frozen.uncovered_residues),
        "certified_sha256": residue_digest(frozen.certified_residues),
        "lsb_first_trie_nodes": trie_node_count(lsb_words),
        "msb_first_trie_nodes": trie_node_count(msb_words),
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        raise ValueError("cannot write empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_residues(frozen: FrozenSet, path: Path) -> None:
    rows = [
        {
            "residue": residue,
            "residue_binary_msb_first": bitstring(residue, frozen.k, lsb_first=False),
            "residue_binary_lsb_first": bitstring(residue, frozen.k, lsb_first=True),
            "residue_mod_8": residue % 8,
        }
        for residue in frozen.uncovered_residues
    ]
    write_csv(rows, path)


def write_markdown(frozen: FrozenSet, summary: dict[str, object], path: Path) -> None:
    lines = [
        "# M22a S2-k16 frozen complement",
        "",
        "This freezes the M22 candidate complement for the S2 branch before any guarded",
        "rewriting-system construction. It is a data artifact, not a proof.",
        "",
        "| Field | Value |",
        "| --- | ---: |",
    ]
    for key in [
        "k",
        "modulus",
        "branch_residue_count",
        "lowbit_certified_count",
        "uncovered_count",
        "certified_fraction",
        "uncovered_fraction",
        "lsb_first_trie_nodes",
        "msb_first_trie_nodes",
    ]:
        lines.append(f"| `{key}` | `{summary[key]}` |")
    lines.extend(
        [
            "",
            f"- Uncovered SHA-256: `{summary['uncovered_sha256']}`",
            f"- Certified SHA-256: `{summary['certified_sha256']}`",
            "- The LSB-first trie is the relevant first guess because the guard is low-bit driven.",
            "- The next step is semantic, not computational: prove that a guard over these bitstrings really matches the mixed binary/ternary SRS branch.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Freeze the M22 S2-k16 uncovered residue set.")
    parser.add_argument("--k", type=int, default=16)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m22_s2_k16")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    frozen = freeze_s2(args.k)
    summary = summary_row(frozen)
    residues_path = args.out_dir / f"{args.prefix}_uncovered_residues.csv"
    summary_path = args.out_dir / f"{args.prefix}_summary.csv"
    md_path = args.out_dir / f"{args.prefix}_frozen_complement.md"
    write_residues(frozen, residues_path)
    write_csv([summary], summary_path)
    write_markdown(frozen, summary, md_path)
    print(f"residues={residues_path}")
    print(f"summary={summary_path}")
    print(f"md={md_path}")
    print(f"uncovered={summary['uncovered_count']}")
    print(f"uncovered_sha256={summary['uncovered_sha256']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
