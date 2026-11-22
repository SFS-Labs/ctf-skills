"""Tests for safe project-local skill copying (not native Freebuff runtime)."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent.parent / "bin/install-project-v8.py"
REL = Path(".agents/skills/ctf-skill-index-v8/SKILL.md")
SKILL = "---\nname: ctf-skill-index-v8\ndescription: Local authorized EVM analysis\n---\n\nbin/skill-orchestrator.py\n"


class ProjectInstallerTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        base = Path(self.tmp.name)
        self.project = base / "project"
        self.project.mkdir()
        self.repo = base / "repo"
        source = self.repo / REL
        source.parent.mkdir(parents=True)
        source.write_text(SKILL, encoding="utf-8")
        self.dest = self.project / REL

    def run_cli(self, *extra):
        return subprocess.run([sys.executable, str(SCRIPT), "--project", str(self.project),
                               "--skills-root", str(self.repo), *extra],
                              capture_output=True, text=True, timeout=10)

    def test_dry_run_is_non_mutating(self):
        proc = self.run_cli()
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(json.loads(proc.stdout)["status"], "DRY_RUN")
        self.assertFalse(self.dest.exists())

    def test_apply_is_idempotent_and_never_runtime_proof(self):
        first = self.run_cli("--apply")
        self.assertEqual(first.returncode, 0, first.stderr)
        self.assertEqual(self.dest.read_text(encoding="utf-8"), SKILL)
        self.assertFalse(json.loads(first.stdout)["native_skill_invocation_observed"])
        second = self.run_cli("--apply")
        self.assertEqual(second.returncode, 0, second.stderr)
        self.assertEqual(json.loads(second.stdout)["status"],
                         "ALREADY_IDENTICAL_RUNTIME_UNVERIFIED")

    def test_conflict_is_not_overwritten(self):
        self.dest.parent.mkdir(parents=True)
        self.dest.write_text("existing user skill", encoding="utf-8")
        proc = self.run_cli("--apply")
        self.assertNotEqual(proc.returncode, 0)
        self.assertEqual(self.dest.read_text(encoding="utf-8"), "existing user skill")

    def test_symlinked_destination_rejected(self):
        (self.project / ".agents").symlink_to(self.repo / ".agents", target_is_directory=True)
        proc = self.run_cli("--apply")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("symlinked destination", proc.stderr)


if __name__ == "__main__":
    unittest.main()
