"""Re-execute submitted A0 test artifacts; this does not regenerate tests with an LLM."""
from __future__ import annotations

import ast
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import statistics
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'code-agent'
sys.path[:0] = [str(REPO / 'src'), str(REPO)]
from eval.dataset import load_dataset

cases = [
    ('HumanEval/13', 'basic: greatest common divisor', 'return a if b == 0', 'return b if b == 0'),
    ('HumanEval/31', 'basic: primality', 'if n <= 1:', 'if n < 1:'),
    ('HumanEval/137', 'variant: numeric types and decimal comma', 'return None', 'return a'),
    ('HumanEval/159', 'variant: need and remaining boundary', 'remaining - need', 'remaining'),
    ('HumanEval/128', 'constraint: zero and empty array', 'if 0 in arr: return 0', 'if 0 in arr: return 1'),
]
instances = {i.instance_id: i for i in load_dataset(REPO / 'benchmarks/humaneval_plus_v2_20.jsonl')}
outcomes = []


def run_tests(workspace):
    env = dict(__import__('os').environ)
    env['PYTHONDONTWRITEBYTECODE'] = '1'
    result = subprocess.run(
        [sys.executable, '-m', 'pytest', 'test_solution.py', '-q', '-p', 'no:cacheprovider'],
        cwd=workspace, text=True, capture_output=True, timeout=12, env=env,
    )
    return {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


for case_id, purpose, original, replacement in cases:
    instance = instances[case_id]
    dirname = case_id.replace('/', '__')
    source = instance.solution_source
    test_path = REPO / 'results/v2_ablation/A0' / (dirname + '.tests.py')
    tests = test_path.read_text()
    ast.parse(tests)
    assert original in source, (case_id, original)
    with tempfile.TemporaryDirectory(prefix='review-replay-') as raw:
        workspace = Path(raw)
        solution = workspace / 'solution.py'
        solution.write_text(source)
        (workspace / 'test_solution.py').write_text(tests)
        repeats = [run_tests(workspace) for _ in range(3)]
        solution.write_text(source.replace(original, replacement, 1))
        mutant = run_tests(workspace)
        solution.write_text(source)
        recovery = run_tests(workspace)
    record = {
        'instance_id': case_id, 'purpose': purpose,
        'artifact': str(test_path.relative_to(REPO)),
        'artifact_sha256': hashlib.sha256(test_path.read_bytes()).hexdigest(),
        'original_repeats': repeats,
        'independent_mutant': {'replace': original, 'with': replacement, 'result': mutant},
        'restored_original': recovery,
        'correct_original_all_runs': all(r['returncode'] == 0 for r in repeats) and recovery['returncode'] == 0,
        'detects_independent_mutant': mutant['returncode'] == 1 and 'failed' in mutant['stdout'] and 'ERROR collecting' not in mutant['stdout'],
    }
    outcomes.append(record)
    print(case_id, 'original_codes', [r['returncode'] for r in repeats],
          'mutant_code', mutant['returncode'], 'restored_code', recovery['returncode'],
          'summary', repeats[0]['stdout'].strip().splitlines()[-1])
    sys.stdout.flush()

summaries = {}
consistency = []
stored_summary = json.loads((REPO / 'results/v2_ablation/summary.json').read_text())
print('STORED_SUMMARY_KEYS', list(stored_summary))
for variant in ['A0','A1','A2','A3']:
    paths = sorted((REPO / 'results/v2_ablation' / variant).glob('*.json'))
    records = [json.loads(p.read_text()) for p in paths]
    assert len(records) == 20
    assert len({r['instance_id'] for r in records}) == 20
    stats = {
        'n': len(records), 'statuses': dict(Counter(r['status'] for r in records)),
        'all_pass_rate': statistics.fmean(bool(r['final']['all_pass']) for r in records),
        'mutation_mean': statistics.fmean(r['final']['mutation_score'] for r in records if r['final']['mutation_score'] is not None),
        'turns_mean': statistics.fmean(r['agent']['turns'] for r in records),
        'tokens_reported_mean': statistics.fmean(r['agent']['total_tokens'] for r in records),
        'input_plus_output_mean': statistics.fmean(r['agent']['input_tokens'] + r['agent']['output_tokens'] for r in records),
        'duration_mean': statistics.fmean(r['duration_sec'] for r in records),
        'tests_files_present': sum((p.with_suffix('.tests.py')).is_file() for p in paths),
        'solution_artifact_matches_dataset': 0,
        'test_artifact_matches_workspace': 0,
        'network_attempt_flags': sum(bool(r['network_attempt']) for r in records),
    }
    for path,r in zip(paths,records):
        workspace = REPO / 'results/v2_ablation/workspaces' / variant / r['instance_id']
        stored_solution = (workspace / 'solution.py').read_text()
        if stored_solution == instances[r['instance_id']].solution_source:
            stats['solution_artifact_matches_dataset'] += 1
        else:
            consistency.append({'variant': variant, 'instance_id': r['instance_id'], 'problem': 'solution mismatch'})
        if path.with_suffix('.tests.py').read_text() == (workspace / 'test_solution.py').read_text():
            stats['test_artifact_matches_workspace'] += 1
        else:
            consistency.append({'variant': variant, 'instance_id': r['instance_id'], 'problem': 'tests mismatch'})
        if len(r['tool_trace']) != r['agent']['tool_calls']:
            consistency.append({'variant': variant, 'instance_id': r['instance_id'], 'problem': 'tool trace count mismatch'})
    summaries[variant] = stats
    print(variant, json.dumps(stats, ensure_ascii=False))

payload = {'evaluation_kind': 'submitted_artifact_reexecution_not_live_llm_generation',
           'core_cases': outcomes, 'raw_record_recalculation': summaries, 'consistency_issues': consistency}
stored_variants = {item['variant']: item for item in stored_summary['variants']}
payload['stored_summary_matches_raw_records'] = all(
    stored_variants[name]['n'] == stats['n']
    and abs(stored_variants[name]['all_pass_rate'] - stats['all_pass_rate']) < 0.000051
    and abs(stored_variants[name]['mutation_mean'] - stats['mutation_mean']) < 0.000051
    and abs(stored_variants[name]['tokens_mean'] - stats['tokens_reported_mean']) < 0.051
    for name, stats in summaries.items()
)
output = ROOT / 'artifact_replay.json'
output.write_text(json.dumps(payload, ensure_ascii=False, indent=2))
print('CONSISTENCY_ISSUES',consistency)
print('SAVED', output)
