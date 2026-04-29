from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


HASH_RE = re.compile(r"\b[a-fA-F0-9]{64}\b")
GIT_SHA_RE = re.compile(r"\b[a-fA-F0-9]{7,40}\b")
SEMVER_RE = re.compile(r"\b\d+(?:\.\d+){1,3}\b")
FAILED_BUILD_RE = re.compile(r"\bFailed to build\b", re.IGNORECASE)
BUILD_ERROR_RE = re.compile(r"\b(cabal:\s+Failed|command not found|No such file or directory)\b", re.IGNORECASE)
HELP_MARKER_RE = re.compile(r"\b(matchbox|usage|options?|--help)\b", re.IGNORECASE)

REQUIRED_FILES = {
    "sha256": "m19-matchbox-sha256.txt",
    "ldd": "m19-matchbox-ldd.txt",
    "help": "m19-matchbox-help.log",
    "build_log": "m19-matchbox-build.log",
    "environment": "environment.txt",
    "boolector_rev": "m19-boolector-source-rev.txt",
    "boolector_version": "m19-boolector-version.txt",
}

PIN_KEYS = ("ghc_version", "cabal_version", "index_state", "matchbox_ref")


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class GateReport:
    passed: bool
    artifact_dir: str
    checks: list[Check]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def nonempty_file_check(role: str, path: Path) -> Check:
    if not path.exists():
        return Check(f"{role}_exists", False, f"missing: {path}")
    if not path.is_file():
        return Check(f"{role}_exists", False, f"not a file: {path}")
    if path.stat().st_size <= 0:
        return Check(f"{role}_exists", False, f"empty file: {path}")
    return Check(f"{role}_exists", True, f"{path.name} ({path.stat().st_size} bytes)")


def parse_key_values(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def check_sha256_manifest(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("sha256_has_matchbox_binary", False, "sha256 artifact is unavailable")
    text = read_text(path)
    hashes = HASH_RE.findall(text)
    names_matchbox = re.search(r"\bmatchbox(?:2015)?\b", text, re.IGNORECASE) is not None
    ok = bool(hashes) and names_matchbox
    detail = "contains SHA-256 for matchbox binary" if ok else "missing 64-hex hash or matchbox binary name"
    return Check("sha256_has_matchbox_binary", ok, detail)


def check_ldd_log(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("ldd_ran_on_binary", False, "ldd artifact is unavailable")
    text = read_text(path)
    missing_marker = re.search(r"\b(command not found|No such file|not found)\b", text, re.IGNORECASE)
    has_loader_signal = "=>" in text or "linux-vdso" in text or "not a dynamic executable" in text
    ok = bool(text.strip()) and missing_marker is None and has_loader_signal
    detail = "ldd output is present and has no missing-library marker" if ok else "ldd output does not prove a binary was inspected"
    return Check("ldd_ran_on_binary", ok, detail)


def check_help_log(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("help_ran_on_binary", False, "help artifact is unavailable")
    text = read_text(path)
    failure_marker = re.search(r"\b(command not found|No such file|Permission denied)\b", text, re.IGNORECASE)
    ok = bool(text.strip()) and failure_marker is None and HELP_MARKER_RE.search(text) is not None
    detail = "help output looks like matchbox executable output" if ok else "help output does not prove matchbox execution"
    return Check("help_ran_on_binary", ok, detail)


def check_build_log(path: Path) -> list[Check]:
    if not path.exists() or not path.is_file():
        return [
            Check("build_log_available", False, "build log is unavailable"),
            Check("build_log_no_failed_build", False, "build log is unavailable"),
        ]
    text = read_text(path)
    failed_to_build = FAILED_BUILD_RE.search(text) is not None
    hard_error = BUILD_ERROR_RE.search(text) is not None
    return [
        Check("build_log_available", bool(text.strip()), "build log is non-empty" if text.strip() else "build log is empty"),
        Check(
            "build_log_no_failed_build",
            not failed_to_build and not hard_error,
            "no Failed to build / missing binary marker"
            if not failed_to_build and not hard_error
            else "build log contains Failed to build or missing binary marker",
        ),
    ]


def check_environment(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("environment_has_pinnings", False, "environment artifact is unavailable")
    values = parse_key_values(read_text(path))
    missing = [key for key in PIN_KEYS if not values.get(key)]
    loose = [
        key
        for key in PIN_KEYS
        if values.get(key, "").lower() in {"latest", "master", "main", "head"}
    ]
    index_state = values.get("index_state", "")
    matchbox_ref = values.get("matchbox_ref", "")
    ok = (
        not missing
        and not loose
        and re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$", index_state) is not None
        and GIT_SHA_RE.search(matchbox_ref) is not None
    )
    detail = (
        "environment pins ghc_version, cabal_version, index_state, matchbox_ref"
        if ok
        else f"missing/loose pinnings: missing={missing or 'none'}, loose={loose or 'none'}"
    )
    return Check("environment_has_pinnings", ok, detail)


def check_boolector_rev(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("boolector_source_rev_pinned", False, "Boolector source rev artifact is unavailable")
    text = read_text(path).strip()
    ok = bool(text) and text.lower() not in {"unknown", "latest", "master", "main", "head"} and (
        GIT_SHA_RE.search(text) is not None or SEMVER_RE.search(text) is not None
    )
    detail = "Boolector source rev/version is pinned" if ok else "Boolector source rev is missing or loose"
    return Check("boolector_source_rev_pinned", ok, detail)


def check_boolector_version(path: Path) -> Check:
    if not path.exists() or not path.is_file():
        return Check("boolector_version_recorded", False, "Boolector version artifact is unavailable")
    text = read_text(path).strip()
    ok = bool(text) and text.lower() != "unknown" and SEMVER_RE.search(text) is not None
    detail = "Boolector version is recorded" if ok else "Boolector version is missing or unparsable"
    return Check("boolector_version_recorded", ok, detail)


def run_gate(artifact_dir: Path) -> GateReport:
    checks: list[Check] = []
    checks.append(
        Check(
            "artifact_dir_exists",
            artifact_dir.exists() and artifact_dir.is_dir(),
            f"artifact dir: {artifact_dir}",
        )
    )
    paths = {role: artifact_dir / filename for role, filename in REQUIRED_FILES.items()}
    checks.extend(nonempty_file_check(role, path) for role, path in paths.items())

    checks.append(check_sha256_manifest(paths["sha256"]))
    checks.append(check_ldd_log(paths["ldd"]))
    checks.append(check_help_log(paths["help"]))
    checks.extend(check_build_log(paths["build_log"]))
    checks.append(check_environment(paths["environment"]))
    checks.append(check_boolector_rev(paths["boolector_rev"]))
    checks.append(check_boolector_version(paths["boolector_version"]))

    return GateReport(
        passed=all(check.ok for check in checks),
        artifact_dir=str(artifact_dir),
        checks=checks,
    )


def print_text_report(report: GateReport) -> None:
    print(f"m19_matchbox_artifact_gate={'PASS' if report.passed else 'FAIL'}")
    print(f"artifact_dir={report.artifact_dir}")
    print("checks:")
    for check in report.checks:
        marker = "ok" if check.ok else "fail"
        print(f"- {marker}: {check.name}: {check.detail}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Gate M19 Matchbox build artifacts. This fails successful workflows that "
            "did not actually produce and smoke-test a matchbox binary."
        )
    )
    parser.add_argument("artifact_dir", type=Path, help="Directory containing M19 Matchbox build artifacts.")
    parser.add_argument("--json", type=Path, help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = run_gate(args.artifact_dir)
    print_text_report(report)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")
        print(f"json={args.json}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
