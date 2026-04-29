from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable


STATUS_LINES = {"YES", "NO", "MAYBE", "TIMEOUT", "ERROR", "KILLED"}
HASH_RE = re.compile(r"\b[a-fA-F0-9]{64}\b")
CPF_ROOT_RE = re.compile(r"<(?:\w+:)?certificationProblem\b", re.IGNORECASE)
CERTIFIED_RE = re.compile(r"^\s*CERTIFIED\b", re.IGNORECASE | re.MULTILINE)
REJECTED_RE = re.compile(
    r"\b(REJECTED|NOT\s+CERTIFIED|CERTIFICATION\s+FAILED)\b", re.IGNORECASE
)


@dataclass(frozen=True)
class Check:
    name: str
    ok: bool
    detail: str


@dataclass(frozen=True)
class FileDigest:
    role: str
    path: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class GateReport:
    passed: bool
    checks: list[Check]
    digests: list[FileDigest]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_nonempty_line(text: str) -> str:
    for line in text.splitlines():
        stripped = line.strip()
        if stripped:
            return stripped
    return ""


def first_status_line(text: str) -> str:
    for line in text.splitlines():
        status = line.strip().upper()
        if status in STATUS_LINES:
            return status
    return ""


def extract_hash_manifest(path: Path) -> dict[str, str]:
    entries: dict[str, str] = {}
    for raw_line in read_text(path).splitlines():
        match = HASH_RE.search(raw_line)
        if not match:
            continue
        digest = match.group(0).lower()
        rest = raw_line[match.end() :].strip()
        if rest.startswith("*"):
            rest = rest[1:].strip()
        if not rest:
            continue
        entries[Path(rest).name] = digest
        entries[rest.replace("\\", "/")] = digest
    return entries


def manifest_digest_for(path: Path, manifest: dict[str, str]) -> str | None:
    keys = [
        str(path).replace("\\", "/"),
        path.name,
        str(path.resolve()).replace("\\", "/"),
    ]
    for key in keys:
        if key in manifest:
            return manifest[key]
    return None


def file_check(role: str, path: Path) -> Check:
    if not path.exists():
        return Check(f"{role}_exists", False, f"missing: {path}")
    if not path.is_file():
        return Check(f"{role}_exists", False, f"not a file: {path}")
    if path.stat().st_size <= 0:
        return Check(f"{role}_exists", False, f"empty file: {path}")
    return Check(f"{role}_exists", True, f"{path} ({path.stat().st_size} bytes)")


def collect_digests(files: Iterable[tuple[str, Path]]) -> list[FileDigest]:
    digests: list[FileDigest] = []
    for role, path in files:
        if path.exists() and path.is_file():
            digests.append(
                FileDigest(
                    role=role,
                    path=str(path),
                    sha256=sha256_file(path),
                    size_bytes=path.stat().st_size,
                )
            )
    return digests


