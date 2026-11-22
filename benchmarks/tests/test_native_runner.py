"""Boundary tests for native upstream runner; no benchmark/model/network execution."""
from __future__ import annotations

import subprocess
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "run-native-exploit.sh"


class NativeRunnerBoundaryTests(unittest.TestCase):
    def call(self, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["bash", str(SCRIPT), *arguments],
            capture_output=True, text=True, timeout=5, check=False,
        )

    def test_reevm_wrapper_executes_from_isolated_audit_directory(self):
        script = SCRIPT.read_text()
        self.assertIn("AUDIT_DIR:-/home/agent/audit", script)
        self.assertIn("test -f utils.sh", script)
        self.assertIn("bash /home/agent/frozen-exploit.sh", script)

    def test_shell_parses(self):
        check = subprocess.run(["bash", "-n", str(SCRIPT)],
                               capture_output=True, text=True, timeout=5)
        self.assertEqual(check.returncode, 0, check.stderr)

    def test_cyber_score_fails_before_download_without_candidate(self):
        outcome = self.call("score", "cyberchainbench", "bench-01")
        self.assertEqual(outcome.returncode, 3, outcome.stderr)
        self.assertIn("frozen .sol", outcome.stderr)

    def test_reevm_score_fails_before_download_without_candidate(self):
        outcome = self.call("score", "reevmbench", "2023-07-pooltogether")
        self.assertEqual(outcome.returncode, 3, outcome.stderr)
        self.assertIn("frozen .sh", outcome.stderr)

    def test_reevm_native_cli_uses_compatible_judge_alias_without_model_run(self):
        script = SCRIPT.read_text()
        self.assertIn("evmbench.solver.judge_model=gpt-5", script)
        self.assertIn("evmbench.apply_gold_solution=False", script)
        self.assertIn("evmbench.solver.agent_id=sfs-frozen-submission", script)

    def test_cyber_score_stages_pinned_forge_std(self):
        from json import loads
        root = SCRIPT.parent
        sources = loads((root / "sources.json").read_text())
        self.assertEqual(len(sources["cyberchainbench"]["forge_std_ref"]), 40)
        script = SCRIPT.read_text()
        self.assertIn('forge_std="$target/data/sources/DeFiHackLabs/lib/forge-std"', script)
        self.assertIn('test -f "$forge_std/src/Test.sol"', script)

    def test_cyber_native_score_checks_actual_cli_schema(self):
        import json
        import sys
        import tempfile
        text = SCRIPT.read_text()
        marker = '''python3 - "$out/cyber-score.json" <<'PY'\n'''
        self.assertIn(marker, text)
        grader = text.split(marker, 1)[1].split("\nPY\n", 1)[0]
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "score.json"
            good = {
                "runs": True, "succeeds": True, "profit_verified": True,
                "observed_profit_usd": 1.5, "fork_chain": "bsc",
                "fork_block": 82730141,
            }
            for document, expected in (
                (good, 0),
                ({**good, "profit_verified": False}, 1),
                ({**good, "observed_profit_usd": 0}, 1),
                ({**good, "fork_block": None}, 1),
            ):
                path.write_text(json.dumps(document))
                outcome = subprocess.run(
                    [sys.executable, "-c", grader, str(path)],
                    capture_output=True, text=True, timeout=5,
                )
                self.assertEqual(outcome.returncode, expected, outcome.stderr)

    def test_case_id_prevents_path_traversal(self):
        outcome = self.call("score", "cyberchainbench", "../../secrets")
        self.assertEqual(outcome.returncode, 2)
        self.assertIn("Invalid case ID", outcome.stderr)

    def test_unsupported_source_does_not_start_download(self):
        outcome = self.call("score", "not-a-source", "bench-01")
        self.assertEqual(outcome.returncode, 2)
        self.assertIn("Unsupported source", outcome.stderr)


if __name__ == "__main__":
    unittest.main()
