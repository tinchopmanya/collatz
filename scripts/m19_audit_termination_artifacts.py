from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


STATUS_LINES = {"YES", "NO", "MAYBE", "ERROR", "TIMEOUT", "KILLED"}
AUDIT_NAME_HINTS = (
    "m19",
    "termination",
    "aprove",
    "ceta",
    "cpf",
    "ttt2",
    "matchbox",
    "rewriting",
)
SELF_REPORT_PREFIX = "m19_termination_artifact_audit"
TEXT_SUFFIXES = {
    ".cpf",
    ".xml",
    ".log",
    ".out",
    ".txt",
    ".md",
    ".html",
    ".json",
    ".csv",
    ".sha256",
}
SIDECARED_SUFFIXES = {".cpf", ".xml", ".log", ".out", ".txt", ".md", ".html", ".json", ".csv"}
CERTIFIED_RE = re.compile(r"\b(CERTIFIED|ACCEPTED|SUCCESSFULLY\s+CERTIFIED)\b", re.IGNORECASE)
REJECTED_RE = re.compile(r"\b(REJECTED|NOT\s+CERTIFIED|CERTIFICATION\s+FAILED)\b", re.IGNORECASE)
HASH_RE = re.compile(r"\b[a-fA-F0-9]{64}\b")


@dataclass(frozen=True)
class Artifact:
    path: Path
    root: Path
    relpath: str
    size_bytes: int
    sha256: str
    artifact_type: str
    tool: str
    top_level_status: str
    ceta_result: str
    hash_status: str
    signals: str


def should_scan(path: Path, all_files: bool) -> bool:
    if not path.is_file():
        return False
    if path.name.lower().startswith(SELF_REPORT_PREFIX):
        return False
    if path.suffix.lower() not in TEXT_SUFFIXES and path.name != "SHA256SUMS":
        return False
    if all_files:
        return True
    needle = str(path).replace("\\", "/").lower()
    return any(hint in needle for hint in AUDIT_NAME_HINTS)


def iter_candidate_files(roots: Iterable[Path], all_files: bool) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    missing_roots: list[Path] = []
    seen: set[Path] = set()
    for root in roots:
        if not root.exists():
            missing_roots.append(root)
            continue
        candidates = [root] if root.is_file() else root.rglob("*")
        for path in candidates:
            resolved = path.resolve()
            if resolved in seen or not should_scan(resolved, all_files):
                continue
            seen.add(resolved)
            files.append(resolved)
    return sorted(files), missing_roots


def read_text_sample(path: Path, limit: int = 1_000_000) -> str:
    try:
        data = path.read_bytes()[:limit]
    except OSError:
        return ""
    return data.decode("utf-8", errors="replace")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def first_status_line(text: str) -> str:
    for raw_line in text.splitlines():
        line = raw_line.strip().upper()
        if line in STATUS_LINES:
            return line
    return ""


def status_from_csv(text: str) -> str:
    lines = text.splitlines()
    if not lines:
        return ""
    try:
        reader = csv.DictReader(lines)
        statuses = {
            str(row.get("status", "")).strip().upper()
            for row in reader
            if str(row.get("status", "")).strip()
        }
    except csv.Error:
        return ""
    if "YES" in statuses and statuses <= {"YES"}:
        return "YES"
    if "YES" in statuses:
        return "PARTIAL_YES"
    for status in ("NO", "MAYBE", "TIMEOUT", "KILLED", "ERROR"):
        if status in statuses:
            return status
    return ""


def detect_tool(path: Path, text: str) -> str:
    haystack = f"{path.name}\n{text[:20000]}".lower()
    tools = []
    for tool in ("ceta", "aprove", "ttt2", "matchbox", "cpf"):
        if tool in haystack:
            tools.append("CeTA" if tool == "ceta" else tool.upper() if tool in {"ttt2", "cpf"} else tool)
    if "rewriting-collatz" in haystack or "qed" in haystack:
        tools.append("rewriting-collatz")
    return ",".join(dict.fromkeys(tools))


