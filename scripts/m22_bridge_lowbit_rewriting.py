from __future__ import annotations

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from m21_angeltveit_lowbit_probe import lowbit_certified_residues  # noqa: E402


@dataclass(frozen=True)
class RewritingBranch:
    name: str
    removed_rule: str
    paper_rule: str
    predicate: str

    def contains(self, residue: int) -> bool:
        if self.predicate == "mod8_eq_1":
            return residue % 8 == 1
        if self.predicate == "mod8_eq_5":
            return residue % 8 == 5
        if self.predicate == "mod4_eq_3":
            return residue % 4 == 3
        raise ValueError(f"unknown predicate: {self.predicate}")


BRANCHES = [
    RewritingBranch(
        name="S1_without_ff_end_to_0_end",
        removed_rule="aad -> ed",
        paper_rule="ff* -> 0*",
        predicate="mod8_eq_1",
    ),
    RewritingBranch(
        name="S2_without_tf_end_to_end",
        removed_rule="bad -> d",
        paper_rule="tf* -> *",
        predicate="mod8_eq_5",
    ),
    RewritingBranch(
        name="S3_without_t_end_to_2_end",
        removed_rule="bd -> gd",
        paper_rule="t* -> 2*",
        predicate="mod4_eq_3",
    ),
]


def branch_rows(ks: list[int]) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for k in ks:
        if k < 3:
            raise ValueError("k must be at least 3 to compare against mod-8 rewriting branches")
        modulus = 1 << k
        certified = lowbit_certified_residues(k)
        for branch in BRANCHES:
            branch_residues = [residue for residue in range(modulus) if branch.contains(residue)]
            certified_in_branch = sum(1 for residue in branch_residues if residue in certified)
            uncovered = len(branch_residues) - certified_in_branch
            rows.append(
                {
                    "k": k,
                    "modulus": modulus,
                    "branch": branch.name,
                    "removed_rule": branch.removed_rule,
                    "paper_rule": branch.paper_rule,
                    "predicate": branch.predicate,
                    "branch_residues": len(branch_residues),
                    "lowbit_certified": certified_in_branch,
                    "uncovered_residues": uncovered,
                    "certified_fraction": f"{certified_in_branch / len(branch_residues):.12f}",
                    "uncovered_fraction": f"{uncovered / len(branch_residues):.12f}",
                }
            )
    return rows


def uncovered_sample_rows(k: int, max_per_branch: int) -> list[dict[str, object]]:
    modulus = 1 << k
    certified = lowbit_certified_residues(k)
    rows: list[dict[str, object]] = []
    for branch in BRANCHES:
        uncovered = [
            residue
            for residue in range(modulus)
            if branch.contains(residue) and residue not in certified
        ]
        if len(uncovered) <= max_per_branch:
            sample = uncovered
        else:
            indexes = {
                (index * (len(uncovered) - 1)) // (max_per_branch - 1)
                for index in range(max_per_branch)
            }
            sample = [uncovered[index] for index in sorted(indexes)]
        for residue in sample:
            rows.append(
                {
                    "k": k,
                    "modulus": modulus,
                    "branch": branch.name,
                    "removed_rule": branch.removed_rule,
                    "residue": residue,
                    "residue_binary": format(residue, f"0{k}b"),
                    "residue_mod_8": residue % 8,
                }
            )
    return rows


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        raise ValueError("cannot write empty CSV")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    lines = [
        "# M22 low-bit to rewriting branch bridge",
        "",
        "This prototype measures whether M21 low-bit descent certificates can act as a",
        "preprocessor for the M19/Yolcu-Aaronson-Heule dynamic S branches. It does not",
        "generate a sound guarded SRS yet; it quantifies the residue slices that such a",
        "guarded benchmark would need to keep after low-bit discharge.",
        "",
        "| k | Branch | Removed rule | Predicate | Certified | Uncovered | Certified fraction |",
        "| ---: | --- | --- | --- | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            "| {k} | `{branch}` | `{removed_rule}` | `{predicate}` | "
            "{lowbit_certified}/{branch_residues} | {uncovered_residues} | "
            "{certified_fraction} |".format(**row)
        )
    lines.extend(
        [
            "",
            "Interpretation:",
            "",
            "- `S1` corresponds to the dynamic branch `aad -> ed` / `ff* -> 0*`, tagged in M19 as residue `1 mod 8`.",
            "- `S2` corresponds to `bad -> d` / `tf* -> *`, tagged as residue `5 mod 8`.",
            "- `S3` is the natural third dynamic branch `bd -> gd` / `t* -> 2*`, tagged as residue `3 mod 4`.",
            "- A guarded rewriting benchmark would need an independently checked translation from binary low-bit guards to the mixed binary/ternary SRS alphabet before any termination result is claimed.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write("\n".join(lines) + "\n")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Quantify low-bit descent coverage of M19 rewriting S branches."
    )
    parser.add_argument("--ks", default="8,10,12,14,16,18,20")
    parser.add_argument("--sample-k", type=int, default=16)
    parser.add_argument("--sample-size", type=int, default=16)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m22_bridge_lowbit_rewriting")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    ks = [int(part) for part in args.ks.split(",") if part.strip()]
    if not ks:
        raise ValueError("--ks must contain at least one integer")
    if max(ks + [args.sample_k]) > 20:
        raise ValueError("This bridge prototype reuses the small M21 probe; keep k <= 20.")
    rows = branch_rows(ks)
    sample_rows = uncovered_sample_rows(args.sample_k, args.sample_size)

    csv_path = args.out_dir / f"{args.prefix}.csv"
    md_path = args.out_dir / f"{args.prefix}.md"
    sample_path = args.out_dir / f"{args.prefix}_uncovered_samples.csv"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)
    write_csv(sample_rows, sample_path)

    print(f"csv={csv_path}")
    print(f"md={md_path}")
    print(f"sample_csv={sample_path}")
    print(f"rows={len(rows)}")
    print(f"sample_rows={len(sample_rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
