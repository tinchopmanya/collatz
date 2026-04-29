import hashlib
import io
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from m19_certificate_gate import main, run_gate  # noqa: E402


def write(path: Path, text: str) -> Path:
    path.write_text(text, encoding="utf-8")
    return path


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class M19CertificateGateTests(unittest.TestCase):
    def test_accepts_complete_certified_artifact_set(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trs = write(root / "challenge.srs", "(RULES a -> b)\n")
            cpf = write(root / "proof.cpf", "<certificationProblem></certificationProblem>\n")
            prover = write(root / "aprove.out", "YES\n<?xml version='1.0'?>\n")
            ceta = write(root / "ceta.log", "CERTIFIED\n")
            jar = write(root / "aprove.jar", "fake prover bytes\n")
            sums = root / "SHA256SUMS"
            sums.write_text(
                "\n".join(
                    f"{sha256(path)}  {path.name}" for path in (trs, cpf, prover, ceta, jar)
                )
                + "\n",
                encoding="utf-8",
            )

            report = run_gate(
                trs=trs,
                cpf=cpf,
                prover_output=prover,
                ceta_log=ceta,
                prover_binary=jar,
                sha256sums=sums,
            )

            self.assertTrue(report.passed)
            self.assertEqual(
                {"trs", "cpf", "prover_output", "ceta_log", "prover_binary", "sha256sums"},
                {digest.role for digest in report.digests},
            )

    def test_rejects_internal_logs_without_separate_cpf(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trs = write(root / "challenge.srs", "(RULES a -> b)\n")
            internal_log = write(
                root / "internal.log",
                "phase 1 found YES internally\nCeTA subcall says CERTIFIED\n",
            )
            ceta = write(root / "ceta.log", "CERTIFIED\n")
            missing_cpf = root / "proof.cpf"

            report = run_gate(
                trs=trs,
                cpf=missing_cpf,
                prover_output=internal_log,
                ceta_log=ceta,
            )

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("top_level_yes", failed)
            self.assertIn("cpf_present", failed)

    def test_rejects_yes_that_is_not_top_level(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trs = write(root / "challenge.srs", "(RULES a -> b)\n")
            cpf = write(root / "proof.cpf", "<certificationProblem/>\n")
            prover = write(root / "aprove.out", "debug line\nYES\n")
            ceta = write(root / "ceta.log", "CERTIFIED\n")

            report = run_gate(trs=trs, cpf=cpf, prover_output=prover, ceta_log=ceta)

            self.assertFalse(report.passed)
            top_level = [check for check in report.checks if check.name == "top_level_yes"][0]
            self.assertFalse(top_level.ok)

    def test_rejects_manifest_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trs = write(root / "challenge.srs", "(RULES a -> b)\n")
            cpf = write(root / "proof.cpf", "<certificationProblem/>\n")
            prover = write(root / "aprove.out", "YES\n")
            ceta = write(root / "ceta.log", "CERTIFIED\n")
            sums = write(root / "SHA256SUMS", f"{'0' * 64}  {cpf.name}\n")

            report = run_gate(
                trs=trs,
                cpf=cpf,
                prover_output=prover,
                ceta_log=ceta,
                sha256sums=sums,
            )

            self.assertFalse(report.passed)
            failed = {check.name for check in report.checks if not check.ok}
            self.assertIn("cpf_hash_manifest_match", failed)

    def test_cli_returns_nonzero_on_failure(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            trs = write(root / "challenge.srs", "(RULES a -> b)\n")
            cpf = write(root / "proof.cpf", "<certificationProblem/>\n")
            prover = write(root / "aprove.out", "MAYBE\n")
            ceta = write(root / "ceta.log", "CERTIFIED\n")

            with redirect_stdout(io.StringIO()):
                code = main(
                    [
                        "--trs",
                        str(trs),
                        "--cpf",
                        str(cpf),
                        "--prover-output",
                        str(prover),
                        "--ceta-log",
                        str(ceta),
                    ]
                )

            self.assertEqual(1, code)


if __name__ == "__main__":
    unittest.main()
