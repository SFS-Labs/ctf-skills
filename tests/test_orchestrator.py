import importlib.util
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT = Path(__file__).resolve().parent.parent / 'bin' / 'skill-orchestrator.py'
spec = importlib.util.spec_from_file_location('sfs_router', SCRIPT)
router = importlib.util.module_from_spec(spec)
spec.loader.exec_module(router)

SKILLS = [
    ('safe-harbor', 'L0', 'knowledge', 'Authorized scope and report boundaries'),
    ('surya', 'L1', 'tool', 'Solidity contract function and call map'),
    ('slither', 'L2', 'tool', 'Solidity static security analyzer access control arithmetic overflow underflow'),
    ('echidna', 'L3', 'tool', 'Solidity property fuzzing invariant and counterexample'),
    ('medusa', 'L3', 'tool', 'Coverage guided solidity property fuzzer'),
    ('properties', 'L3', 'corpus', 'ERC20 solvency invariants'),
    ('mythril', 'L4', 'tool', 'Symbolic execution of EVM bytecode'),
    ('canonical-signatures', 'L5', 'tool', 'EVM function selectors and signatures'),
    ('pyevmasm', 'L5', 'tool', 'EVM bytecode disassembly'),
    ('cryo', 'L7', 'tool', 'Historical blockchain trace and balance extraction'),
    ('diffusc', 'L6', 'tool', 'Differential solidity upgrade fuzzing'),
    ('not-so-smart-contracts', 'L8', 'knowledge', 'Vulnerable smart contract patterns'),
    ('smart-contract-best-practices', 'L8', 'knowledge', 'Secure smart contract guidelines'),
    ('evm-cfg-builder', 'L5', 'tool', 'Bytecode control-flow graph construction'),
    ('abi-guesser', 'L5', 'tool', 'Bytecode ABI reconstruction'),
]

class RouteTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        data = {'skills': []}
        for slug, layer, kind, role in SKILLS:
            data['skills'].append({'slug': slug, 'layer': layer, 'kind': kind, 'role': role, 'triggers': role.lower().split(), 'pairs_with': []})
            p = self.root / 'knowledge' / slug / 'SKILL.md'
            p.parent.mkdir(parents=True)
            p.write_text(f'# {slug}\n\n{role}\nWhen appropriate, use for code-focused review.\n', encoding='utf-8')
        (self.root / 'manifest.json').write_text(json.dumps(data), encoding='utf-8')

    def tearDown(self):
        self.tmp.cleanup()

    def test_non_security_task_does_not_trigger(self):
        answer = router.route('Write social media marketing copy for a restaurant', self.root)
        self.assertEqual('NO_MATCH', answer['status'])
        self.assertEqual([], answer['candidates'])

    def test_crypto_news_does_not_activate_smart_contract_auditor(self):
        self.assertEqual('NO_MATCH', router.route('What is the Ethereum price today?', self.root)['status'])

    def test_solana_smart_contract_not_misidentified_as_evm(self):
        self.assertEqual('NO_MATCH', router.route('Review Solana smart contract program', self.root)['status'])

    def test_non_evm_chain_does_not_route_evm_tools(self):
        answer = router.route('Review a Solana Anchor Rust program', self.root)
        self.assertEqual('NO_MATCH', answer['status'])

    def test_underflow_picks_static_and_property_tools(self):
        answer = router.route('Audit Solidity DEX emergencyWithdraw unchecked underflow and balance accounting', self.root)
        names = [s['slug'] for s in answer['candidates']]
        self.assertIn('slither', names)
        self.assertIn('echidna', names)
        self.assertEqual('ROUTED_NOT_EXECUTED', answer['status'])
        self.assertEqual('COUNTEREXAMPLE', answer['dag'][-3]['id'])

    def test_historical_requires_fork_verification(self):
        answer = router.route('Reproduce historical exploit in BSC smart contract at block 82730141', self.root, top_k=9)
        steps = {x['id']: x for x in answer['dag']}
        self.assertIn('FORK', steps)
        self.assertEqual(['FORK'], steps['HYPOTHESES']['depends_on'])
        self.assertIn('cryo', [x['slug'] for x in answer['candidates']])

    def test_signature_requires_more_than_only_static(self):
        answer = router.route('Analyze solidity claim EIP712 signature signer replay and ABI', self.root, top_k=9)
        names = [x['slug'] for x in answer['candidates']]
        self.assertIn('canonical-signatures', names)
        self.assertTrue(any(n in names for n in ('mythril', 'pyevmasm')))

    def test_upgrade_retrieval(self):
        answer = router.route('Verify Solidity proxy upgrade storage layout diff', self.root, top_k=7)
        self.assertIn('diffusc', [x['slug'] for x in answer['candidates']])

    def test_scales_to_134_entries_with_distractors(self):
        data = json.loads((self.root / 'manifest.json').read_text())
        for i in range(134 - len(data['skills'])):
            data['skills'].append({'slug': f'irrelevant-module-{i:03d}',
                                   'layer': 'L8', 'kind': 'knowledge',
                                   'role': 'Styling image assets for marketing',
                                   'triggers': ['visual', 'marketing'], 'pairs_with': []})
        (self.root / 'manifest.json').write_text(json.dumps(data))
        result = router.route('Security audit Solidity DEX unchecked emergencyWithdraw underflow', self.root)
        self.assertEqual(134, result['catalog_entries'])
        self.assertIn('slither', [x['slug'] for x in result['candidates']])
        self.assertLessEqual(len(result['candidates']), 7)

    def test_dependencies_reference_only_existing_nodes_and_are_acyclic(self):
        for task in ['Audit solidity reentrancy', 'Reproduce historical Ethereum contract exploit at block 19000000']:
            answer = router.route(task, self.root)
            seen = set()
            for node in answer['dag']:
                self.assertTrue(set(node['depends_on']) <= seen)
                seen.add(node['id'])

    def test_evidence_requires_independent_hashes_and_local_counterexample(self):
        artifact = self.root / 'counterexample.json'
        artifact.write_text('{"test": "pass"}', encoding='utf-8')
        checksum = hashlib.sha256(artifact.read_bytes()).hexdigest()
        partial = {'evidence': [{'path': str(artifact), 'family': 'source_review', 'sha256': checksum}]}
        self.assertFalse(router.assess(partial, self.root)['structural_evidence_ready'])
        second = self.root / 'independent.log'
        second.write_text('forge test: 1 passed; 0 failed', encoding='utf-8')
        partial['evidence'].append({'path': str(second), 'family': 'local_counterexample', 'sha256': hashlib.sha256(second.read_bytes()).hexdigest()})
        result = router.assess(partial, self.root)
        self.assertTrue(result['structural_evidence_ready'])
        self.assertFalse(result['can_claim_verified_exploit'])
        partial['evidence'][1]['sha256'] = '0' * 64
        self.assertFalse(router.assess(partial, self.root)['structural_evidence_ready'])

if __name__ == '__main__':
    unittest.main()