def detect_type(path: Path, text: str) -> str:
    lower_name = path.name.lower()
    lower_text = text.lower()
    if path.name == "SHA256SUMS" or path.suffix.lower() == ".sha256":
        return "hash_manifest"
    if path.suffix.lower() == ".cpf" or "<certificationproblem" in lower_text:
        return "cpf_certificate"
    if "ceta" in lower_name or "certif" in lower_name:
        return "certifier_log"
    if path.suffix.lower() in {".log", ".out", ".txt", ".html"}:
        return "tool_log"
    if path.suffix.lower() in {".csv", ".json", ".md"}:
        return "inventory_or_report"
    return "candidate"


def detect_ceta_result(text: str) -> str:
    if REJECTED_RE.search(text):
        return "REJECTED"
    if CERTIFIED_RE.search(text):
        return "CERTIFIED"
    return ""


def should_scan_ceta_result(path: Path, artifact_type: str) -> bool:
    if artifact_type == "certifier_log":
        return True
    haystack = path.name.lower()
    return "ceta" in haystack or "isafor" in haystack


def collect_signals(path: Path, text: str) -> list[str]:
    lower_text = text.lower()
    signals: list[str] = []
    if "<certificationproblem" in lower_text:
        signals.append("cpf-root")
    if re.search(r"\bQED\b", text):
        signals.append("qed")
    if re.search(r"\bSAT\b", text):
        signals.append("sat")
    if "top-level" in lower_text:
        signals.append("mentions-top-level")
    if HASH_RE.search(text):
        signals.append("contains-sha256")
    if re.search(r"\b(version|commit|release|master_20\d\d_\d\d_\d\d)\b", text, re.IGNORECASE):
        signals.append("versioned")
    if path.suffix.lower() in {".cpf", ".xml"}:
        signals.append("xml-like")
    return signals


def verify_companion_sha256(path: Path, actual_hash: str) -> str:
    if path.suffix.lower() not in SIDECARED_SUFFIXES:
        return "not_applicable"

    sidecar = path.with_name(path.name + ".sha256")
    if not sidecar.exists():
        return "missing_sidecar"

    text = read_text_sample(sidecar, limit=10000)
    match = HASH_RE.search(text)
    if not match:
        return "sidecar_unparseable"
    expected = match.group(0).lower()
    if expected == actual_hash:
        return "ok"
    return "mismatch"


def verify_hash_manifests(files: list[Path]) -> dict[Path, str]:
    statuses: dict[Path, str] = {}
    manifests = [path for path in files if path.name == "SHA256SUMS"]
    manifests.extend(path for path in files if path.suffix.lower() == ".sha256")

    for manifest in manifests:
        text = read_text_sample(manifest, limit=200000)
        bad_lines = 0
        checked = 0
        for raw_line in text.splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            match = HASH_RE.search(line)
            if not match:
                bad_lines += 1
                continue
            expected = match.group(0).lower()
            rest = line[match.end() :].strip().lstrip("*").strip()

            if manifest.suffix.lower() == ".sha256" and not rest:
                target = manifest.with_suffix("")
            else:
                target = (manifest.parent / rest).resolve()

            if not target.exists():
                bad_lines += 1
                continue
            checked += 1
            if sha256_file(target) != expected:
                bad_lines += 1

        if bad_lines:
            statuses[manifest] = f"manifest_failed:{bad_lines}"
        elif checked:
            statuses[manifest] = f"manifest_ok:{checked}"
        else:
            statuses[manifest] = "manifest_unparseable"
    return statuses


