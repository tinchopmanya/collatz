from __future__ import annotations

import argparse
from pathlib import Path


PATCHES = {
    "random.randint(0, 1e9)": "random.randint(0, int(1e9))",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply minimal Python 3 compatibility patches to rewriting-collatz."
    )
    parser.add_argument("--repo", type=Path, required=True, help="Path to rewriting-collatz clone")
    return parser.parse_args()


def patch_file(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    applied: list[str] = []
    for old, new in PATCHES.items():
        if old in text:
            text = text.replace(old, new)
            applied.append(f"{path.name}: {old} -> {new}")
    path.write_text(text, encoding="utf-8")
    return applied


def main() -> int:
    args = parse_args()
    sat_path = args.repo / "prover" / "sat.py"
    if not sat_path.exists():
        raise FileNotFoundError(f"missing expected file: {sat_path}")

    applied = patch_file(sat_path)
    if applied:
        print("Applied compatibility patches:")
        for item in applied:
            print(f"- {item}")
    else:
        print("No compatibility patches were needed.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
