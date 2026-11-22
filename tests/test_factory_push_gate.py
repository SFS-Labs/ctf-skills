"""Hermetic regression tests for the optional public GitHub push gate.

No real credentials, remote requests, commits, or pushes are performed.
"""
import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent.parent / "bin" / "push"
spec = importlib.util.spec_from_file_location("factory_push", SCRIPT)
# Extension-less script: use SourceFileLoader explicitly.
from importlib.machinery import SourceFileLoader
spec = importlib.util.spec_from_loader("factory_push", SourceFileLoader("factory_push", str(SCRIPT)))
push = importlib.util.module_from_spec(spec)
spec.loader.exec_module(push)


class PublicPushGateTests(unittest.TestCase):
    def setUp(self):
        self.patches = [
            patch.object(push, "credentials", return_value=("synthetic-only-token", "GH_TOKEN")),
            patch.object(push, "api_visibility", return_value=(False, "main")),
            patch.object(push, "run_worker", return_value=(0, True)),
            patch.object(push, "api_ref", return_value="a" * 40),
            patch.object(push, "local_head", return_value="a" * 40),
        ]
        self.mocks = [p.start() for p in self.patches]
        self.addCleanup(self._stop_patches)

    def _stop_patches(self):
        for item in reversed(self.patches):
            item.stop()

    def test_canonical_repo_is_used(self):
        self.assertEqual(push.DEFAULT_REPO, "SFS-Labs/ctf-skills")

    def test_public_push_denied_without_explicit_gate(self):
        with self.assertRaises(SystemExit) as caught:
            push.main([])
        self.assertEqual(caught.exception.code, 2)
        self.mocks[2].assert_not_called()

    def test_public_push_explicit_flag_allows_mocked_worker(self):
        self.assertEqual(push.main(["--allow-public"]), 0)
        self.mocks[2].assert_called_once()

    def test_unknown_visibility_blocks_even_with_flag(self):
        self.mocks[1].return_value = (None, None)
        with self.assertRaises(SystemExit) as caught:
            push.main(["--allow-public"])
        self.assertEqual(caught.exception.code, 2)
        self.mocks[2].assert_not_called()


if __name__ == "__main__":
    unittest.main()
