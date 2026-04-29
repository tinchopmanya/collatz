from __future__ import annotations

import argparse
import csv
import json
import os
import re
import shlex
import subprocess
import time
from pathlib import Path
from typing import Any


VERDICTS = {"YES", "NO", "MAYBE"}
STATUSES = VERDICTS | {"TIMEOUT", "ERROR"}
ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]")


def split_command(command: str) -> list[str]:
    return shlex.split(command, posix=os.name != "nt")


def clean_line(line: str) -> str:
    return ANSI_RE.sub("", line).strip()


def first_nonempty_line(text: str) -> str | None:
    for raw_line in text.splitlines():
        line = clean_line(raw_line)
        if line:
            return line
    return None


def classify_output(text: str, return_code: int | None, timed_out: bool) -> str:
    if timed_out:
        return "TIMEOUT"

    first = first_nonempty_line(text)
    if first is not None:
        upper_first = first.upper()
        if upper_first in {"TIMEOUT", "ERROR"}:
            return upper_first
        if upper_first in VERDICTS and return_code in (0, None):
            return upper_first

    upper_text = text.upper()
    if return_code in {124, 137, 143}:
        return "TIMEOUT"
    if any(token in upper_text for token in ("TIMEOUT", "TIMED OUT", "TIME LIMIT")):
        return "TIMEOUT"
    if any(
        token in upper_text
        for token in (
            "CANNOT EXECUTE",
            "COMMAND NOT FOUND",
            "NO SUCH FILE",
            "PARSE ERROR",
            "EXCEPTION",
            "FATAL",
            "ERROR",
        )
    ):
        return "ERROR"
    if return_code not in (0, None):
        return "ERROR"

    # Matchbox/TermComp-style YES/NO/MAYBE is expected as the first stdout line.
    # If logs contain no top-level verdict, keep the result safe and inconclusive.
    return "MAYBE"


def sha256_file(path: Path) -> str:
    import hashlib

    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def run_one(
    command: list[str],
    extra_args: list[str],
    challenge: Path,
    wall_timeout: int,
    out_log: Path,
    dry_run: bool,
) -> dict[str, Any]:
    cmd = [*command, *extra_args, str(challenge)]
    start = time.monotonic()
    timed_out = False
    return_code: int | None

    if dry_run:
        text = "DRY_RUN\n" + " ".join(shlex.quote(part) for part in cmd) + "\n"
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
                encoding="utf-8",
                errors="replace",
            )
            text = proc.stdout
            return_code = proc.returncode
        except FileNotFoundError as exc:
            text = f"ERROR: cannot execute Matchbox command: {exc}\n"
            return_code = 127
        except subprocess.TimeoutExpired as exc:
            timed_out = True
            text = exc.stdout or ""
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")
            text += f"\nTIMEOUT: outer wall timeout after {wall_timeout} seconds\n"
            return_code = None

    elapsed = time.monotonic() - start
    out_log.write_text(text, encoding="utf-8", errors="replace")
    status = "MAYBE" if dry_run else classify_output(text, return_code, timed_out)
    first_line = first_nonempty_line(text) or ""

    return {
        "challenge": challenge.name,
        "challenge_path": str(challenge),
        "challenge_sha256": sha256_file(challenge) if challenge.exists() else "",
        "status": status,
        "top_line": first_line,
        "return_code": "" if return_code is None else return_code,
        "wall_timeout": wall_timeout,
        "elapsed_seconds": f"{elapsed:.3f}",
        "command": " ".join(shlex.quote(part) for part in cmd),
        "log": str(out_log),
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "challenge",
        "challenge_path",
        "challenge_sha256",
        "status",
        "top_line",
        "return_code",
        "wall_timeout",
        "elapsed_seconds",
        "command",
        "log",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(rows: list[dict[str, Any]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(rows, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown(rows: list[dict[str, Any]], path: Path) -> None:
    counts = {status: 0 for status in ["YES", "NO", "MAYBE", "TIMEOUT", "ERROR"]}
    for row in rows:
        counts[str(row["status"])] = counts.get(str(row["status"]), 0) + 1

    lines = [
        "# M19 Matchbox challenge run",
        "",
        "## Summary",
        "",
        f"- Runs: {len(rows)}",
        f"- YES: {counts.get('YES', 0)}",
        f"- NO: {counts.get('NO', 0)}",
        f"- MAYBE: {counts.get('MAYBE', 0)}",
        f"- TIMEOUT: {counts.get('TIMEOUT', 0)}",
        f"- ERROR: {counts.get('ERROR', 0)}",
        "",
        "## Results",
        "",
        "| Challenge | Status | Seconds | Return code | First non-empty output line | Log |",
        "| --- | --- | ---: | ---: | --- | --- |",
    ]
    for row in rows:
        top_line = str(row["top_line"]).replace("|", "\\|")
        if len(top_line) > 80:
            top_line = top_line[:77] + "..."
        lines.append(
            f"| `{row['challenge']}` | {row['status']} | {row['elapsed_seconds']} | "
            f"{row['return_code']} | `{top_line}` | `{row['log']}` |"
        )

    lines.extend(
        [
            "",
            "## Classification Rule",
            "",
            "The runner only accepts `YES`, `NO`, `MAYBE`, `TIMEOUT`, or `ERROR` when it appears as the exact first non-empty output line after ANSI stripping.",
            "Internal occurrences such as proof subgoals, solver messages, or prose are not treated as top-level Matchbox verdicts.",
            "If Matchbox exits successfully without a top-level verdict, this report records `MAYBE` rather than promoting a substring to `YES`.",
        ]
    )

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run Matchbox on M19 TPDB/SRS challenge files with conservative verdict parsing."
    )
    parser.add_argument(
        "--matchbox-command",
        default="matchbox2015",
        help="Executable or quoted command prefix, e.g. 'matchbox2015 --satchmo --bits 4'.",
    )
    parser.add_argument(
        "--matchbox-arg",
        action="append",
        default=[],
        help="Extra argument appended before the challenge path. Use --matchbox-arg=--cpf for flags.",
    )
    parser.add_argument("--challenge-file", type=Path, action="append", required=True)
    parser.add_argument("--out-dir", type=Path, required=True)
    parser.add_argument("--wall-timeout", type=int, default=180)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    command = split_command(args.matchbox_command)
    if not command:
        raise SystemExit("--matchbox-command must not be empty")

    args.out_dir.mkdir(parents=True, exist_ok=True)
    log_dir = args.out_dir / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    rows: list[dict[str, Any]] = []
    for challenge in args.challenge_file:
        log_path = log_dir / f"{challenge.stem}.matchbox.log"
        row = run_one(
            command=command,
            extra_args=args.matchbox_arg,
            challenge=challenge,
            wall_timeout=args.wall_timeout,
            out_log=log_path,
            dry_run=args.dry_run,
        )
        rows.append(row)
        print(row["challenge"], row["status"])

    write_csv(rows, args.out_dir / "m19_matchbox_challenges.csv")
    write_json(rows, args.out_dir / "m19_matchbox_challenges.json")
    write_markdown(rows, args.out_dir / "m19_matchbox_challenges.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
