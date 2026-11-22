"""Offline contract tests; do not claim host tooling or Freebuff runtime verified."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin/security-toolchain-preflight.py"


class PreflightTests(unittest.TestCase):
    def invoke(self, *args):
        proc = subprocess.run([sys.executable, str(SCRIPT), *args],
                              capture_output=True, text=True, timeout=20)
        self.assertIn(proc.returncode, (0, 2))
        return proc, json.loads(proc.stdout)

    def test_schema_and_evidence_boundary(self):
        proc, report = self.invoke()
        self.assertEqual(proc.returncode, 0)
        self.assertEqual(report["schema_version"], 1)
        self.assertIn("v8_skill", report["checks"])
        self.assertEqual(report["checks"]["freebuff_trace"]["status"], "UNVERIFIED")
        self.assertIn("no skill invocation", report["notice"])

    def test_missing_skill_never_claims_invocation(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, report = self.invoke("--skills-root", tmp)
            self.assertEqual(report["checks"]["v8_skill"]["status"], "MISSING")

    def test_project_dependency_absent(self):
        with tempfile.TemporaryDirectory() as tmp:
            _, report = self.invoke("--project", tmp)
            self.assertEqual(report["checks"]["oz_foundry_upgrades"]["status"],
                             "MISSING_PROJECT_DEPENDENCY")

    def test_strict_failure_and_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / "nested" / "receipt.json"
            proc, report = self.invoke("--require", "freebuff_trace", "--out", str(out))
            self.assertEqual(proc.returncode, 2)
            self.assertFalse(report["required_pass"])
            self.assertEqual(json.loads(out.read_text()), report)

    def test_unknown_require_rejected(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "--require", "invalid_key"],
                              capture_output=True, text=True, timeout=10)
        self.assertEqual(proc.returncode, 2)
        self.assertIn("unknown required", proc.stderr)


if __name__ == "__main__":
    unittest.main()
