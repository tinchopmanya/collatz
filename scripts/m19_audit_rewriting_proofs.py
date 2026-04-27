from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


RUN_RE = re.compile(r"^run\s+(?P<path>\S+)\s+(?P<args>.+)$")
CNF_RE = re.compile(r"CNF:\s+(?P<vars>\d+)\s+variables,\s+(?P<clauses>\d+)\s+clauses")
SAT_RE = re.compile(r"\bSAT\s+\(Attempt\s+(?P<attempt>\d+),\s+(?P<seconds>[0-9.]+)\s+s\)")


@dataclass(frozen=True)
class ProofRun:
    source: str
    args: str
    log_name: str


def parse_proofs_sh(path: Path) -> list[ProofRun]:
    runs: list[ProofRun] = []
    for raw_line in path.read_text(encoding="utf-8").splitlines():
        match = RUN_RE.match(raw_line.strip())
        if not match:
            continue
        source = match.group("path")
        log_name = f"{Path(source).stem}.log"
        runs.append(ProofRun(source=source, args=match.group("args"), log_name=log_name))
    return runs


def parse_log(path: Path) -> dict[str, object]:
    if not path.exists():
        return {
            "log_exists": False,
            "has_sat": False,
            "has_qed": False,
            "variables": "",
            "clauses": "",
            "attempt": "",
            "sat_seconds": "",
        }

    text = path.read_text(encoding="utf-8", errors="replace")
    cnf = CNF_RE.search(text)
    sat = SAT_RE.search(text)
    return {
        "log_exists": True,
        "has_sat": sat is not None,
        "has_qed": "QED" in text,
        "variables": int(cnf.group("vars")) if cnf else "",
        "clauses": int(cnf.group("clauses")) if cnf else "",
        "attempt": int(sat.group("attempt")) if sat else "",
        "sat_seconds": float(sat.group("seconds")) if sat else "",
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "source",
        "log_name",
        "args",
        "log_exists",
        "has_sat",
        "has_qed",
        "variables",
        "clauses",
        "attempt",
        "sat_seconds",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path, repo_label: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    missing = [row for row in rows if not row["log_exists"]]
    failed = [row for row in rows if not row["has_sat"] or not row["has_qed"]]
    largest = sorted(
        (row for row in rows if isinstance(row["clauses"], int)),
        key=lambda row: int(row["clauses"]),
        reverse=True,
    )[:5]

    lines = [
        "# M19 rewriting proof inventory",
        "",
        f"External repo: `{repo_label}`",
        "",
        "## Summary",
        "",
        f"- Proof runs declared in `proofs.sh`: {len(rows)}",
        f"- Logs missing: {len(missing)}",
        f"- Logs without SAT or QED: {len(failed)}",
        "",
        "## Largest CNFs",
        "",
        "| Source | Variables | Clauses | SAT seconds |",
        "| --- | ---: | ---: | ---: |",
    ]
    for row in largest:
        lines.append(
            f"| `{row['source']}` | {row['variables']} | {row['clauses']} | {row['sat_seconds']} |"
        )

    lines.extend(
        [
            "",
            "## Full Inventory",
            "",
            "| Source | Log | Args | SAT | QED | Variables | Clauses |",
            "| --- | --- | --- | --- | --- | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            "| "
            f"`{row['source']}` | "
            f"`{row['log_name']}` | "
            f"`{row['args']}` | "
            f"{row['has_sat']} | "
            f"{row['has_qed']} | "
            f"{row['variables']} | "
            f"{row['clauses']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit rewriting-collatz proof logs against proofs.sh."
    )
    parser.add_argument("--repo", type=Path, required=True, help="Path to rewriting-collatz clone.")
    parser.add_argument("--repo-label", default="", help="Human-readable repo label for Markdown.")
    parser.add_argument("--csv", type=Path, required=True, help="CSV output path.")
    parser.add_argument("--md", type=Path, required=True, help="Markdown output path.")
    parser.add_argument(
        "--only-source",
        action="append",
        default=[],
        help="Restrict audit to one source path from proofs.sh. Can be repeated.",
    )
    args = parser.parse_args()

    repo = args.repo.resolve()
    proof_runs = parse_proofs_sh(repo / "proofs.sh")
    if args.only_source:
        wanted = {source.replace("\\", "/") for source in args.only_source}
        proof_runs = [proof_run for proof_run in proof_runs if proof_run.source in wanted]
        missing_sources = sorted(wanted - {proof_run.source for proof_run in proof_runs})
        if missing_sources:
            raise SystemExit(f"unknown proof source(s): {', '.join(missing_sources)}")

    rows: list[dict[str, object]] = []
    for proof_run in proof_runs:
        row = {
            "source": proof_run.source,
            "log_name": proof_run.log_name,
            "args": proof_run.args,
        }
        row.update(parse_log(repo / "proofs" / proof_run.log_name))
        rows.append(row)

    write_csv(rows, args.csv)
    repo_label = args.repo_label or str(repo)
    write_markdown(rows, args.md, repo_label)

    missing_or_failed = [
        row for row in rows if not row["log_exists"] or not row["has_sat"] or not row["has_qed"]
    ]
    if missing_or_failed:
        print(f"audit_failed={len(missing_or_failed)}")
        return 1

    print(f"proof_runs={len(rows)}")
    print(f"csv={args.csv}")
    print(f"md={args.md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