def inspect_artifacts(files: list[Path], roots: list[Path]) -> list[Artifact]:
    manifest_statuses = verify_hash_manifests(files)
    artifacts: list[Artifact] = []

    for path in files:
        text = read_text_sample(path)
        file_hash = sha256_file(path)
        root = next((candidate for candidate in roots if path == candidate or candidate in path.parents), path.parent)
        relpath = path.relative_to(root).as_posix() if path != root and root in path.parents else path.name
        artifact_type = detect_type(path, text)
        hash_status = manifest_statuses.get(path)
        if hash_status is None:
            hash_status = verify_companion_sha256(path, file_hash)
        top_level_status = first_status_line(text)
        if not top_level_status and path.suffix.lower() == ".csv":
            top_level_status = status_from_csv(text)
        ceta_result = detect_ceta_result(text) if should_scan_ceta_result(path, artifact_type) else ""
        artifacts.append(
            Artifact(
                path=path,
                root=root,
                relpath=relpath,
                size_bytes=path.stat().st_size,
                sha256=file_hash,
                artifact_type=artifact_type,
                tool=detect_tool(path, text),
                top_level_status=top_level_status,
                ceta_result=ceta_result,
                hash_status=hash_status,
                signals=",".join(collect_signals(path, text)),
            )
        )
    return artifacts


def classify_bundle(artifacts: list[Artifact]) -> str:
    if not artifacts:
        return "no_artifacts"

    has_cpf = any(artifact.artifact_type == "cpf_certificate" for artifact in artifacts)
    has_ceta_certified = any(
        artifact.ceta_result == "CERTIFIED"
        and artifact.artifact_type in {"certifier_log", "tool_log"}
        for artifact in artifacts
    )
    has_top_yes = any(artifact.top_level_status == "YES" for artifact in artifacts)
    has_logs = any(artifact.artifact_type in {"tool_log", "certifier_log", "inventory_or_report"} for artifact in artifacts)
    has_qed_or_sat = any("qed" in artifact.signals or "sat" in artifact.signals for artifact in artifacts)

    if has_cpf and has_ceta_certified:
        return "certified_top_level"
    if has_cpf and has_top_yes:
        return "cpf_present_unchecked_top_level"
    if has_cpf:
        return "cpf_present_unchecked"
    if has_top_yes:
        return "top_level_uncertified"
    if has_logs or has_qed_or_sat:
        return "uncertified_logs_only"
    return "candidate_files_only"


def write_csv_report(artifacts: list[Artifact], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "relpath",
        "artifact_type",
        "tool",
        "top_level_status",
        "ceta_result",
        "hash_status",
        "size_bytes",
        "sha256",
        "signals",
        "absolute_path",
    ]
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for artifact in artifacts:
            writer.writerow(
                {
                    "relpath": artifact.relpath,
                    "artifact_type": artifact.artifact_type,
                    "tool": artifact.tool,
                    "top_level_status": artifact.top_level_status,
                    "ceta_result": artifact.ceta_result,
                    "hash_status": artifact.hash_status,
                    "size_bytes": artifact.size_bytes,
                    "sha256": artifact.sha256,
                    "signals": artifact.signals,
                    "absolute_path": str(artifact.path),
                }
            )


