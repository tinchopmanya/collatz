from __future__ import annotations

import argparse
import csv
import subprocess
import time
from pathlib import Path


def classify_output(text: str, return_code: int | None, timed_out: bool) -> str:
    upper = text.upper()
    if timed_out:
        return "TIMEOUT"

    # AProVE's WST status normally appears as a standalone line. Internal
    # subproofs can also contain YES, so do not classify by substring alone.
    for raw_line in text.splitlines():
        line = raw_line.strip().upper()
        if line in {"YES", "NO", "MAYBE", "ERROR", "TIMEOUT", "KILLED"}:
            return line

    if "JAVA HEAP SPACE" in upper or "OUTOFMEMORYERROR" in upper:
        return "OOM"
    if "CANNOT RUN PROGRAM" in upper or "PLEASE INSTALL" in upper:
        return "ENV_ERROR"
    if "ERROR" in upper or "EXCEPTION" in upper:
        return "ERROR"
    if return_code not in (0, None):
        return "ERROR"
    return "UNKNOWN"


def run_one(
    java: str,
    jar: Path,
    challenge: Path,
    timeout: int,
    wall_timeout: int,
    out_log: Path,
    dry_run: bool,
) -> dict[str, object]:
    cmd = [
        java,
        "-ea",
        "-jar",
        str(jar),
        "-m",
        "wst",
        str(challenge),
        "-p",
        "plain",
        "-t",
        str(timeout),
    ]
    start = time.monotonic()
    timed_out = False
    if dry_run:
        text = "DRY_RUN\n" + " ".join(cmd) + "\n"
        return_code = 0
    else:
        try:
            proc = subprocess.run(
                cmd,
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
    status = "DRY_RUN" if dry_run else classify_output(text, return_code, timed_out)
    return {
        "challenge": challenge.name,
        "challenge_path": str(challenge),
        "status": status,
        "return_code": "" if return_code is None else return_code,
        "timeout": timeout,
        "wall_timeout": wall_timeout,
        "elapsed_seconds": f"{elapsed:.3f}",
        "log": str(out_log),
    }


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "challenge",
        "challenge_path",
        "status",
        "return_code",
        "timeout",
        "wall_timeout",
        "elapsed_seconds",
        "log",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    successes = [row for row in rows if row["status"] == "YES"]
    killed = [row for row in rows if row["status"] == "KILLED"]
    env_errors = [row for row in rows if row["status"] == "ENV_ERROR"]
    lines = [
        "# M19 AProVE challenge run",
        "",
        "## Summary",
        "",
        f"- Runs: {len(rows)}",
        f"- YES: {len(successes)}",
        f"- KILLED: {len(killed)}",
        f"- ENV_ERROR: {len(env_errors)}",
        "",
        "| Challenge | Status | Seconds | Log |",
        "| --- | --- | ---: | --- |",
    ]
    for row in rows:
        lines.append(
            f"| `{row['challenge']}` | {row['status']} | {row['elapsed_seconds']} | `{row['log']}` |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Run AProVE on M19 TPDB challenge files.")
    parser.add_argument("--jar", type=Path, required=True)
    parser.add_argument("--challenge-file", type=Path, action="append", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=60)
    parser.add_argument("--wall-timeout", type=int, default=90)
    parser.add_argument("--java", default="java")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    args.out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = args.out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, object]] = []
    for challenge in args.challenge_file:
        log_path = log_dir / f"{challenge.stem}.aprove.log"
        row = run_one(
            java=args.java,
            jar=args.jar,
            challenge=challenge,
            timeout=args.timeout,
            wall_timeout=args.wall_timeout,
            out_log=log_path,
            dry_run=args.dry_run,
        )
        rows.append(row)
        print(row["challenge"], row["status"])

    write_csv(rows, args.out_dir / "m19_aprove_challenges.csv")
    write_markdown(rows, args.out_dir / "m19_aprove_challenges.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
