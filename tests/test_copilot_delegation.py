"""Tests fuer die Copilot-Delegationsschicht.

Alle API-Aufrufe gehen gegen einen lokalen HTTP-Mock mit simulierten
GitHub-Antworten. Es gibt keinen echten GitHub-Schreibzugriff, keine
Copilot-Delegation und keine Kosten.
"""
import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "bin" / "copilot-delegate.py"
spec = importlib.util.spec_from_file_location("sfs_copilot_delegate", SCRIPT)
cp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cp)

TASK = ("Add a bounded fix in src/fix.py so the existing tests pass and add a "
        "regression test for the sign error.")


class DelegationBase(unittest.TestCase):
    scenario = "happy"

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.state = Path(self.tmp.name) / "state"
        self.mock = cp.MockGitHub(self.scenario).start()
        self.client = cp.GitHubClient(token="test-token", api_url=self.mock.url, retries=2)

    def tearDown(self):
        self.mock.stop()
        self.tmp.cleanup()

    def brief(self, task=TASK):
        return cp.detect_brief(task, "demo/repo", "main", ["src/fix.py"])

    def open_gate(self):
        cp.save_policy(self.state, {
            **cp.DEFAULT_POLICY,
            "paid_delegation_allowed": True,
            "credits_exhausted": False,
        })

    def delegate(self, route="issue", simulated=True, execute=True):
        return cp.create_delegation(
            self.client, self.brief(), self.state, route=route,
            execute=execute, allow_paid=True, simulated=simulated)

    def deliver(self, scenario="happy", route="issue"):
        self.mock.scenario = scenario
        record = self.delegate(route=route)
        return cp.watch(self.client, record, self.state, follow=True,
                        interval=0, max_polls=4)


class PreflightTests(DelegationBase):
    def test_read_only_preflight_reports_copilot_routes_and_closed_gate(self):
        result = cp.preflight(self.client, "demo/repo", state_dir=self.state,
                              standard=cp.load_local_standard(), simulated=True)
        self.assertEqual("SFS-Labs", result["login"])
        self.assertEqual(cp.BOT_LOGIN, result["copilot"]["bot_login"])
        self.assertTrue(result["routes"]["issue"]["available"])
        self.assertTrue(result["routes"]["agent-task"]["available"])
        self.assertFalse(result["paid_gate"]["open"])
        self.assertFalse(result["ready_to_delegate"])
        self.assertTrue(any("credits" in b for b in result["blockers"]))
        self.assertTrue(Path(result["receipt"]).is_file())

    def test_preflight_records_vendored_standard_and_pat_404(self):
        result = cp.preflight(self.client, "demo/repo", state_dir=self.state,
                              simulated=True)
        self.assertEqual("local-vendored", result["standard"]["source"])
        self.assertEqual(404, result["standard"]["remote_status"])
        self.assertEqual(5, len(result["standard"]["domains"]))
        self.assertEqual("277ad8a4d45043b2fc6c9b463aa0d989596e976e",
                         result["standard"]["origin"]["blob_sha"])
        self.assertTrue(result["standard"]["path"].endswith(
            "COPILOT_PROFICIENCY_OPERATING_STANDARD.md"))

    def test_preflight_rejects_invalid_repo(self):
        with self.assertRaises(cp.CopilotError):
            cp.preflight(self.client, "not-a-repo", state_dir=self.state)

    def test_local_standard_cache_invalidates_when_file_changes(self):
        cp.write_json(self.state / "standard.json", {
            "fetched_epoch": cp.time.time(), "source": "local-fallback",
            "sha256": "0" * 64, "domains": [],
        })
        result = cp.resolve_standard(None, self.state, root=ROOT)
        self.assertNotEqual("0" * 64, result["sha256"])
        self.assertEqual("local-vendored", result["source"])


