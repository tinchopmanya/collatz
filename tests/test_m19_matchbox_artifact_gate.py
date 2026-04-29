import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m19_matchbox_artifact_gate import main, run_gate  # noqa: E402


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def write_complete_artifact(root: Path) -> None:
    write(root / "m19-matchbox-sha256.txt", f"{'a' * 64}  matchbox2015\n")
    write(
        root / "m19-matchbox-ldd.txt",
        "linux-vdso.so.1\nlibc.so.6 => /lib/x86_64-linux-gnu/libc.so.6\n",
    )
    write(root / "m19-matchbox-help.log", "matchbox2015 usage: matchbox2015 [options] file.tpdb\n")
    write(root / "m19-matchbox-build.log", "Building matchbox\nCompleted matchbox\n")
    write(
        root / "environment.txt",
        "\n".join(
            [
                "ghc_version=8.10.7",
                "cabal_version=3.10.3.0",
                "index_state=2021-09-01T00:00:00Z",
                "matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4",
                "actual_build=true",
            ]
        )
        + "\n",
    )
    write(root / "m19-boolector-source-rev.txt", "3.2.4\n")
    write(root / "m19-boolector-version.txt", "Boolector 3.2.4\n")


class M19MatchboxArtifactGateTests(unittest.TestCase):
    def test_accepts_complete_binary_artifact_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_complete_artifact(root)

            report = run_gate(root)

            self.assertTrue(report.passed)
            self.assertFalse([check for check in report.checks if not check.ok])

    def test_rejects_successful_workflow_without_binary_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write(root / "m19-matchbox-build.log", "Workflow completed successfully\n")
            write(
                root / "environment.txt",
                "ghc_version=8.10.7\ncabal_version=3.10.3.0\n"
                "index_state=2021-09-01T00:00:00Z\n"
                "matchbox_ref=3b219db26dfb5ff9dd8777dcebabdd4e2a9427a4\n",
            )
            write(root / "m19-boolector-source-rev.txt", "3.2.4\n")
            write(root / "m19-boolector-version.txt", "Boolector 3.2.4\n")

            report = run_gate(root)

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("sha256_exists", failed)
            self.assertIn("ldd_exists", failed)
            self.assertIn("help_exists", failed)
            self.assertIn("sha256_has_matchbox_binary", failed)

    def test_rejects_failed_build_even_with_other_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_complete_artifact(root)
            write(root / "m19-matchbox-build.log", "Failed to build boolector-0.0.0.13\n")

            report = run_gate(root)

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("build_log_no_failed_build", failed)

    def test_rejects_unpinned_environment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_complete_artifact(root)
            write(
                root / "environment.txt",
                "ghc_version=latest\ncabal_version=3.10.3.0\n"
                "index_state=2021-09-01T00:00:00Z\nmatchbox_ref=master\n",
            )

            report = run_gate(root)

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("environment_has_pinnings", failed)

    def test_rejects_missing_boolector_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_complete_artifact(root)
            write(root / "m19-boolector-version.txt", "unknown\n")

            report = run_gate(root)

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("boolector_version_recorded", failed)

    def test_cli_returns_nonzero_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_complete_artifact(root)
            (root / "m19-matchbox-help.log").unlink()

            with redirect_stdout(io.StringIO()):
                code = main([str(root)])

            self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()