def write_json_report(
    artifacts: list[Artifact],
    classification: str,
    missing_roots: list[Path],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "classification": classification,
        "missing_roots": [str(root) for root in missing_roots],
        "artifact_count": len(artifacts),
        "artifacts": [
            {
                "relpath": artifact.relpath,
                "artifact_type": artifact.artifact_type,
                "tool": artifact.tool,
                "top_level_status": artifact.top_level_status,
                "ceta_result": artifact.ceta_result,
                "hash_status": artifact.hash_status,
                "size_bytes": artifact.size_bytes,
                "sha256": artifact.sha256,
                "signals": artifact.signals.split(",") if artifact.signals else [],
                "absolute_path": str(artifact.path),
            }
            for artifact in artifacts
        ],
    }
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def write_markdown_report(
    artifacts: list[Artifact],
    classification: str,
    missing_roots: list[Path],
    path: Path,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    counts: dict[str, int] = {}
    for artifact in artifacts:
        counts[artifact.artifact_type] = counts.get(artifact.artifact_type, 0) + 1
    hash_failures = [
        artifact
        for artifact in artifacts
        if artifact.hash_status.startswith("mismatch") or artifact.hash_status.startswith("manifest_failed")
    ]
    strong = [
        artifact
        for artifact in artifacts
        if artifact.artifact_type == "cpf_certificate"
        or artifact.ceta_result
        or artifact.top_level_status
        or "qed" in artifact.signals
    ]

    lines = [
        "# M19 termination artifact audit",
        "",
        "## Summary",
        "",
        f"- Bundle classification: `{classification}`",
        f"- Candidate artifacts: {len(artifacts)}",
        f"- Missing roots: {len(missing_roots)}",
        f"- Hash failures: {len(hash_failures)}",
        "",
        "## Artifact Counts",
        "",
        "| Type | Count |",
        "| --- | ---: |",
    ]
    for artifact_type, count in sorted(counts.items()):
        lines.append(f"| `{artifact_type}` | {count} |")

    if missing_roots:
        lines.extend(["", "## Missing Roots", ""])
        for root in missing_roots:
            lines.append(f"- `{root}`")

    lines.extend(
        [
            "",
            "## Highest-Signal Artifacts",
            "",
            "| Artifact | Type | Tool | Status | CeTA | Hash | Signals |",
            "| --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for artifact in strong[:50]:
        lines.append(
            "| "
            f"`{artifact.relpath}` | "
            f"`{artifact.artifact_type}` | "
            f"{artifact.tool or ''} | "
            f"{artifact.top_level_status or ''} | "
            f"{artifact.ceta_result or ''} | "
            f"`{artifact.hash_status}` | "
            f"{artifact.signals or ''} |"
        )

    lines.extend(
        [
            "",
            "## Evidence Ladder",
            "",
            "- `certified_top_level`: CPF certificate plus a successful CeTA/certifier artifact was found.",
            "- `cpf_present_unchecked_top_level`: CPF and a top-level `YES` exist, but no successful certifier run was found.",
            "- `top_level_uncertified`: a tool reports top-level `YES`, but no CPF/CeTA evidence was found.",
            "- `uncertified_logs_only`: logs or reports exist, but there is no top-level certified proof artifact.",
            "- `no_artifacts`: no candidate evidence was found in the scanned roots.",
        ]
    )
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def has_hash_failure(artifacts: list[Artifact]) -> bool:
    return any(
        artifact.hash_status == "mismatch" or artifact.hash_status.startswith("manifest_failed")
        for artifact in artifacts
    )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Audit M19 termination-proof artifacts without trusting raw logs as certification."
    )
    parser.add_argument(
        "--artifact-root",
        type=Path,
        action="append",
        default=[],
        help="Root directory or file to scan. Can be repeated. Default: reports.",
    )
    parser.add_argument("--csv", type=Path, default=Path("reports/m19_termination_artifact_audit.csv"))
    parser.add_argument("--md", type=Path, default=Path("reports/m19_termination_artifact_audit.md"))
    parser.add_argument("--json", type=Path, default=Path("reports/m19_termination_artifact_audit.json"))
    parser.add_argument("--all-files", action="store_true", help="Scan every supported text artifact.")
    parser.add_argument(
        "--require-certified",
        action="store_true",
        help="Exit non-zero unless the bundle is classified as certified_top_level.",
    )
    parser.add_argument(
        "--allow-hash-failures",
        action="store_true",
        help="Do not fail on present but mismatching hash manifests/sidecars.",
    )
    args = parser.parse_args()

    roots = [root.resolve() for root in (args.artifact_root or [Path("reports")])]
    files, missing_roots = iter_candidate_files(roots, all_files=args.all_files)
    artifacts = inspect_artifacts(files, roots)
    classification = classify_bundle(artifacts)

    write_csv_report(artifacts, args.csv)
    write_json_report(artifacts, classification, missing_roots, args.json)
    write_markdown_report(artifacts, classification, missing_roots, args.md)

    print(f"classification={classification}")
    print(f"artifact_count={len(artifacts)}")
    print(f"csv={args.csv}")
    print(f"md={args.md}")
    print(f"json={args.json}")

    if not args.allow_hash_failures and has_hash_failure(artifacts):
        print("hash verification failed", file=sys.stderr)
        return 2
    if args.require_certified and classification != "certified_top_level":
        print("certified top-level proof not found", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
