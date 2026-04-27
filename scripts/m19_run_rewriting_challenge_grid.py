from __future__ import annotations

import argparse
import csv
import re
import shutil
import subprocess
import time
from pathlib import Path


CNF_RE = re.compile(r"CNF:\s+(?P<vars>\d+)\s+variables,\s+(?P<clauses>\d+)\s+clauses")
SAT_RE = re.compile(r"\bSAT\s+\(Attempt\s+(?P<attempt>\d+),\s+(?P<seconds>[0-9.]+)\s+s\)")


def parse_int_set(spec: str) -> list[int]:
    values: set[int] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            left, right = part.split("-", 1)
            start = int(left)
            stop = int(right)
            if stop < start:
                raise ValueError(f"invalid range: {part}")
            values.update(range(start, stop + 1))
        else:
            values.add(int(part))
    return sorted(values)


def parse_csv(spec: str) -> list[str]:
    return [part.strip() for part in spec.split(",") if part.strip()]


def venv_python(rewriting_repo: Path) -> str:
    candidates = [
        rewriting_repo / ".venv" / "bin" / "python",
        rewriting_repo / ".venv" / "Scripts" / "python.exe",
    ]
    for candidate in candidates:
        if candidate.exists():
            return str(candidate)
    return "python"


def status_from_return_code(return_code: int | None, timed_out: bool, text: str) -> str:
    if timed_out:
        return "TIMEOUT"
    if return_code == 19 and "QED" in text:
        return "QED"
    if return_code == 11:
        return "PARTIAL"
    if return_code == 29:
        return "UNSAT"
    if return_code == 0 and "DRY_RUN" in text:
        return "DRY_RUN"
    return "ERROR"


def parse_log(text: str) -> dict[str, object]:
    cnf_matches = list(CNF_RE.finditer(text))
    sat_matches = list(SAT_RE.finditer(text))
    cnf = cnf_matches[-1] if cnf_matches else None
    sat = sat_matches[-1] if sat_matches else None
    return {
        "has_qed": "QED" in text,
        "has_sat": sat is not None,
        "variables": int(cnf.group("vars")) if cnf else "",
        "clauses": int(cnf.group("clauses")) if cnf else "",
        "sat_attempt": int(sat.group("attempt")) if sat else "",
        "sat_seconds": float(sat.group("seconds")) if sat else "",
    }


def safe_stem(path: Path) -> str:
    return path.stem.replace(" ", "_").replace("/", "_").replace("\\", "_")


