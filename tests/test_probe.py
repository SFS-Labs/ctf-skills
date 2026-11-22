import importlib.util
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parent.parent / 'bin' / 'skill-orchestrator.py'
spec = importlib.util.spec_from_file_location('sfs_router_probe', SCRIPT)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

class ProbeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.source = self.root / 'Target.sol'
        self.source.write_text('pragma solidity ^0.8.20; contract Target {}')
        self.bindir = self.root / 'bin'
        self.bindir.mkdir()
        for name in ('surya', 'slither'):
            executable = self.bindir / name
            executable.write_text('#!/bin/sh\nprintf "%s\n" "' + name + ': simulated successful probe"\n')
            executable.chmod(0o755)

    def tearDown(self):
        self.tmp.cleanup()

    def test_probe_requires_explicit_execution_gate(self):
        with self.assertRaisesRegex(ValueError, 'allow-exec'):
            router.execute_static(self.source, self.root / 'out')

    def test_probe_rejects_non_solidity_file(self):
        other = self.root / 'foo.sh'
        other.write_text('#!/bin/sh\necho hi')
        with self.assertRaisesRegex(ValueError, 'regular .sol'):
            router.execute_static(other, self.root / 'out', True)

    def test_probe_invokes_two_binaries_sequentially_and_creates_evidence(self):
        with patch.dict(os.environ, {'PATH': str(self.bindir)}, clear=False):
            result = router.execute_static(self.source, self.root / 'out', True, 2)
        self.assertEqual(2, len(result['runs']))
        self.assertEqual(['surya','slither'], [r['tool'] for r in result['runs']])
        self.assertEqual(['EXECUTED_ZERO']*2, [r['status'] for r in result['runs']])
        self.assertTrue((self.root / 'out' / 'execution-receipt.json').is_file())
        self.assertTrue((self.root / 'out' / 'surya.log').is_file())
        self.assertFalse(result['completion'] == 'verified exploit')

    def test_ram_pressure_prevents_spawning(self):
        with patch.object(router, 'enough_memory', return_value=False):
            result = router.execute_static(self.source, self.root / 'out', True, 2)
        self.assertEqual(1, len(result['runs']))
        self.assertEqual('SKIPPED_RESOURCE_PRESSURE', result['runs'][0]['status'])

    def test_probe_unavailable_records_unavailability_not_success(self):
        with patch.object(router.shutil, 'which', return_value=None):
            result = router.execute_static(self.source, self.root / 'out', True, 2)
        self.assertTrue(all(r['status'] == 'UNAVAILABLE' for r in result['runs']))

if __name__ == '__main__':
    unittest.main()
