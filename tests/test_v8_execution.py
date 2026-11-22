"""V8-Abnahmetests: echte Ausfuehrung, Zustandsmaschine, Evidenz-Inhalt, Recovery.

Die 16 Prototyp-Tests (test_orchestrator.py, test_probe.py) bleiben unveraendert.
Diese Datei deckt die neuen V8-Funktionen ab: Adapter-Ausfuehrung, Timeout,
Verfuegbarkeit, Recovery, Inhaltsprüfung der Evidenz und Domänenrouting.
"""
import importlib.util
import json
import os
from pathlib import Path
import stat
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "skill-orchestrator.py"
spec = importlib.util.spec_from_file_location("sfs_orchestrator_v8", SCRIPT)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)


def _write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _search_path(directory: Path) -> str:
    """Fake-Binary zuerst, Systempfade erhalten (Skripte brauchen /bin/sh-Helfer)."""
    return f"{directory}{os.pathsep}{os.environ.get('PATH', '/usr/bin:/bin')}"


def _fake_binary(directory: Path, name: str, body: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(body, encoding="utf-8")
    path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
    return path


def _sha(path: Path) -> str:
    import hashlib
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


FORGE_OK = {
    "test/Solvency.t.sol:SolvencyTest": {
        "test_results": {
            "test_reentrancy_drains_vault()": {"status": "Success"},
            "test_invariant_holds_initially()": {"status": "Success"},
        }
    }
}

SOLIDITY_TEST_SOURCE = """
pragma solidity ^0.8.0;
contract SolvencyTest {
    Vault vault;
    function test_reentrancy_drains_vault() public payable {
        vault.deposit{value: 2 ether}();
        require(address(vault).balance <= 1 ether, "Drain");
    }
    function test_invariant_holds_initially() public payable {
        vault.deposit{value: 1 ether}();
        require(address(vault).balance == 1 ether, "holds");
    }
}
"""

SLITHER_OK = json.dumps({
    "success": True, "error": None,
    "results": {"detectors": [
        {"check": "reentrancy-eth", "impact": "High", "confidence": "Medium",
         "elements": [{"source_mapping": {"filename_relative": "Vulnerable.sol"}}]},
        {"check": "tx-origin", "impact": "Medium", "confidence": "Medium",
         "elements": [{"source_mapping": {"filename_relative": "Vulnerable.sol"}}]},
    ]},
})


class AdapterSafetyTests(unittest.TestCase):
    def test_argv_allows_directory_prefix_composition(self):
        self.assertEqual(["--json", "/tmp/out/slither.json"],
                         router.render_argv(["--json", "{outdir}/slither.json"],
                                            {"outdir": "/tmp/out"}))

    def test_argv_rejects_option_like_value(self):
        with self.assertRaisesRegex(ValueError, "option-like"):
            router.render_argv(["{target}"], {"target": "--json"})

    def test_argv_rejects_path_traversal(self):
        with self.assertRaisesRegex(ValueError, "traversal"):
            router.render_argv(["{outdir}/x.json"], {"outdir": "../../etc"})

    def test_argv_rejects_missing_placeholder(self):
        with self.assertRaisesRegex(ValueError, "missing placeholder"):
            router.render_argv(["{target}"], {})

    def test_argv_rejects_control_characters(self):
        with self.assertRaisesRegex(ValueError, "control character"):
            router.render_argv(["{target}"], {"target": "a\nb"})

    def test_argv_rejects_unknown_placeholder(self):
        with self.assertRaisesRegex(ValueError, "missing placeholder"):
            router.render_argv(["{nope}/x"], {"target": "/tmp/a"})

    def test_argv_uses_no_shell_and_keeps_argument_boundaries(self):
        argv = router.render_argv(["describe", "{target}"], {"target": "/tmp/a b; rm -rf /"})
        self.assertEqual(["describe", "/tmp/a b; rm -rf /"], argv)
        self.assertNotIn("shell", json.dumps(router.ADAPTERS["surya-describe"]))


class AdapterExecutionTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.target = _write(self.root / "Target.sol", "pragma solidity ^0.8.0; contract Target {}")
        self.bindir = self.root / "bin"

    def tearDown(self):
        self.tmp.cleanup()

    def test_adapter_records_receipt_version_and_log_hash(self):
        _fake_binary(self.bindir, "surya", '#!/bin/sh\nif [ "$1" = "--version" ]; then echo "surya 9.9"; exit 0; fi\necho " + Target"\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("surya-describe", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("COMPLETED", row["status"])
        self.assertEqual(0, row["exit_code"])
        self.assertIn("surya 9.9", row["version"])
        self.assertTrue(Path(row["log"]).is_file())
        self.assertEqual(_sha(Path(row["log"])), row["log_sha256"])
        self.assertEqual("map", row["family"])

    def test_timeout_kills_process_group_and_is_not_success(self):
        _fake_binary(self.bindir, "surya", '#!/bin/sh\nsleep 30\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("surya-describe", {"target": str(self.target)},
                                     self.root / "out", timeout=1)
        self.assertEqual("TIMEOUT", row["status"])
        self.assertIsNone(row["exit_code"])
        self.assertLess(row["duration_s"], 15)

    def test_unavailable_binary_is_not_executed(self):
        with patch.object(router.shutil, "which", return_value=None):
            row = router.run_adapter("slither-json", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("UNAVAILABLE", row["status"])
        self.assertNotIn("argv", row)

    def test_nonzero_exit_is_failure_not_success(self):
        _fake_binary(self.bindir, "surya", '#!/bin/sh\nexit 3\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("surya-describe", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("FAILED", row["status"])
        self.assertEqual(3, row["exit_code"])

    def test_slither_exit_255_with_valid_json_is_completed(self):
        _fake_binary(self.bindir, "slither", '#!/bin/sh\nif [ "$1" = "--version" ]; then echo 0.11.6; exit 0; fi\n'
                     'for a in "$@"; do case "$a" in *.json) echo \'{"success": true, "results": {"detectors": []}}\' > "$a";; esac; done\n'
                     'echo "2 result(s) found"\nexit 255\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("slither-json", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("COMPLETED", row["status"])
        self.assertEqual(255, row["exit_code"])

    def test_slither_completed_without_json_contract_fails(self):
        _fake_binary(self.bindir, "slither", '#!/bin/sh\nif [ "$1" = "--version" ]; then echo 0.11.6; exit 0; fi\nexit 0\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("slither-json", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("FAILED", row["status"])
        self.assertIn("JSON-Vertrag", row["detail"])

    def test_echidna_exit_1_counts_as_finding_not_failure(self):
        _fake_binary(self.bindir, "echidna", '#!/bin/sh\nif [ "$1" = "--version" ]; then echo "Echidna 2.4.0"; exit 0; fi\n'
                     'echo \'{"success": false, "tests": [{"name": "assert_solvent", "status": "falsified"}]}\'\nexit 1\n')
        with patch.dict(os.environ, {"PATH": _search_path(self.bindir)}, clear=False):
            row = router.run_adapter("echidna-assertion", {"target": str(self.target),
                                                         "contract": "Target", "test_limit": "100"},
                                     self.root / "out")
        self.assertEqual("COMPLETED", row["status"])
        facts = router.observe("echidna-assertion", row, self.root / "out")
        self.assertEqual(1, facts["falsified"])

    def test_missing_project_blocks_instead_of_running_in_cwd(self):
        row = router.run_adapter("forge-test", {"project": None}, self.root / "out")
        self.assertEqual("BLOCKED", row["status"])
        self.assertIn("project", row["detail"])

    def test_resource_reserve_prevents_spawn(self):
        with patch.object(router, "reserve_ok", return_value=(False, "synthetic low memory")):
            row = router.run_adapter("slither-json", {"target": str(self.target)}, self.root / "out")
        self.assertEqual("BLOCKED", row["status"])
        self.assertIn("Ressourcenreserve", row["detail"])


class EvidenceContentTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.base = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def _report(self, **families):
        rows = []
        for family, name in families.items():
            p = self.base / name
            rows.append({"path": name, "family": family, "sha256": _sha(p)})
        return {"evidence": rows}

    def test_forged_static_claim_without_detector_is_not_verified(self):
        _write(self.base / "slither.json", SLITHER_OK)
        _write(self.base / "forge.json", json.dumps(FORGE_OK))
        _write(self.base / "test" / "Solvency.t.sol", SOLIDITY_TEST_SOURCE)
        report = self._report(static="slither.json", counterexample="forge.json")
        report["claims"] = [{"family": "static", "detector": "integer-overflow"}]
        result = router.verify_evidence(report, self.base)
        self.assertFalse(result["claims"][0]["supported"])
        self.assertNotEqual("VERIFIED_LOCAL", result["verdict"])

    def test_declared_detector_present_is_supported(self):
        _write(self.base / "slither.json", SLITHER_OK)
        report = self._report(static="slither.json")
        report["claims"] = [{"family": "static", "detector": "reentrancy-eth"}]
        self.assertTrue(router.verify_evidence(report, self.base)["claims"][0]["supported"])

    def test_failed_slither_run_is_not_evidence(self):
        _write(self.base / "slither.json", json.dumps(
            {"success": False, "error": "compilation failed", "results": {"detectors": []}}))
        result = router.verify_evidence(self._report(static="slither.json"), self.base)
        self.assertNotEqual("VERIFIED_LOCAL", result["verdict"])
        self.assertFalse(result["content_verified_families"])

    def test_counterexample_without_assertion_in_source_is_not_verified(self):
        _write(self.base / "forge.json", json.dumps(FORGE_OK))
        _write(self.base / "test" / "Solvency.t.sol",
               "contract SolvencyTest { function test_reentrancy_drains_vault() public {} }")
        result = router.verify_evidence(self._report(counterexample="forge.json"), self.base)
        self.assertNotEqual("VERIFIED_LOCAL", result["verdict"])
        self.assertFalse(result["content"]["counterexample"]["counterexamples"])

    def test_negative_control_is_required_for_full_verification(self):
        _write(self.base / "slither.json", SLITHER_OK)
        _write(self.base / "forge.json", json.dumps(FORGE_OK))
        _write(self.base / "test" / "Solvency.t.sol", SOLIDITY_TEST_SOURCE)
        result = router.verify_evidence(
            self._report(static="slither.json", counterexample="forge.json"), self.base)
        self.assertEqual("PARTIAL", result["verdict"])

    def test_full_chain_verifies_locally(self):
        _write(self.base / "slither.json", SLITHER_OK)
        _write(self.base / "forge.json", json.dumps(FORGE_OK))
        _write(self.base / "control.json", json.dumps({
            "test/Solvency.t.sol:SolvencyTest": {
                "test_results": {"test_invariant_holds_initially()": {"status": "Success"}}}}))
        _write(self.base / "test" / "Solvency.t.sol", SOLIDITY_TEST_SOURCE)
        result = router.verify_evidence(self._report(
            static="slither.json", counterexample="forge.json", negative_control="control.json"), self.base)
        self.assertEqual("VERIFIED_LOCAL", result["verdict"])
        self.assertIn("static:slither", result["independent_methods"])
        self.assertIn("dynamic:forge", result["independent_methods"])
        self.assertFalse(result["can_claim_verified_exploit"])

    def test_failing_counterexample_test_is_a_contradiction(self):
        _write(self.base / "forge.json", json.dumps({
            "test/Solvency.t.sol:SolvencyTest": {"test_results": {
                "test_reentrancy_drains_vault()": {"status": "Failure"}}}}))
        _write(self.base / "test" / "Solvency.t.sol", SOLIDITY_TEST_SOURCE)
        result = router.verify_evidence(self._report(counterexample="forge.json"), self.base)
        self.assertEqual("INVALID", result["verdict"])

    def test_state_delta_is_checked_arithmetically(self):
        _write(self.base / "delta.json", json.dumps(
            {"metric": "vault_balance_wei", "before": 3000000000000000000,
             "after": 0, "relation": "lt"}))
        ok = router.verify_evidence({"evidence": [
            {"path": "delta.json", "family": "state_delta", "sha256": _sha(self.base / "delta.json")}]},
            self.base)
        self.assertTrue(ok["content"]["state_delta"]["valid"])
        _write(self.base / "bad.json", json.dumps(
            {"metric": "x", "before": 1, "after": 2, "relation": "lt"}))
        bad = router.verify_evidence({"evidence": [
            {"path": "bad.json", "family": "state_delta", "sha256": _sha(self.base / "bad.json")}]},
            self.base)
        self.assertFalse(bad["content"]["state_delta"]["valid"])

    def test_structural_gate_alone_never_claims_verification(self):
        _write(self.base / "notes.json", "{}")
        result = router.assess(self._report(source_review="notes.json"), self.base)
        self.assertFalse(result["can_claim_verified_exploit"])


class PlanAndStateTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        (_write(self.root / "manifest.json", json.dumps({"skills": [
            {"slug": "safe-harbor", "layer": "L0", "kind": "knowledge", "status": "wissen",
             "role": "scope", "triggers": ["scope"], "pairs_with": []},
            {"slug": "surya", "layer": "L1", "kind": "tool", "status": "binary",
             "role": "solidity map", "triggers": ["solidity"], "pairs_with": ["slither"]},
            {"slug": "slither", "layer": "L2", "kind": "tool", "status": "binary",
             "role": "solidity static analyzer reentrancy", "triggers": ["solidity"], "pairs_with": ["surya"]},
            {"slug": "echidna", "layer": "L3", "kind": "tool", "status": "binary",
             "role": "solidity property fuzzer invariant", "triggers": ["solidity"],
             "pairs_with": ["slither"]},
        ]})))
        for slug in ("safe-harbor", "surya", "slither", "echidna"):
            _write(self.root / "knowledge" / slug / "SKILL.md", f"# {slug}\n")
        self.target = _write(self.root / "Vault.sol", "pragma solidity ^0.8.0; contract Vault {}")

    def tearDown(self):
        self.tmp.cleanup()

    def test_state_machine_contains_required_states(self):
        for state in ("DISCOVERED", "SELECTED", "READY", "INVOKED", "COMPLETED",
                      "FAILED", "UNAVAILABLE", "VERIFIED", "BLOCKED"):
            self.assertIn(state, router.STATES)

    def test_plan_marks_non_adapter_steps_knowledge_only(self):
        plan = router.compose("Audit solidity reentrancy in withdraw", self.root,
                              None, "source", 5, {"target": str(self.target)})
        steps = {s["id"]: s for s in plan["steps"]}
        self.assertEqual("KNOWLEDGE_ONLY", steps["SCOPE"]["status"])
        self.assertEqual("KNOWLEDGE_ONLY", steps["HYPOTHESES"]["status"])
        self.assertEqual("DISCOVERED", steps["STATIC"]["status"])

    def test_plan_dependencies_are_closed_and_acyclic(self):
        plan = router.compose("Audit solidity reentrancy in withdraw", self.root,
                              None, "source", 5, {"target": str(self.target)})
        seen = set()
        for step in plan["steps"]:
            self.assertTrue(set(step["depends_on"]) <= seen)
            seen.add(step["id"])

    def test_run_requires_explicit_execution_gate(self):
        plan = router.compose("Audit solidity reentrancy in withdraw", self.root,
                              None, "source", 5, {"target": str(self.target)})
        with self.assertRaisesRegex(ValueError, "allow-exec"):
            router.run_plan(plan, self.root / "out")

    def test_unavailable_static_adapter_uses_documented_fallback(self):
        plan = router.compose("Audit solidity reentrancy in withdraw", self.root,
                              None, "source", 5, {"target": str(self.target)})
        real_which = router.shutil.which

        def which(name, *a, **k):
            return None if name in ("slither", "myth") else real_which(name, *a, **k)
        with patch.object(router.shutil, "which", side_effect=which), \
             patch.object(router, "run_adapter", return_value={"status": "UNAVAILABLE", "adapter": "x",
                                                               "family": "static"}):
            summary = router.run_plan(plan, self.root / "out", allow_exec=True)
        decisions = " ".join(json.dumps(d) for d in summary["decisions"])
        self.assertIn("UNAVAILABLE", decisions)
        self.assertTrue(any(s["id"] == "STATIC_FALLBACK" for s in summary["extra_steps"]) or
                        summary["states"].get("STATIC") == "UNAVAILABLE")

    def test_solana_task_routes_knowledge_not_evm_tools(self):
        answer = router.route("Review a Solana Anchor program for missing signer checks", self.root)
        self.assertEqual("NO_MATCH", answer["status"])
        self.assertEqual([], [c for c in answer["candidates"] if c["kind"] == "tool"])
        self.assertIn("status_detail", answer)

    def test_non_security_task_stays_negative(self):
        self.assertEqual("NO_MATCH", router.route("Write marketing copy for a bakery", self.root)["status"])


class RealCorpusTests(unittest.TestCase):
    """Echter Lauf gegen den autorisierten lokalen Korpus (SFS_V8_REAL=1)."""

    @unittest.skipUnless(os.environ.get("SFS_V8_REAL") == "1", "set SFS_V8_REAL=1 for real tool run")
    def test_real_run_reproduces_known_vulnerability(self):
        root = Path(__file__).resolve().parent.parent
        corpus = root / "corpora" / "verify"
        self.assertTrue((corpus / "Vulnerable.sol").is_file())
        out = Path(tempfile.mkdtemp()) / "run"
        ctx = {"target": corpus / "Vulnerable.sol", "project": corpus, "contract": "Vault"}
        plan = router.compose("Audit Solidity vault withdraw reentrancy and unchecked accounting",
                              root, None, "auto", 7, ctx)
        summary = router.run_plan(plan, out, allow_exec=True, allow_network=False)
        self.assertEqual("VERIFIED", summary["status"])
        self.assertIn("reentrancy-eth", summary["facts"]["STATIC"]["checks"])
        self.assertTrue(summary["verification"]["content"]["counterexample"]["valid"])
        self.assertTrue(summary["verification"]["content"]["negative_control"]["valid"])
        self.assertGreaterEqual(len(summary["verification"]["independent_methods"]), 2)


if __name__ == "__main__":
    unittest.main()
