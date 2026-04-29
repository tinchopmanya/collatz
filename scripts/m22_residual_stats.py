from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Callable, Iterable


SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

from m22_freeze_s2_k16 import freeze_s2, residue_digest  # noqa: E402


EXPECTED_K = 16
EXPECTED_UNCOVERED_SHA256 = "bd04a1c2f65ccda483901f23fdb5f2392b824ac5b2d7ab1011e66f18771bb210"
DEFAULT_SOURCE_CSV = Path("reports/m22_s2_k16_uncovered_residues.csv")


@dataclass(frozen=True)
class ResidualSet:
    k: int
    modulus: int
    residues: list[int]
    sha256: str
    source: str


def bits_msb(value: int, width: int) -> str:
    return format(value, f"0{width}b")


def bits_lsb(value: int, width: int) -> str:
    return bits_msb(value, width)[::-1]


def reverse_bits(value: int, width: int) -> int:
    reversed_value = 0
    for _ in range(width):
        reversed_value = (reversed_value << 1) | (value & 1)
        value >>= 1
    return reversed_value


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


def branch_index(residue: int) -> int:
    if residue % 8 != 5:
        raise ValueError(f"residue is not in the S2 branch: {residue}")
    return (residue - 5) // 8


def residue_from_branch_index(index: int) -> int:
    return 5 + (8 * index)


def read_residue_csv(path: Path) -> list[int]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None or "residue" not in reader.fieldnames:
            raise ValueError(f"{path} must contain a 'residue' column")
        return [int(row["residue"]) for row in reader]


def build_residual_set(
    residues: Iterable[int],
    *,
    k: int,
    source: str,
    expected_sha256: str | None,
) -> ResidualSet:
    residue_list = list(residues)
    modulus = 1 << k
    if sorted(residue_list) != residue_list:
        raise ValueError("frozen residual list must be sorted in ascending order")
    if len(set(residue_list)) != len(residue_list):
        raise ValueError("frozen residual list contains duplicate residues")
    if any(residue < 0 or residue >= modulus for residue in residue_list):
        raise ValueError(f"all residues must be in [0, 2^{k})")
    if any(residue % 8 != 5 for residue in residue_list):
        raise ValueError("all frozen residuals must stay in the S2 branch: residue mod 8 = 5")

    digest = residue_digest(residue_list)
    if expected_sha256 is not None and digest != expected_sha256:
        raise ValueError(
            "unexpected frozen S2-k16 residual SHA-256: "
            f"got {digest}, expected {expected_sha256}"
        )
    return ResidualSet(k=k, modulus=modulus, residues=residue_list, sha256=digest, source=source)


def load_or_regenerate_residual_set(
    *,
    k: int = EXPECTED_K,
    source_csv: Path = DEFAULT_SOURCE_CSV,
    expected_sha256: str = EXPECTED_UNCOVERED_SHA256,
) -> ResidualSet:
    if k != EXPECTED_K:
        raise ValueError("M22 residual stats are pinned to S2 k=16")
    if source_csv.exists():
        residues = read_residue_csv(source_csv)
        source = str(source_csv)
    else:
        residues = freeze_s2(k).uncovered_residues
        source = "regenerated:m22_freeze_s2_k16.freeze_s2"
    return build_residual_set(
        residues,
        k=k,
        source=source,
        expected_sha256=expected_sha256,
    )


def s2_branch_capacity(k: int, predicate: Callable[[int], bool]) -> int:
    return sum(1 for residue in range(5, 1 << k, 8) if predicate(residue))


def distribution_rows(
    residual: ResidualSet,
    *,
    min_j: int = 3,
    max_j: int | None = None,
) -> list[dict[str, object]]:
    max_j = residual.k if max_j is None else max_j
    if min_j < 3:
        raise ValueError("min_j must be at least 3 for the S2 mod-8 branch")
    if max_j > residual.k:
        raise ValueError("max_j cannot exceed k")
    rows: list[dict[str, object]] = []
    total = len(residual.residues)
    for j in range(min_j, max_j + 1):
        modulus = 1 << j
        capacity = 1 << (residual.k - j)
        counts = Counter(residue % modulus for residue in residual.residues)
        for residue_mod, count in sorted(counts.items()):
            rows.append(
                {
                    "k": residual.k,
                    "total_residuals": total,
                    "j": j,
                    "modulus": modulus,
                    "residue_mod": residue_mod,
                    "residue_mod_binary_msb_first": bits_msb(residue_mod, j),
                    "residue_mod_binary_lsb_first": bits_lsb(residue_mod, j),
                    "count": count,
                    "fraction_of_residuals": f"{count / total:.12f}",
                    "s2_branch_capacity": capacity,
                    "density_within_s2_bucket": f"{count / capacity:.12f}",
                }
            )
    return rows