class DetectTests(unittest.TestCase):
    def test_builds_bounded_brief_with_paths_acceptance_and_tests(self):
        brief = cp.detect_brief(TASK, "demo/repo", "main", ["src/fix.py"])
        self.assertTrue(brief["eligibility"]["eligible"])
        self.assertEqual(["src/fix.py"], brief["allowed_paths"])
        self.assertEqual("main", brief["base_ref"])
        self.assertIn("src/fix.py", cp.build_prompt(brief))
        self.assertEqual([], cp.validate_brief(brief))

    def test_rejects_broad_or_unbounded_task(self):
        brief = cp.detect_brief("Redesign the entire codebase and migrate everything.",
                                "demo/repo")
        self.assertFalse(brief["eligibility"]["eligible"])
        self.assertIn("breite/architekturweite Formulierung", " ".join(
            brief["eligibility"]["reasons"]))

    def test_rejects_forbidden_scope(self):
        brief = cp.detect_brief("Deploy to production and rotate the API key.",
                                "demo/repo")
        self.assertFalse(brief["eligibility"]["eligible"])
        self.assertTrue(brief["eligibility"]["forbidden_scope"])

    def test_validation_rejects_traversal_and_secrets(self):
        brief = cp.detect_brief(TASK, "demo/repo", "main", ["src/fix.py"])
        brief["allowed_paths"] = ["../etc/passwd"]
        self.assertTrue(any("invalid path" in e for e in cp.validate_brief(brief)))
        brief = cp.detect_brief(TASK, "demo/repo", "main", ["src/fix.py"])
        brief["objective"] += " token=ghp_" + "a" * 36
        self.assertTrue(any("secret-like" in e for e in cp.validate_brief(brief)))


class GateTests(DelegationBase):
    def test_dry_run_sends_no_write(self):
        result = cp.create_delegation(self.client, self.brief(), self.state,
                                      execute=False, allow_paid=True, simulated=True)
        self.assertEqual("DRY_RUN", result["status"])
        self.assertEqual([], self.mock.write_calls)
        self.assertTrue(result["planned_requests"])

    def test_execute_without_paid_gate_writes_nothing(self):
        result = cp.create_delegation(self.client, self.brief(), self.state,
                                      execute=True, allow_paid=False, simulated=False)
        self.assertEqual("BLOCKED_PAID_GATE", result["state"])
        self.assertEqual([], self.mock.write_calls)
        self.assertIn("--allow-paid missing", result["blocked_reasons"])

    def test_execute_with_flag_but_closed_policy_writes_nothing(self):
        result = cp.create_delegation(self.client, self.brief(), self.state,
                                      execute=True, allow_paid=True, simulated=False)
        self.assertEqual("BLOCKED_PAID_GATE", result["state"])
        self.assertEqual([], self.mock.write_calls)
        self.assertTrue(any("credits_exhausted" in r for r in result["blocked_reasons"]))

    def test_policy_gate_requires_both_policy_flags(self):
        cp.save_policy(self.state, {**cp.DEFAULT_POLICY,
                                    "paid_delegation_allowed": True,
                                    "credits_exhausted": True})
        result = cp.create_delegation(self.client, self.brief(), self.state,
                                      execute=True, allow_paid=True, simulated=False)
        self.assertEqual("BLOCKED_PAID_GATE", result["state"])
        self.assertEqual([], self.mock.write_calls)


class IssueDelegationTests(DelegationBase):
    def test_execute_creates_issue_and_assigns_copilot(self):
        self.open_gate()
        record = self.delegate(simulated=False)
        self.assertEqual("DELEGATED", record["state"])
        self.assertEqual(71, record["remote"]["issue_number"])
        self.assertTrue(record["remote"]["assigned"])
        self.assertTrue(any(m == "POST" and p == "/repos/demo/repo/issues"
                            for m, p in self.mock.write_calls))
        self.assertTrue(any(m == "POST" and p == "/graphql"
                            for m, p in self.mock.write_calls))

    def test_duplicate_brief_is_not_created_twice(self):
        self.open_gate()
        first = self.delegate(simulated=False)
        second = self.delegate(simulated=False)
        self.assertEqual(first["id"], second["id"])
        self.assertEqual(first["id"], second["duplicate_of"])
        issue_posts = [1 for m, p in self.mock.write_calls
                       if m == "POST" and p == "/repos/demo/repo/issues"]
        self.assertEqual(1, len(issue_posts))

    def test_auto_route_falls_back_to_agent_task_when_issues_disabled(self):
        self.mock.has_issues = False
        self.open_gate()
        record = self.delegate(route="auto", simulated=False)
        self.assertEqual("agent-task", record["route"])
        self.assertEqual("task-1", record["remote"]["task_id"])
        self.assertEqual("DELEGATED", record["state"])
        self.assertFalse(any(m == "POST" and p == "/repos/demo/repo/issues"
                             for m, p in self.mock.write_calls))

    def test_assignment_failure_is_recorded_without_claiming_success(self):
        self.mock.scenario = "assign-failure"
        self.open_gate()
        record = self.delegate(simulated=False)
        self.assertFalse(record["remote"]["assigned"])
        self.assertEqual("FAILED", record["state"])
        self.assertIn("assignment failed", record["history"][-1]["detail"])


