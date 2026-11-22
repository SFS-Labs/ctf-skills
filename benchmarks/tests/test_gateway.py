import json
import os
import tempfile
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gateway

CYBER = {
    "id": "bench-01",
    "name": "Known incident",
    "chain": "bsc",
    "block_number": 12653565,
    "vulnerable_address": "0xf642f2a626a8b732619606c493abfc2433dd2d35",
    "function": "syntheticFunction",
    "type": "synthetic-vuln",
    "file": "MetaSwapUtils.sol",
    "fix_description": "SECRET FIX",
    "attack_txs": ["0xattack"],
    "case_link": "https://incident",
}
CONFIG = """id: 2023-07-pooltogether
framework: foundry-json
run_cmd_dir: vault
base_commit: 4240445ed3b5145be1032cf1becc9c6866046bf7
vulnerabilities:
  - id: "H-02"
    title: "SECRET vulnerability"
"""
DOCKERFILE = "RUN git clone --recurse https://github.com/evmbench-org/2023-07-pooltogether.git $AUDIT_DIR"


def mocked(source, path):
    if source == "cyberchainbench":
        return json.dumps(CYBER)
    return DOCKERFILE if path.endswith("Dockerfile") else CONFIG


class GatewayTest(unittest.TestCase):
    def test_cyber_detect_masks_known_answer(self):
        with patch.object(gateway, "fetch_text", side_effect=mocked):
            brief = gateway.prepare("cyberchainbench", "bench-01", "detect")
        output = json.dumps(brief)
        for secret in (
            "syntheticFunction", "synthetic-vuln", "SECRET FIX",
            "0xattack", "Known incident", "bench-01", "12653565",
        ):
            self.assertNotIn(secret, output)
        self.assertEqual(brief["target"]["chain"], "bsc")

    def test_cyber_reproduce_adds_block_not_solution(self):
        with patch.object(gateway, "fetch_text", side_effect=mocked):
            brief = gateway.prepare("cyberchainbench", "bench-01", "reproduce")
        self.assertEqual(brief["target"]["historical_block"], 12653565)
        self.assertNotIn("syntheticFunction", json.dumps(brief))

    def test_reevm_masks_finding(self):
        with patch.object(gateway, "fetch_text", side_effect=mocked):
            brief = gateway.prepare("reevmbench", "2023-07-pooltogether", "detect")
        self.assertNotIn("H-02", json.dumps(brief))
        self.assertNotIn("SECRET", json.dumps(brief))
        self.assertEqual(
            brief["target"]["source_commit"],
            "4240445ed3b5145be1032cf1becc9c6866046bf7",
        )

    def test_cyber_grade(self):
        with patch.object(gateway, "fetch_text", side_effect=mocked):
            good = gateway.grade("cyberchainbench", "bench-01", {
                "findings": [{"type": "SYNTHETIC-VULN", "function": "syntheticFunction"}]
            })
            bad = gateway.grade("cyberchainbench", "bench-01", {
                "findings": [{"type": "reentrancy", "function": "withdraw"}]
            })
        self.assertEqual(good["status"], "LABEL_MATCH_UNVERIFIED")
        self.assertFalse(bad["label_match"])
        self.assertEqual(good["independent_reproduction"], "NOT_VERIFIED")

    def test_reevm_grade(self):
        with patch.object(gateway, "fetch_text", side_effect=mocked):
            result = gateway.grade("reevmbench", "2023-07-pooltogether", {
                "findings": [{"finding_id": "H-02"}]
            })
        self.assertEqual(result["status"], "MANUAL_REVIEW_REQUIRED")
        self.assertTrue(result["finding_id_match"])
        self.assertEqual(result["reference_findings"][0]["id"], "H-02")
        self.assertEqual(len(result["frozen_submission_sha256"]), 64)

    def test_reevm_target_missing_base_commit_uses_pinned_head(self):
        no_commit = """id: 2024-06-thorchain
vulnerabilities:
  - id: "H-01"
    title: "SECRET vulnerability"
"""
        with patch.object(gateway, "fetch_text", side_effect=lambda s, p:
                          DOCKERFILE if p.endswith("Dockerfile") else no_commit):
            with patch.object(gateway, "snapshot_head", return_value="a" * 40):
                doc = gateway.load_reference("reevmbench", "2024-06-thorchain")
                brief = gateway.prepare("reevmbench", "2024-06-thorchain", "detect")
        self.assertEqual(doc["base_commit"], "a" * 40)
        self.assertEqual(brief["target"]["revision_method"], "upstream_head_at_preparation")
        self.assertNotIn("SECRET", json.dumps(brief))

    def test_cyber_catalog_ids_only(self):
        rows = [
            {"name": "bench-02.json"},
            {"name": "bench-01.json"},
            {"name": "README.md"},
        ]
        with patch.object(gateway, "fetch_github_json", return_value=rows):
            cat = gateway.catalog("cyberchainbench")
        self.assertEqual(cat["case_ids"], ["bench-01", "bench-02"])
        self.assertEqual(cat["case_count"], 2)

    def test_reevm_catalog_from_split(self):
        with patch.object(gateway, "fetch_text",
                          return_value="2023-07-pooltogether\n2024-06-thorchain\n"):
            cat = gateway.catalog("reevmbench")
        self.assertEqual(cat["case_count"], 2)
        self.assertIn("2024-06-thorchain", cat["case_ids"])

    def test_inline_submission_works_without_commit(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "grade.json"
            report = {"findings": [{"type": "synthetic-vuln",
                                    "function": "syntheticFunction"}]}
            with patch.object(gateway, "fetch_text", side_effect=mocked):
                with patch.dict(os.environ, {"SUBMISSION_JSON": json.dumps(report)}):
                    exit_code = gateway.main([
                        "grade", "--source", "cyberchainbench",
                        "--case-id", "bench-01", "--submission-json-env",
                        "--output", str(target)])
            self.assertEqual(exit_code, 0)
            out = json.loads(target.read_text())
            self.assertTrue(out["label_match"])

    def test_smoke_dispatch_prepares_both_sources(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / "smoke.json"
            with patch.object(gateway, "prepare", side_effect=lambda source, case, phase:
                              {"source": source, "case": case, "phase": phase}):
                exit_code = gateway.main([
                    "smoke", "--source", "cyberchainbench", "--output", str(target)])
            self.assertEqual(exit_code, 0)
            result = json.loads(target.read_text())
            self.assertEqual(len(result["cases"]), 2)
            self.assertEqual({x["source"] for x in result["cases"]},
                             {"reevmbench", "cyberchainbench"})


    def test_path_rejection(self):
        for bad in ("../../secret", "../bench-01", "foo/bar", "", ".hidden", "a;b"):
            with self.assertRaises(gateway.GatewayError):
                gateway.validate_id(bad)
        with self.assertRaises(gateway.GatewayError):
            gateway.confined_submission_path("../../README.md")


if __name__ == "__main__":
    unittest.main()