def block_rows(residual: ResidualSet) -> list[dict[str, object]]:
    indexes = [branch_index(residue) for residue in residual.residues]
    if not indexes:
        return []

    blocks: list[tuple[int, int]] = []
    start = previous = indexes[0]
    for index in indexes[1:]:
        if index == previous + 1:
            previous = index
            continue
        blocks.append((start, previous))
        start = previous = index
    blocks.append((start, previous))

    rows: list[dict[str, object]] = []
    previous_end: int | None = None
    for block_id, (start_index, end_index) in enumerate(blocks, start=1):
        start_residue = residue_from_branch_index(start_index)
        end_residue = residue_from_branch_index(end_index)
        length = end_index - start_index + 1
        rows.append(
            {
                "block_id": block_id,
                "k": residual.k,
                "start_branch_index": start_index,
                "end_branch_index": end_index,
                "start_residue": start_residue,
                "end_residue": end_residue,
                "start_residue_binary_msb_first": bits_msb(start_residue, residual.k),
                "end_residue_binary_msb_first": bits_msb(end_residue, residual.k),
                "start_residue_binary_lsb_first": bits_lsb(start_residue, residual.k),
                "end_residue_binary_lsb_first": bits_lsb(end_residue, residual.k),
                "length": length,
                "residue_step": 8,
                "span_width": end_residue - start_residue + 1,
                "gap_from_previous_branch_indices": ""
                if previous_end is None
                else start_index - previous_end - 1,
            }
        )
        previous_end = end_index
    return rows