class WatchTests(DelegationBase):
    def test_watch_finds_pr_and_passing_ci(self):
        record = self.deliver()
        self.assertEqual("COMPLETED", record["state"])
        self.assertEqual(12, record["pull_request"]["number"])
        self.assertEqual("abc123def456", record["pull_request"]["head_sha"])
        self.assertEqual("success", record["ci"]["conclusion"])
        self.assertTrue(record["observed_activity"])
        self.assertIn("copilot/fix-add", record["branches"])

    def test_quota_comment_is_terminal_failure(self):
        record = self.deliver("quota")
        self.assertEqual("QUOTA_BLOCKED", record["state"])
        self.assertIn("credits", record["history"][-1]["detail"].lower())

    def test_watch_limit_is_not_success(self):
        self.mock.scenario = "timeout"
        record = self.delegate()
        record = cp.watch(self.client, record, self.state, follow=True,
                          interval=0, max_polls=2)
        self.assertEqual("WATCH_LIMIT_REACHED", record["state"])
        self.assertNotIn(record["state"], cp.SUCCESS_STATES)

    def test_agent_task_route_completes_with_pull_artifact(self):
        record = self.deliver(route="agent-task")
        self.assertEqual("COMPLETED", record["state"])
        self.assertEqual(12, record["pull_request"]["number"])

    def test_rate_limit_is_retried(self):
        record = self.deliver("rate-limit", route="agent-task")
        self.assertTrue(self.mock.rate_limited)
        self.assertEqual("COMPLETED", record["state"])


class ReviewTests(DelegationBase):
    def _review(self, scenario="happy", pr_login=cp.BOT_FULL):
        self.mock.pr_login = pr_login
        record = self.deliver(scenario)
        return cp.review_delegation(self.client, record, self.state)

    def test_happy_diff_is_verified_with_ci(self):
        result = self._review()
        self.assertEqual("VERIFIED", result["verdict"])
        self.assertEqual("abc123def456", result["head_sha"])
        self.assertEqual(1, len(result["files"]))
        self.assertTrue(Path(result["receipt"]).is_file())
        self.assertIn("kein Auto-Merge", " ".join(result["next_actions"]))
        self.assertIn("Copilot evidence: not verified (simulated mock",
                      result["evidence_note"])
        self.assertIn("Decision: VERIFIED", result["evidence_note"])

    def test_ci_failure_requires_changes(self):
        result = self._review("ci-failure")
        self.assertEqual("CHANGES_REQUIRED", result["verdict"])
        self.assertTrue(any(c["name"] == "ci" and c["status"] == "FAIL"
                            for c in result["checks"]))

    def test_workflow_file_is_out_of_scope(self):
        result = self._review("scope-violation")
        self.assertEqual("CHANGES_REQUIRED", result["verdict"])
        self.assertTrue(any(c["name"] == "scope" and c["status"] == "FAIL"
                            for c in result["checks"]))

    def test_secret_in_diff_is_rejected(self):
        result = self._review("secret")
        self.assertEqual("CHANGES_REQUIRED", result["verdict"])
        self.assertTrue(any(c["name"] == "secret_scan" and c["status"] == "FAIL"
                            for c in result["checks"]))

    def test_non_copilot_author_is_rejected(self):
        result = self._review("happy", pr_login="mallory")
        self.assertEqual("CHANGES_REQUIRED", result["verdict"])
        self.assertTrue(any(c["name"] == "copilot_authorship" and c["status"] == "FAIL"
                            for c in result["checks"]))

    def test_changed_head_sha_is_rejected(self):
        record = self.deliver()
        record["pull_request"]["head_sha"] = "0" * 12
        result = cp.review_delegation(self.client, record, self.state)
        self.assertEqual("CHANGES_REQUIRED", result["verdict"])
        self.assertTrue(any(c["name"] == "head_sha" and c["status"] == "FAIL"
                            for c in result["checks"]))

    def test_no_merge_endpoint_is_called(self):
        self._review()
        for method, path in self.mock.calls:
            self.assertNotIn(method, ("PUT", "DELETE"))
            self.assertNotIn("/merge", path)
            self.assertNotIn("/merge", path.lower())