def run_one(
    python_exe: str,
    rewriting_repo: Path,
    relative_rulefile: str,
    out_log: Path,
    interpretation: str,
    dimension: int,
    result_width: int,
    remove_any: bool,
    solver_timeout: int,
    workers: int,
    tries: int,
    wall_timeout: int,
    dry_run: bool,
) -> dict[str, object]:
    cmd = [
        python_exe,
        "prover/main.py",
        relative_rulefile,
        "-i",
        interpretation,
        "-d",
        str(dimension),
        "-rw",
        str(result_width),
        "-work",
        str(workers),
        "-tout",
        str(solver_timeout),
        "-try",
        str(tries),
        "--printascii",
    ]
    if remove_any:
        cmd.append("-any")

    start = time.monotonic()
    timed_out = False
    if dry_run:
        text = "DRY_RUN\n" + " ".join(cmd) + "\n"
        return_code = 0
    else:
        try:
            proc = subprocess.run(
                cmd,
                cwd=rewriting_repo,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                timeout=wall_timeout,
                check=False,
            )
            text = proc.stdout
            return_code = proc.returncode
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            text = exc.stdout or ""
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")
            return_code = None

    elapsed = time.monotonic() - start
    out_log.write_text(text, encoding="utf-8", errors="replace")
    parsed = parse_log(text)
    status = status_from_return_code(return_code, timed_out, text)

    row = {
        "challenge": Path(relative_rulefile).name,
        "rulefile": relative_rulefile,
        "interpretation": interpretation,
        "dimension": dimension,
        "result_width": result_width,
        "remove_any": remove_any,
        "solver_timeout": solver_timeout,
        "workers": workers,
        "tries": tries,
        "wall_timeout": wall_timeout,
        "status": status,
        "return_code": "" if return_code is None else return_code,
        "elapsed_seconds": f"{elapsed:.3f}",
        "log": str(out_log),
    }
    row.update(parsed)
    return row


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "challenge",
        "rulefile",
        "interpretation",
        "dimension",
        "result_width",
        "remove_any",
        "solver_timeout",
        "workers",
        "tries",
        "wall_timeout",
        "status",
        "return_code",
        "elapsed_seconds",
        "has_qed",
        "has_sat",
        "variables",
        "clauses",
        "sat_attempt",
        "sat_seconds",
        "log",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    successes = [row for row in rows if row["status"] == "QED"]
    timeouts = [row for row in rows if row["status"] == "TIMEOUT"]
    errors = [row for row in rows if row["status"] == "ERROR"]
    lines = [
        "# M19 rewriting challenge grid",
        "",
        "## Summary",
        "",
        f"- Runs: {len(rows)}",
        f"- QED: {len(successes)}",
        f"- Timeouts: {len(timeouts)}",
        f"- Errors: {len(errors)}",
        "",
    ]
    if successes:
        lines.extend(["## Successful Runs", "", "| Challenge | Interpretation | d | rw | Log |", "| --- | --- | ---: | ---: | --- |"])
        for row in successes:
            lines.append(
                f"| `{row['challenge']}` | {row['interpretation']} | {row['dimension']} | {row['result_width']} | `{row['log']}` |"
            )
        lines.append("")

    lines.extend(
        [
            "## Full Grid",
            "",
            "| Challenge | Interpretation | d | rw | Status | CNF vars | CNF clauses | Seconds |",
            "| --- | --- | ---: | ---: | --- | ---: | ---: | ---: |",
        ]
    )
    for row in rows:
        lines.append(
            f"| `{row['challenge']}` | {row['interpretation']} | {row['dimension']} | {row['result_width']} | "
            f"{row['status']} | {row['variables']} | {row['clauses']} | {row['elapsed_seconds']} |"
        )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run a bounded rewriting-collatz S1/S2 search grid."
    )
    parser.add_argument("--rewriting-repo", type=Path, required=True)
    parser.add_argument("--challenge-file", type=Path, action="append", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--interpretations", default="natural,arctic")
    parser.add_argument("--dimensions", default="1-3")
    parser.add_argument("--result-widths", default="2-5")
    parser.add_argument("--solver-timeout", type=int, default=30)
    parser.add_argument("--wall-timeout", type=int, default=60)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--tries", type=int, default=1)
    parser.add_argument("--remove-any", action="store_true")
    parser.add_argument("--stop-on-success", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    rewriting_repo = args.rewriting_repo.resolve()
    challenge_dir = rewriting_repo / "m19_challenges"
    log_dir = args.out_dir / "logs"
    challenge_dir.mkdir(parents=True, exist_ok=True)
    log_dir.mkdir(parents=True, exist_ok=True)

    relative_rulefiles: list[str] = []
    for challenge_file in args.challenge_file:
        destination = challenge_dir / challenge_file.name
        shutil.copyfile(challenge_file, destination)
        relative_rulefiles.append(destination.relative_to(rewriting_repo).as_posix())

    rows: list[dict[str, object]] = []
    python_exe = venv_python(rewriting_repo)

    for relative_rulefile in relative_rulefiles:
        for interpretation in parse_csv(args.interpretations):
            for dimension in parse_int_set(args.dimensions):
                for result_width in parse_int_set(args.result_widths):
                    log_name = (
                        f"{safe_stem(Path(relative_rulefile))}_{interpretation}_"
                        f"d{dimension}_rw{result_width}.log"
                    )
                    row = run_one(
                        python_exe=python_exe,
                        rewriting_repo=rewriting_repo,
                        relative_rulefile=relative_rulefile,
                        out_log=log_dir / log_name,
                        interpretation=interpretation,
                        dimension=dimension,
                        result_width=result_width,
                        remove_any=args.remove_any,
                        solver_timeout=args.solver_timeout,
                        workers=args.workers,
                        tries=args.tries,
                        wall_timeout=args.wall_timeout,
                        dry_run=args.dry_run,
                    )
                    rows.append(row)
                    print(
                        row["challenge"],
                        row["interpretation"],
                        f"d={row['dimension']}",
                        f"rw={row['result_width']}",
                        row["status"],
                    )
                    if args.stop_on_success and row["status"] == "QED":
                        write_csv(rows, args.out_dir / "m19_challenge_grid.csv")
                        write_markdown(rows, args.out_dir / "m19_challenge_grid.md")
                        return 0

    write_csv(rows, args.out_dir / "m19_challenge_grid.csv")
    write_markdown(rows, args.out_dir / "m19_challenge_grid.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
