from __future__ import annotations

import argparse
import csv
import json
import subprocess
from pathlib import Path


RUN_FIELDS = [
    "databaseId",
    "name",
    "workflowName",
    "displayTitle",
    "event",
    "headBranch",
    "status",
    "conclusion",
    "createdAt",
    "updatedAt",
    "url",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Record GitHub Actions run status for M19 orchestration."
    )
    parser.add_argument("run_ids", nargs="+", help="GitHub Actions run IDs")
    parser.add_argument("--out-dir", type=Path, default=Path("reports/m19_github_runs"))
    parser.add_argument("--prefix", default="m19_github_runs")
    parser.add_argument(
        "--download-artifacts",
        action="store_true",
        help="Also run `gh run download` into an artifacts subdirectory.",
    )
    return parser.parse_args()


def run_gh_json(args: list[str]) -> dict[str, object]:
    process = subprocess.run(
        ["gh", *args],
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return json.loads(process.stdout)


def run_gh(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["gh", *args],
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )


def get_run(run_id: str) -> dict[str, object]:
    return run_gh_json(["run", "view", run_id, "--json", ",".join(RUN_FIELDS)])


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RUN_FIELDS)
        writer.writeheader()
        writer.writerows(rows)


def write_markdown(rows: list[dict[str, object]], path: Path) -> None:
    complete = [row for row in rows if row.get("status") == "completed"]
    successful = [row for row in rows if row.get("conclusion") == "success"]
    lines = [
        "# M19 GitHub Actions run monitor",
        "",
        "## Summary",
        "",
        f"- Runs: {len(rows)}",
        f"- Completed: {len(complete)}",
        f"- Successful: {len(successful)}",
        "",
        "| Run | Workflow | Status | Conclusion | Updated | URL |",
        "| ---: | --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        conclusion = str(row.get("conclusion") or "")
        lines.append(
            "| {run} | {workflow} | {status} | {conclusion} | {updated} | {url} |".format(
                run=row.get("databaseId", ""),
                workflow=row.get("workflowName") or row.get("name", ""),
                status=row.get("status", ""),
                conclusion=conclusion,
                updated=row.get("updatedAt", ""),
                url=row.get("url", ""),
            )
        )

    lines.extend(
        [
            "",
            "## Interpretation Rules",
            "",
            "- A successful workflow is operational evidence only, not a mathematical proof.",
            "- Any `YES` inside logs must be audited as top-level before being treated as evidence.",
            "- Artifacts should be preserved with run IDs and tool versions before publication claims.",
        ]
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def download_artifacts(run_id: str, out_dir: Path) -> tuple[bool, str]:
    target = out_dir / "artifacts" / run_id
    target.mkdir(parents=True, exist_ok=True)
    process = run_gh(["run", "download", run_id, "--dir", str(target)])
    output = "\n".join(part for part in [process.stdout, process.stderr] if part)
    return process.returncode == 0, output.strip()


def main() -> int:
    args = parse_args()
    rows = [get_run(run_id) for run_id in args.run_ids]
    args.out_dir.mkdir(parents=True, exist_ok=True)

    csv_path = args.out_dir / f"{args.prefix}.csv"
    md_path = args.out_dir / f"{args.prefix}.md"
    write_csv(rows, csv_path)
    write_markdown(rows, md_path)

    print(f"csv={csv_path}")
    print(f"md={md_path}")

    if args.download_artifacts:
        for run_id in args.run_ids:
            ok, output = download_artifacts(run_id, args.out_dir)
            status = "downloaded" if ok else "not_downloaded"
            print(f"artifacts {run_id}: {status}")
            if output:
                print(output)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