class ProficiencyTests(DelegationBase):
    def test_simulated_delegation_is_excluded(self):
        record = self.deliver()
        result = cp.review_delegation(self.client, record, self.state)
        self.assertEqual("VERIFIED", result["verdict"])
        report = cp.collect_proficiency(self.state)
        self.assertEqual(0, report["proven_domains"])
        self.assertEqual(1, report["simulated_excluded"])
        self.assertIn("Keine echte", cp.proficiency_markdown(report))

    def test_real_verified_record_maps_all_five_domains(self):
        state = Path(self.tmp.name) / "real-state"
        cp.ensure_state(state)
        receipt_path = cp.review_dir(state) / "d-real-abc123.json"
        receipt = {
            "delegation_id": "d-real",
            "verdict": "VERIFIED",
            "head_sha": "abc123def456",
            "checks": [{"name": "scope", "status": "PASS"}],
            "ci": {"conclusion": "success"},
            "diff_sha256": "d" * 64,
        }
        cp.write_json(receipt_path, receipt)
        record = {
            "id": "d-real",
            "simulated": False,
            "state": "REVIEWED",
            "repo": "demo/repo",
            "observed_activity": True,
            "brief_sha256": "b" * 64,
            "pull_request": {"html_url": "https://github.com/demo/repo/pull/12",
                             "head_sha": "abc123def456"},
            "review": {
                "verdict": "VERIFIED",
                "head_sha": "abc123def456",
                "receipt": str(receipt_path),
                "receipt_sha256": cp.sha256_bytes(receipt_path.read_bytes()),
            },
            "agent_configuration": {"observed": True, "kind": "custom_agent",
                                    "sha256": "c" * 64},
            "tool_context": {"observed": True, "tools": ["mcp:demo"]},
        }
        cp.write_json(cp.delegation_dir(state) / "d-real.json", record)
        report = cp.collect_proficiency(state)
        self.assertEqual(5, report["proven_domains"])
        self.assertEqual(0, report["simulated_excluded"])
        self.assertTrue(all(row["status"] == "PROVEN" for row in report["domains"].values()))

    def test_unreviewed_real_record_is_not_counted(self):
        state = Path(self.tmp.name) / "unreviewed-state"
        cp.ensure_state(state)
        record = {
            "id": "d-open", "simulated": False, "state": "COMPLETED",
            "repo": "demo/repo", "observed_activity": True,
            "brief_sha256": "b" * 64,
            "pull_request": {"html_url": "https://github.com/demo/repo/pull/2",
                             "head_sha": "f" * 12},
        }
        cp.write_json(cp.delegation_dir(state) / "d-open.json", record)
        report = cp.collect_proficiency(state)
        self.assertEqual(0, report["proven_domains"])


class HygieneTests(DelegationBase):
    def test_token_is_never_written_to_state(self):
        token = "ghp_" + "c" * 36
        client = cp.GitHubClient(token=token, api_url=self.mock.url)
        cp.preflight(client, "demo/repo", state_dir=self.state,
                     standard=cp.load_local_standard(), simulated=True)
        cp.create_delegation(client, self.brief(), self.state, execute=True,
                             allow_paid=True, simulated=True)
        for path in self.state.rglob("*"):
            if path.is_file():
                self.assertNotIn(token, path.read_text(encoding="utf-8", errors="replace"))

    def test_vendored_standard_is_verbatim_and_lists_five_domains(self):
        text = (ROOT / "docs" / "COPILOT_PROFICIENCY_OPERATING_STANDARD.md").read_text(
            encoding="utf-8")
        for domain in ("AI Collaboration", "Prompting", "Code Generation & Validation",
                       "Agent Configuration", "Tool & Context Integration"):
            self.assertIn(domain, text)
        self.assertIn("SFS-Labs | GitHub Copilot Proficiency Operating Standard", text)
        meta = json.loads((ROOT / "docs" /
                           "COPILOT_PROFICIENCY_OPERATING_STANDARD.provenance.json")
                          .read_text(encoding="utf-8"))
        self.assertEqual(hashlib.sha256(text.encode("utf-8")).hexdigest(),
                         meta["content_sha256"])
        self.assertEqual("277ad8a4d45043b2fc6c9b463aa0d989596e976e", meta["blob_sha"])


class CliTests(unittest.TestCase):
    def test_demo_happy_returns_success_and_zero_spend(self):
        proc = subprocess.run([sys.executable, str(SCRIPT), "demo", "--scenario", "happy",
                               "--json"], capture_output=True, text=True, timeout=120)
        self.assertEqual(0, proc.returncode, proc.stderr)
        result = json.loads(proc.stdout)
        self.assertTrue(result["ok"])
        self.assertEqual("REVIEWED", result["state"])
        self.assertEqual(0, result["paid_spend"])
        self.assertEqual(0, result["proven_domains"])

    def test_orchestrator_exposes_copilot_preflight(self):
        proc = subprocess.run([sys.executable, str(ROOT / "bin" / "skill-orchestrator.py"),
                               "copilot", "--help"], capture_output=True, text=True, timeout=60)
        self.assertEqual(0, proc.returncode, proc.stderr)
        self.assertIn("preflight", proc.stdout)
        self.assertIn("delegate", proc.stdout)


if __name__ == "__main__":
    unittest.main()
