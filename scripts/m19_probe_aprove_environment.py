from __future__ import annotations

import argparse
import csv
import json
import os
import platform
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


WST_STATUSES = {"YES", "NO", "MAYBE", "ERROR", "TIMEOUT", "KILLED"}


def total_memory_mb() -> int | None:
    if sys.platform.startswith("linux"):
        meminfo = Path("/proc/meminfo")
        if meminfo.exists():
            for line in meminfo.read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("MemTotal:"):
                    parts = line.split()
                    if len(parts) >= 2:
                        return int(parts[1]) // 1024
    if sys.platform == "darwin":
        try:
            proc = subprocess.run(
                ["sysctl", "-n", "hw.memsize"],
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL,
                timeout=5,
                check=False,
            )
            if proc.returncode == 0:
                return int(proc.stdout.strip()) // (1024 * 1024)
        except (OSError, subprocess.SubprocessError, ValueError):
            return None
    if sys.platform.startswith("win"):
        try:
            import ctypes

            class MemoryStatus(ctypes.Structure):
                _fields_ = [
                    ("dwLength", ctypes.c_ulong),
                    ("dwMemoryLoad", ctypes.c_ulong),
                    ("ullTotalPhys", ctypes.c_ulonglong),
                    ("ullAvailPhys", ctypes.c_ulonglong),
                    ("ullTotalPageFile", ctypes.c_ulonglong),
                    ("ullAvailPageFile", ctypes.c_ulonglong),
                    ("ullTotalVirtual", ctypes.c_ulonglong),
                    ("ullAvailVirtual", ctypes.c_ulonglong),
                    ("ullAvailExtendedVirtual", ctypes.c_ulonglong),
                ]

            status = MemoryStatus()
            status.dwLength = ctypes.sizeof(MemoryStatus)
            if ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(status)):
                return int(status.ullTotalPhys // (1024 * 1024))
        except Exception:
            return None
    return None


def run_cmd(
    cmd: list[str],
    timeout: int = 10,
    stdin: str | None = None,
) -> dict[str, Any]:
    exe = shutil.which(cmd[0])
    row: dict[str, Any] = {
        "cmd": cmd,
        "path": exe or "",
        "found": exe is not None,
        "return_code": "",
        "timed_out": False,
        "stdout": "",
    }
    if exe is None:
        return row
    try:
        proc = subprocess.run(
            cmd,
            input=stdin,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
        row["return_code"] = proc.returncode
        row["stdout"] = proc.stdout
    except subprocess.TimeoutExpired as exc:
        row["timed_out"] = True
        text = exc.stdout or ""
        if isinstance(text, bytes):
            text = text.decode("utf-8", errors="replace")
        row["stdout"] = text
    except OSError as exc:
        row["stdout"] = f"{type(exc).__name__}: {exc}"
    return row


def first_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def probe_commands() -> dict[str, Any]:
    yices_e = run_cmd(["yices", "-e"], timeout=5, stdin="")
    yices_e_text = str(yices_e["stdout"]).lower()
    return {
        "java_version": run_cmd(["java", "-version"], timeout=10),
        "yices_version": run_cmd(["yices", "--version"], timeout=10),
        "yices_e_empty_stdin": yices_e,
        "minisat2_help": run_cmd(["minisat2", "-help"], timeout=10),
        "minisat_help": run_cmd(["minisat", "-help"], timeout=10),
        "derived": {
            "yices_e_supported": bool(yices_e["found"])
            and not yices_e["timed_out"]
            and "invalid option" not in yices_e_text
            and "unknown option" not in yices_e_text,
            "minisat2_on_path": bool(shutil.which("minisat2")),
            "minisat_on_path": bool(shutil.which("minisat")),
        },
    }


def parse_srs(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {
            "path": str(path),
            "exists": False,
            "suffixes": path.suffixes,
            "aprove_srs_suffix": path.name.endswith(".srs"),
            "starts_rules": False,
            "has_var_section": False,
            "rule_count": 0,
            "rules": [],
        }
    text = path.read_text(encoding="utf-8", errors="replace")
    rules = []
    in_rules = False
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("(RULES"):
            in_rules = True
            suffix = line[len("(RULES") :].strip()
            if suffix:
                line = suffix
            else:
                continue
        if line == ")":
            in_rules = False
            continue
        if in_rules and "->" in line:
            rules.append(line.rstrip(",").strip())
    return {
        "path": str(path),
        "exists": path.exists(),
        "suffixes": path.suffixes,
        "aprove_srs_suffix": path.name.endswith(".srs"),
        "starts_rules": text.lstrip().startswith("(RULES"),
        "has_var_section": "(VAR" in text,
        "rule_count": len(rules),
        "rules": rules,
    }


def classify_aprove_output(text: str, return_code: int | None, timed_out: bool) -> str:
    upper = text.upper()
    lower = text.lower()
    if timed_out:
        return "WALL_TIMEOUT"
    if "INVALID OPTION: -E" in upper or ("yices" in lower and "invalid option" in lower):
        return "ENV_YICES_E_INCOMPATIBLE"
    if "CANNOT RUN PROGRAM" in upper and "YICES" in upper:
        return "ENV_MISSING_YICES"
    if "CANNOT RUN PROGRAM" in upper and "MINISAT2" in upper:
        return "ENV_MISSING_MINISAT2"
    if "PLEASE INSTALL" in upper and "MINISAT" in upper:
        return "ENV_MISSING_MINISAT2"
    if "JAVA HEAP SPACE" in upper or "OUTOFMEMORYERROR" in upper:
        return "ENV_JAVA_OOM"
    if "PARSE ERROR" in upper or "LEXICAL ERROR" in upper:
        return "INPUT_PARSE_ERROR"

    for raw_line in text.splitlines():
        line = raw_line.strip().upper()
        if line in WST_STATUSES:
            return f"WST_{line}"

    if return_code not in (0, None):
        return "APROVE_ERROR"
    return "UNKNOWN"


def run_aprove(
    java: str,
    jar: Path,
    challenge: Path,
    timeout: int,
    wall_timeout: int,
    out_log: Path,
    dry_run: bool,
) -> dict[str, Any]:
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
        return_code: int | None = 0
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
    out_log.parent.mkdir(parents=True, exist_ok=True)
    out_log.write_text(text, encoding="utf-8", errors="replace")
    status = "DRY_RUN" if dry_run else classify_aprove_output(text, return_code, timed_out)
    return {
        "challenge": challenge.name,
        "challenge_path": str(challenge),
        "status": status,
        "return_code": "" if return_code is None else return_code,
        "timeout": timeout,
        "wall_timeout": wall_timeout,
        "elapsed_seconds": f"{elapsed:.3f}",
        "log": str(out_log),
        "first_output_line": first_line(text),
    }


def write_csv(rows: list[dict[str, Any]], path: Path) -> None:
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
        "first_output_line",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def markdown_bool(value: object) -> str:
    return "yes" if value else "no"


def write_markdown(data: dict[str, Any], path: Path) -> None:
    command_probe = data["command_probe"]
    derived = command_probe["derived"]
    lines = [
        "# M19 AProVE environment probe",
        "",
        "## Environment",
        "",
        f"- Platform: `{data['platform']['platform']}`",
        f"- Python: `{data['platform']['python']}`",
        f"- CPU count: `{data['platform']['cpu_count']}`",
        f"- Total memory MB: `{data['platform']['total_memory_mb']}`",
        f"- JAVA_TOOL_OPTIONS: `{data['environment'].get('JAVA_TOOL_OPTIONS', '')}`",
        "",
        "## Tool Probe",
        "",
        "| Tool check | Found | Path | Return | First output |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for key in ["java_version", "yices_version", "yices_e_empty_stdin", "minisat2_help", "minisat_help"]:
        row = command_probe[key]
        lines.append(
            f"| `{key}` | {markdown_bool(row['found'])} | `{row['path']}` | "
            f"`{row['return_code']}` | `{first_line(str(row['stdout']))}` |"
        )
    lines.extend(
        [
            "",
            "## Derived Environment Classification",
            "",
            f"- `yices -e` supported: {markdown_bool(derived['yices_e_supported'])}",
            f"- `minisat2` on PATH: {markdown_bool(derived['minisat2_on_path'])}",
            f"- `minisat` on PATH: {markdown_bool(derived['minisat_on_path'])}",
            "",
            "## SRS Inputs",
            "",
            "| File | `.srs` suffix | Starts `(RULES` | Rule count |",
            "| --- | --- | --- | ---: |",
        ]
    )
    for row in data["srs_probe"]:
        lines.append(
            f"| `{Path(row['path']).name}` | {markdown_bool(row['aprove_srs_suffix'])} | "
            f"{markdown_bool(row['starts_rules'])} | {row['rule_count']} |"
        )

    aprove_runs = data.get("aprove_runs", [])
    lines.extend(["", "## AProVE Runs", ""])
    if aprove_runs:
        lines.extend(
            [
                "| Challenge | Status | Return | Seconds | First output | Log |",
                "| --- | --- | ---: | ---: | --- | --- |",
            ]
        )
        for row in aprove_runs:
            lines.append(
                f"| `{row['challenge']}` | `{row['status']}` | `{row['return_code']}` | "
                f"{row['elapsed_seconds']} | `{row['first_output_line']}` | `{row['log']}` |"
            )
    else:
        lines.append("AProVE was not run because no `--jar` was provided.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `ENV_*` statuses are environment blockers, not mathematical evidence.",
            "- `WST_MAYBE`, `WST_TIMEOUT`, `WST_KILLED`, or `WALL_TIMEOUT` mean no proof was found in this run.",
            "- Only `WST_YES` is a candidate proof signal, and it still needs log/certificate audit.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def default_challenges() -> list[Path]:
    base = Path("reports") / "m19_rewriting_challenges"
    return [
        base / "m19_collatz_S1_without_ff_end_to_0_end.aprove.srs",
        base / "m19_collatz_S2_without_tf_end_to_end.aprove.srs",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Probe whether the local/CI environment is suitable for AProVE S1/S2 runs."
    )
    parser.add_argument("--jar", type=Path)
    parser.add_argument("--challenge-file", type=Path, action="append")
    parser.add_argument("--out-dir", type=Path, default=Path(tempfile.gettempdir()) / "m19_aprove_environment_probe")
    parser.add_argument("--timeout", type=int, default=20)
    parser.add_argument("--wall-timeout", type=int, default=45)
    parser.add_argument("--java", default="java")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    challenges = args.challenge_file or default_challenges()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    data: dict[str, Any] = {
        "platform": {
            "platform": platform.platform(),
            "python": sys.version.replace("\n", " "),
            "cpu_count": os.cpu_count(),
            "total_memory_mb": total_memory_mb(),
        },
        "environment": {
            "JAVA_TOOL_OPTIONS": os.environ.get("JAVA_TOOL_OPTIONS", ""),
            "_JAVA_OPTIONS": os.environ.get("_JAVA_OPTIONS", ""),
            "PATH": os.environ.get("PATH", ""),
        },
        "command_probe": probe_commands(),
        "srs_probe": [parse_srs(path) for path in challenges],
        "aprove_runs": [],
    }

    if args.jar is not None:
        log_dir = args.out_dir / "logs"
        rows = []
        for challenge in challenges:
            row = run_aprove(
                java=args.java,
                jar=args.jar,
                challenge=challenge,
                timeout=args.timeout,
                wall_timeout=args.wall_timeout,
                out_log=log_dir / f"{challenge.stem}.aprove-probe.log",
                dry_run=args.dry_run,
            )
            rows.append(row)
            print(challenge.name, row["status"])
        data["aprove_runs"] = rows
        write_csv(rows, args.out_dir / "m19_aprove_environment_probe_runs.csv")
    else:
        print("AProVE run skipped: no --jar provided")

    (args.out_dir / "m19_aprove_environment_probe.json").write_text(
        json.dumps(data, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    write_markdown(data, args.out_dir / "m19_aprove_environment_probe.md")

    derived = data["command_probe"]["derived"]
    if not derived["yices_e_supported"]:
        print("ENV: yices -e is not supported or yices is missing")
    if not derived["minisat2_on_path"]:
        print("ENV: minisat2 is missing from PATH")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