def symmetry_rows(residual: ResidualSet) -> list[dict[str, object]]:
    residue_set = set(residual.residues)
    branch_width = residual.k - 3
    max_branch_index = (1 << branch_width) - 1
    rows: list[dict[str, object]] = []

    def add_row(
        *,
        name: str,
        kind: str,
        parameter: str,
        transform: Callable[[int], int],
        involutive: bool,
        note: str,
    ) -> None:
        images = [transform(residue) for residue in residual.residues]
        valid_images = [
            image for image in images if 0 <= image < residual.modulus and image % 8 == 5
        ]
        forward_hits = sum(1 for image in images if image in residue_set)
        fixed_points = sum(
            1
            for residue, image in zip(residual.residues, images)
            if residue == image and image in residue_set
        )
        hit_orbits = (
            fixed_points + ((forward_hits - fixed_points) // 2) if involutive else ""
        )
        rows.append(
            {
                "name": name,
                "kind": kind,
                "parameter": parameter,
                "k": residual.k,
                "checked_residuals": len(residual.residues),
                "preserves_s2_mod8": len(valid_images) == len(images),
                "forward_hits": forward_hits,
                "forward_hit_fraction": f"{forward_hits / len(residual.residues):.12f}",
                "fixed_points": fixed_points,
                "involutive": involutive,
                "hit_orbits_if_involutive": hit_orbits,
                "note": note,
            }
        )

    add_row(
        name="branch_index_reflection",
        kind="reflection",
        parameter=f"q -> {max_branch_index} - q",
        transform=lambda residue: residue_from_branch_index(
            max_branch_index - branch_index(residue)
        ),
        involutive=True,
        note="Reflects the 13-bit S2 branch index.",
    )
    add_row(
        name="branch_index_bit_reverse",
        kind="bit_reverse",
        parameter=f"reverse_bits(q,{branch_width})",
        transform=lambda residue: residue_from_branch_index(
            reverse_bits(branch_index(residue), branch_width)
        ),
        involutive=True,
        note="Reverses the branch-index bits after removing the fixed low suffix 101.",
    )
    for bit in range(3, residual.k):
        add_row(
            name=f"xor_residue_bit_{bit}",
            kind="xor",
            parameter=f"r -> r xor 2^{bit}",
            transform=lambda residue, bit=bit: residue ^ (1 << bit),
            involutive=True,
            note="Toggles one non-fixed residue bit, preserving r mod 8 = 5.",
        )
    for bit in range(3, residual.k):
        add_row(
            name=f"cyclic_shift_plus_2^{bit}",
            kind="cyclic_shift",
            parameter=f"r -> r + 2^{bit} mod 2^{residual.k}",
            transform=lambda residue, bit=bit: (residue + (1 << bit)) % residual.modulus,
            involutive=False,
            note="Cyclic shift inside the S2 branch; hit count equals overlap with that translate.",
        )
    return rows


def _candidate_row(
    *,
    k: int,
    family_type: str,
    selector: str,
    selector_bits: int,
    residues: list[int],
    capacity: int,
    rationale: str,
    selector_exact_for_u16: bool,
    m22_c1_c2_use: str,
) -> dict[str, object]:
    density = len(residues) / capacity if capacity else 0.0
    overinclude = 0 if selector_exact_for_u16 else max(capacity - len(residues), 0)
    return {
        "rank": 0,
        "family_type": family_type,
        "selector": selector,
        "selector_bits": selector_bits,
        "residue_count": len(residues),
        "selector_s2_branch_capacity": capacity,
        "density_within_selector": f"{density:.12f}",
        "selector_exact_for_u16": selector_exact_for_u16,
        "non_residual_s2_overinclude": overinclude,
        "m22_c1_c2_use": m22_c1_c2_use,
        "min_residue": min(residues),
        "max_residue": max(residues),
        "residues": " ".join(str(residue) for residue in residues),
        "residues_binary_msb_first": " ".join(bits_msb(residue, k) for residue in residues),
        "rationale": rationale,
    }


def _sort_candidates(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    category_rank = {
        "low_mod_bucket": 0,
        "msb_prefix": 1,
        "xor_overlap_family": 2,
        "exact_branch_block": 3,
    }

    def key(row: dict[str, object]) -> tuple[int, int, int, int, float, int]:
        density = float(row["density_within_selector"])
        exact_rank = 0 if row["selector_exact_for_u16"] is True else 1
        return (
            exact_rank,
            category_rank.get(str(row["family_type"]), 99),
            int(row["selector_bits"]),
            -int(row["residue_count"]),
            -density,
            int(row["min_residue"]),
        )

    return sorted(rows, key=key)


def prioritized_candidate_rows(
    residual: ResidualSet,
    *,
    max_family_size: int = 24,
    max_rows: int = 80,
) -> list[dict[str, object]]:
    if max_family_size < 2:
        raise ValueError("max_family_size must be at least 2")
    if max_rows < 1:
        raise ValueError("max_rows must be positive")

    residue_set = set(residual.residues)
    low_mod_candidates: list[dict[str, object]] = []
    for row in distribution_rows(residual, min_j=5, max_j=residual.k - 1):
        count = int(row["count"])
        if 2 <= count <= max_family_size:
            residue_mod = int(row["residue_mod"])
            modulus = int(row["modulus"])
            residues = [residue for residue in residual.residues if residue % modulus == residue_mod]
            capacity = int(row["s2_branch_capacity"])
            exact = count == capacity
            low_mod_candidates.append(
                _candidate_row(
                    k=residual.k,
                    family_type="low_mod_bucket",
                    selector=f"r mod 2^{row['j']} = {residue_mod}",
                    selector_bits=int(row["j"]),
                    residues=residues,
                    capacity=capacity,
                    rationale="Short low-bit guard; useful first target for guarded rewriting.",
                    selector_exact_for_u16=exact,
                    m22_c1_c2_use=(
                        "C2-exact microbenchmark after C1 recheck"
                        if exact
                        else "exploratory queue only; fails C2 if used alone"
                    ),
                )
            )

    msb_candidates: list[dict[str, object]] = []
    for prefix_bits in range(4, min(9, residual.k + 1)):
        counts = Counter(bits_msb(residue, residual.k)[:prefix_bits] for residue in residual.residues)
        for prefix, count in sorted(counts.items()):
            if not (2 <= count <= max_family_size):
                continue
            residues = [
                residue
                for residue in residual.residues
                if bits_msb(residue, residual.k).startswith(prefix)
            ]
            capacity = s2_branch_capacity(
                residual.k,
                lambda residue, prefix=prefix: bits_msb(residue, residual.k).startswith(prefix),
            )
            exact = count == capacity
            msb_candidates.append(
                _candidate_row(
                    k=residual.k,
                    family_type="msb_prefix",
                    selector=f"msb_prefix_{prefix_bits} = {prefix}",
                    selector_bits=prefix_bits,
                    residues=residues,
                    capacity=capacity,
                    rationale="Coarse contiguous region in the 16-bit residue space.",
                    selector_exact_for_u16=exact,
                    m22_c1_c2_use=(
                        "C2-exact microbenchmark after C1 recheck"
                        if exact
                        else "exploratory queue only; fails C2 if used alone"
                    ),
                )
            )

    xor_candidates: list[dict[str, object]] = []
    for bit in range(3, residual.k):
        participants = [
            residue for residue in residual.residues if (residue ^ (1 << bit)) in residue_set
        ]
        if 2 <= len(participants) <= max_family_size:
            xor_candidates.append(
                _candidate_row(
                    k=residual.k,
                    family_type="xor_overlap_family",
                    selector=f"r in U and r xor 2^{bit} in U",
                    selector_bits=bit + 1,
                    residues=participants,
                    capacity=len(participants),
                    rationale="Exact paired family suggested by a bit-toggle overlap.",
                    selector_exact_for_u16=False,
                    m22_c1_c2_use="diagnostic overlap only; not a standalone C2 guard",
                )
            )

    block_candidates: list[dict[str, object]] = []
    for row in block_rows(residual):
        length = int(row["length"])
        if 2 <= length <= max_family_size:
            start = int(row["start_residue"])
            end = int(row["end_residue"])
            residues = [residue for residue in residual.residues if start <= residue <= end]
            block_candidates.append(
                _candidate_row(
                    k=residual.k,
                    family_type="exact_branch_block",
                    selector=(
                        f"branch_index in [{row['start_branch_index']},"
                        f"{row['end_branch_index']}]"
                    ),
                    selector_bits=residual.k,
                    residues=residues,
                    capacity=length,
                    rationale="Exact adjacent S2 branch-index block; smallest no-slack family.",
                    selector_exact_for_u16=True,
                    m22_c1_c2_use="C2-exact microbenchmark after C1 recheck",
                )
            )

    low_mod_quota = max_rows // 2
    msb_quota = max_rows // 4
    xor_quota = max(1, max_rows // 8)
    block_quota = max_rows - low_mod_quota - msb_quota - xor_quota
    selected = (
        _sort_candidates(low_mod_candidates)[:low_mod_quota]
        + _sort_candidates(msb_candidates)[:msb_quota]
        + _sort_candidates(xor_candidates)[:xor_quota]
        + _sort_candidates(block_candidates)[:block_quota]
    )
    ranked = _sort_candidates(selected)[:max_rows]
    for rank, row in enumerate(ranked, start=1):
        row["rank"] = rank
    return ranked


def summary_rows(
    residual: ResidualSet,
    distribution: list[dict[str, object]],
    blocks: list[dict[str, object]],
    symmetries: list[dict[str, object]],
    candidates: list[dict[str, object]],
) -> list[dict[str, object]]:
    block_lengths = [int(row["length"]) for row in blocks]
    top_symmetry = max(symmetries, key=lambda row: int(row["forward_hits"]))
    return [
        {
            "k": residual.k,
            "modulus": residual.modulus,
            "source": residual.source,
            "residual_count": len(residual.residues),
            "residual_sha256": residual.sha256,
            "distribution_rows": len(distribution),
            "block_count": len(blocks),
            "singleton_blocks": sum(1 for length in block_lengths if length == 1),
            "max_block_length": max(block_lengths) if block_lengths else 0,
            "symmetry_rows": len(symmetries),
            "top_symmetry": top_symmetry["name"],
            "top_symmetry_forward_hits": top_symmetry["forward_hits"],
            "candidate_rows": len(candidates),
        }
    ]


def c1_c2_gate_rows(
    residual: ResidualSet,
    distribution: list[dict[str, object]],
    blocks: list[dict[str, object]],
    symmetries: list[dict[str, object]],
) -> list[dict[str, object]]:
    block_lengths = [int(row["length"]) for row in blocks]
    singleton_blocks = sum(1 for length in block_lengths if length == 1)
    lsb_trie_nodes = trie_node_count([bits_lsb(residue, residual.k) for residue in residual.residues])
    small_buckets = [
        row
        for row in distribution
        if 5 <= int(row["j"]) < residual.k and 2 <= int(row["count"]) <= 24
    ]
    exact_lowbit_buckets = [
        row
        for row in small_buckets
        if int(row["count"]) == int(row["s2_branch_capacity"])
    ]
    nonexact_small_buckets = [
        row
        for row in small_buckets
        if int(row["count"]) < int(row["s2_branch_capacity"])
    ]
    best_nonexact_density = (
        max(float(row["density_within_s2_bucket"]) for row in nonexact_small_buckets)
        if nonexact_small_buckets
        else 0.0
    )
    top_symmetry = max(symmetries, key=lambda row: int(row["forward_hits"]))
    all_residues_s2 = all(residue % 8 == 5 for residue in residual.residues)

    return [
        {
            "criterion": "M22-C1",
            "gate": "rechecker_independence",
            "status": "not_satisfied_by_this_script",
            "metric": "implementation_dependency",
            "value": "reads frozen CSV; fallback imports m22_freeze_s2_k16.freeze_s2",
            "comparator_or_threshold": "C1 requires an implementation that does not import M21/M22",
            "evidence": (
                "This stats script verifies the frozen SHA and shape, but it is not the "
                "independent rechecker requested by M22KillCriteria."
            ),
            "interpretation": (
                "Use these CSVs as fixtures and work queues for C1, not as completion of C1."
            ),
            "next_action": "Write a no-import rechecker that reproduces counts, hashes, false-positive checks, and affine checks.",
        },
        {
            "criterion": "M22-C1",
            "gate": "hash_count_anchor",
            "status": "partial_support",
            "metric": "residual_count/sha256/all_mod8_eq_5",
            "value": f"{len(residual.residues)}/{residual.sha256}/{all_residues_s2}",
            "comparator_or_threshold": EXPECTED_UNCOVERED_SHA256,
            "evidence": (
                "The loaded or regenerated U_16 set is sorted, unique, inside S2, and SHA-pinned."
            ),
            "interpretation": (
                "This supports C1 by making drift visible, but it does not test false positives "
                "or the affine invariant independently."
            ),
            "next_action": "Have C1 consume this SHA as the expected output, not as its input authority.",
        },
        {
            "criterion": "M22-C2",
            "gate": "exact_guard_feasibility",
            "status": "partial_support_needs_semantic_validator",
            "metric": "lsb_trie_nodes/block_count/singleton_blocks",
            "value": f"{lsb_trie_nodes}/{len(blocks)}/{singleton_blocks}",
            "comparator_or_threshold": "C2 must accept exactly 378/378 U_16 residues and 0 outside S2",
            "evidence": (
                f"{len(residual.residues)} residuals compress to {lsb_trie_nodes} LSB-trie "
                f"nodes; branch-index ranges split into {len(blocks)} blocks, "
                f"{singleton_blocks} singletons, max block {max(block_lengths) if block_lengths else 0}."
            ),
            "interpretation": (
                "Exact guarding is feasible as a finite object, but range compression is poor. "
                "C2 still needs the binary-residue to mixed-alphabet S2 validator."
            ),
            "next_action": "Generate the exact guard only after a validator proves the S2 branch translation.",
        },
        {
            "criterion": "M22-C2",
            "gate": "small_exact_lowbit_subfamilies",
            "status": "actionable_microbenchmarks_after_C1",
            "metric": "exact_lowbit_buckets_with_2_to_24_residuals",
            "value": len(exact_lowbit_buckets),
            "comparator_or_threshold": "exact buckets have 0 certified overinclude",
            "evidence": (
                f"{len(exact_lowbit_buckets)} low-bit buckets are exact subsets of U_16; "
                f"{len(small_buckets)} small buckets exist before exactness filtering."
            ),
            "interpretation": (
                "These are the safest small rewriting candidates because their simple selector "
                "does not admit certified S2 residues."
            ),
            "next_action": "Use exact buckets as C2-safe microbenchmarks, not as proof of the full bridge.",
        },
        {
            "criterion": "M22-C2",
            "gate": "coarse_selector_semantics",
            "status": "kill_if_used_alone",
            "metric": "best_nonexact_small_bucket_density",
            "value": f"{best_nonexact_density:.12f}",
            "comparator_or_threshold": "must be 1.0 for a coarse selector to be exact",
            "evidence": (
                f"{len(nonexact_small_buckets)} small low-bit buckets still overinclude "
                "non-residual S2 classes."
            ),
            "interpretation": (
                "Clustering is not a semantic shortcut. A non-exact bucket can guide search, "
                "but using it alone would change the S2 complement problem."
            ),
            "next_action": "Use non-exact buckets only as ranked work queues, never as standalone guards.",
        },
        {
            "criterion": "M22-C2",
            "gate": "symmetry_shortcut",
            "status": "weak_signal_only",
            "metric": "top_symmetry_forward_hits",
            "value": f"{top_symmetry['name']}:{top_symmetry['forward_hits']}",
            "comparator_or_threshold": f"{len(residual.residues)} hits would be closure",
            "evidence": (
                f"Best simple symmetry covers {top_symmetry['forward_hits']} of "
                f"{len(residual.residues)} directed images."
            ),
            "interpretation": (
                "Simple symmetries are useful diagnostics but do not close U_16 or replace "
                "the exact C2 guard."
            ),
            "next_action": "Do not quotient by these symmetries unless a later proof preserves S2 semantics.",
        },
    ]


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Profile the frozen M22 S2-k16 residual complement without Matchbox."
    )
    parser.add_argument("--source-csv", type=Path, default=DEFAULT_SOURCE_CSV)
    parser.add_argument("--out-dir", type=Path, default=Path("reports"))
    parser.add_argument("--prefix", default="m22_residual_stats")
    parser.add_argument("--min-j", type=int, default=3)
    parser.add_argument("--max-j", type=int, default=EXPECTED_K)
    parser.add_argument("--max-family-size", type=int, default=24)
    parser.add_argument("--max-candidates", type=int, default=80)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    residual = load_or_regenerate_residual_set(source_csv=args.source_csv)
    distribution = distribution_rows(residual, min_j=args.min_j, max_j=args.max_j)
    blocks = block_rows(residual)
    symmetries = symmetry_rows(residual)
    candidates = prioritized_candidate_rows(
        residual,
        max_family_size=args.max_family_size,
        max_rows=args.max_candidates,
    )
    summary = summary_rows(residual, distribution, blocks, symmetries, candidates)
    c1_c2 = c1_c2_gate_rows(residual, distribution, blocks, symmetries)

    summary_path = args.out_dir / f"{args.prefix}_summary.csv"
    distribution_path = args.out_dir / f"{args.prefix}_mod_distribution.csv"
    blocks_path = args.out_dir / f"{args.prefix}_branch_blocks.csv"
    symmetries_path = args.out_dir / f"{args.prefix}_symmetries.csv"
    candidates_path = args.out_dir / f"{args.prefix}_candidate_subfamilies.csv"
    c1_c2_path = args.out_dir / f"{args.prefix}_c1_c2_gate.csv"

    write_csv(summary, summary_path)
    write_csv(distribution, distribution_path)
    write_csv(blocks, blocks_path)
    write_csv(symmetries, symmetries_path)
    write_csv(candidates, candidates_path)
    write_csv(c1_c2, c1_c2_path)

    print(f"summary={summary_path}")
    print(f"mod_distribution={distribution_path}")
    print(f"branch_blocks={blocks_path}")
    print(f"symmetries={symmetries_path}")
    print(f"candidate_subfamilies={candidates_path}")
    print(f"c1_c2_gate={c1_c2_path}")
    print(f"residual_count={len(residual.residues)}")
    print(f"residual_sha256={residual.sha256}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