def run_gate(
    *,
    trs: Path,
    cpf: Path,
    prover_output: Path,
    ceta_log: Path,
    prover_binary: Path | None = None,
    sha256sums: Path | None = None,
) -> GateReport:
    checks: list[Check] = []
    required_files = [
        ("trs", trs),
        ("cpf", cpf),
        ("prover_output", prover_output),
        ("ceta_log", ceta_log),
    ]
    if prover_binary is not None:
        required_files.append(("prover_binary", prover_binary))
    if sha256sums is not None:
        required_files.append(("sha256sums", sha256sums))

    checks.extend(file_check(role, path) for role, path in required_files)
    existing = {
        role: path for role, path in required_files if path.exists() and path.is_file()
    }

    if "prover_output" in existing:
        prover_text = read_text(prover_output)
        top_line = first_nonempty_line(prover_text).upper()
        status = first_status_line(prover_text)
        checks.append(
            Check(
                "top_level_yes",
                top_line == "YES",
                f"first non-empty line is {top_line or '<none>'!r}; first status is {status or '<none>'!r}",
            )
        )
    else:
        checks.append(Check("top_level_yes", False, "prover output is unavailable"))

    if "cpf" in existing:
        cpf_text = read_text(cpf)
        has_cpf_root = CPF_ROOT_RE.search(cpf_text) is not None
        checks.append(
            Check(
                "cpf_present",
                has_cpf_root,
                "separate CPF file contains certificationProblem root"
                if has_cpf_root
                else "separate CPF file lacks certificationProblem root",
            )
        )
        checks.append(
            Check(
                "cpf_is_separate_artifact",
                cpf.resolve() != prover_output.resolve() if prover_output.exists() else True,
                "CPF is stored separately from prover output",
            )
        )
    else:
        checks.append(Check("cpf_present", False, "CPF file is unavailable"))
        checks.append(Check("cpf_is_separate_artifact", False, "CPF file is unavailable"))

    if "ceta_log" in existing:
        ceta_text = read_text(ceta_log)
        rejected = REJECTED_RE.search(ceta_text) is not None
        certified = CERTIFIED_RE.search(ceta_text) is not None
        checks.append(
            Check(
                "ceta_certified",
                certified and not rejected,
                "CeTA log has CERTIFIED and no rejection marker"
                if certified and not rejected
                else "CeTA log does not contain an acceptable CERTIFIED result",
            )
        )
    else:
        checks.append(Check("ceta_certified", False, "CeTA log is unavailable"))

    digest_inputs = required_files
    digests = collect_digests(digest_inputs)
    digest_roles = {digest.role for digest in digests}
    expected_digest_roles = {"trs", "cpf", "prover_output", "ceta_log"}
    if prover_binary is not None:
        expected_digest_roles.add("prover_binary")
    checks.append(
        Check(
            "hashes_available",
            expected_digest_roles <= digest_roles,
            "SHA-256 computed for " + ", ".join(sorted(digest_roles)),
        )
    )

    if sha256sums is not None and sha256sums.exists() and sha256sums.is_file():
        manifest = extract_hash_manifest(sha256sums)
        for role, path in required_files:
            if role == "sha256sums":
                continue
            if not path.exists() or not path.is_file():
                continue
            expected = manifest_digest_for(path, manifest)
            actual = sha256_file(path)
            checks.append(
                Check(
                    f"{role}_hash_manifest_match",
                    expected == actual,
                    "manifest hash matches"
                    if expected == actual
                    else f"manifest has {expected or '<missing>'}, actual is {actual}",
                )
            )

    passed = all(check.ok for check in checks)
    return GateReport(passed=passed, checks=checks, digests=digests)


def print_text_report(report: GateReport) -> None:
    print(f"m19_certificate_gate={'PASS' if report.passed else 'FAIL'}")
    print("checks:")
    for check in report.checks:
        marker = "ok" if check.ok else "fail"
        print(f"- {marker}: {check.name}: {check.detail}")
    print("sha256:")
    for digest in report.digests:
        print(f"- {digest.role}: {digest.sha256}  {digest.path}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Gate M19 CPF/CeTA certification artifacts. This validates a top-level "
            "YES, a separate CPF, CeTA CERTIFIED, and SHA-256 identities."
        )
    )
    parser.add_argument("--trs", type=Path, required=True, help="Input TRS/SRS artifact.")
    parser.add_argument("--cpf", type=Path, required=True, help="Separate CPF XML artifact.")
    parser.add_argument(
        "--prover-output",
        type=Path,
        required=True,
        help="Top-level prover stdout/log whose first non-empty line must be YES.",
    )
    parser.add_argument(
        "--ceta-log", type=Path, required=True, help="CeTA verifier log with CERTIFIED."
    )
    parser.add_argument(
        "--prover-binary",
        type=Path,
        help="Optional pinned prover binary/JAR to include in hash identity.",
    )
    parser.add_argument(
        "--sha256sums",
        type=Path,
        help="Optional SHA256SUMS manifest; when present, listed hashes must match.",
    )
    parser.add_argument("--json", type=Path, help="Optional JSON report path.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    report = run_gate(
        trs=args.trs,
        cpf=args.cpf,
        prover_output=args.prover_output,
        ceta_log=args.ceta_log,
        prover_binary=args.prover_binary,
        sha256sums=args.sha256sums,
    )
    print_text_report(report)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")
        print(f"json={args.json}")
    return 0 if report.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
