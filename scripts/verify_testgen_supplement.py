"""Independent replay and aggregation of the 60 supplementary model records."""
import argparse
import hashlib
import json
import math
import sys
import tempfile
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from eval.dataset import load_dataset
from eval.metrics import run_mutation_tests, run_pytest_on
from eval.mutation import generate_mutants


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, default=ROOT / "results/testgen_supplement_v1")
    parser.add_argument("--receipt", type=Path, required=True)
    args = parser.parse_args(); output = args.results.resolve()
    manifest = json.loads((output / "manifest.json").read_text())
    for name, expected in manifest["files_sha256"].items():
        if hashlib.sha256((output/'source'/name).read_bytes()).hexdigest() != expected or hashlib.sha256((ROOT/name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Frozen/live supplementary source differs: " + name)
    baseline = ROOT / manifest["baseline_directory"]
    for name, expected in manifest["baseline_sha256"].items():
        if hashlib.sha256((baseline/name).read_bytes()).hexdigest() != expected:
            raise SystemExit("Reused baseline changed: " + name)
    instances = {x.instance_id:x for x in load_dataset(output/'source'/manifest['dataset'])}
    expected = {output/v/(iid.replace('/','__')+'.json') for v,iid in manifest['jobs']}
    if set(output.glob('A*/*.json')) != expected or len(expected) != 60:
        raise SystemExit("Supplementary job membership mismatch")
    def replay(path):
        d = json.loads(path.read_text()); f = d.get('final',{})
        if d['variant'] != path.parent.name or path.stem != d['instance_id'].replace('/','__'):
            raise ValueError("Supplement record identity mismatch")
        suite_path = path.with_suffix('.tests.py'); suite = suite_path.read_text() if suite_path.exists() else ''
        if len(suite) != d['tests_chars']:
            raise ValueError("Supplement suite length mismatch")
        row = {'record':str(path.relative_to(output)), 'record_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
               'suite_sha256':hashlib.sha256(suite_path.read_bytes()).hexdigest() if suite_path.exists() else None}
        if not suite:
            row.update(reference_matches=not f.get('all_pass',False), scoring_matches=not f.get('mutants_total',0), reference_restored=True)
            return row
        instance = instances[d['instance_id']]
        with tempfile.TemporaryDirectory(prefix='supplement-replay-') as tmp:
            w = Path(tmp); (w/'solution.py').write_text(instance.solution_source); (w/'test_solution.py').write_text(suite)
            reference = run_pytest_on('test_solution.py',w,timeout=manifest['measurement_seconds']['pytest'])
            mutation = run_mutation_tests(w,instance.solution_source,'test_solution.py',timeout=manifest['measurement_seconds']['per_mutant'])
            restored = (w/'solution.py').read_text() == instance.solution_source
        row.update(reference_passed=reference.all_pass, reference_timed_out=reference.timed_out,
                   reference_passed_count=reference.passed, reference_failed_count=reference.failed,
                   reference_errors_count=reference.errors, reference_summary=reference.summary_line,
                   reference_failure_output=(reference.stdout+reference.stderr)[-4000:] if not reference.all_pass else '',
                   reference_matches=reference.all_pass == f.get('all_pass',False),
                   mutants_total=mutation['total'], mutants_killed=mutation['killed'], mutation_errors=mutation['errors'],
                   scoring_matches=all(mutation[k] == f.get(saved,0) for k,saved in (('total','mutants_total'),('killed','mutants_killed'),('errors','mutants_errors'))),
                   reference_restored=restored)
        return row
    rows=[]
    with ThreadPoolExecutor(max_workers=2) as pool:
        for row in pool.map(replay,sorted(expected)):
            rows.append(row)
            print(f"[{len(rows)}/60] {row['record']} reference={row['reference_matches']} scoring={row['scoring_matches']}",flush=True)
    # Derive all five primary means directly; do not import the reporting helper.
    derived={}; summary=json.loads((output/'supplement_summary.json').read_text())
    for variant in ('A0','A1','A2','A3','A4'):
        folder = baseline if variant in ('A0','A4') else output
        records = [json.loads(p.read_text()) for p in sorted((folder/variant).glob('*.json'))]
        scores=[]; actions=[]; incomplete=0
        for d in records:
            f=d.get('final',{}); a=d.get('agent',{}).get('system_actions',[]); actions.extend(a)
            total=len(generate_mutants(instances[d['instance_id']].solution_source))
            valid=bool(f.get('all_pass')) and not (d.get('solution_modified') or f.get('solution_modified') or any(x.get('solution_restored') for x in a))
            measured=f.get('mutants_total')==total and f.get('mutation_score') is not None
            if total: scores.append(f.get('mutants_killed',0)/total if valid and measured else 0)
            incomplete += any(x.get('decision')=='coverage_incomplete' for x in a)
        derived[variant]={'runs':len(records),'valid_mutation':sum(scores)/len(scores) if scores else None,
                          'all_pass_rate':sum(bool(d.get('final',{}).get('all_pass')) for d in records)/len(records),
                          'tokens':sum(d.get('agent',{}).get('input_tokens',0)+d.get('agent',{}).get('output_tokens',0) for d in records)/len(records),
                          'system_pytest_runs':len(actions),'coverage_incomplete_instances':incomplete}
        if variant in ('A2','A3') and any(d.get('tests_chars') for d in records) and not actions:
            raise SystemExit("Guided mechanism trace missing: " + variant)
    matches=all(math.isclose(value,summary['variants'][variant][key],abs_tol=1e-12) for variant,fields in derived.items() for key,value in fields.items())
    receipt={'scope':'Offline replay only; original model records are not replaced', 'frozen_files_verified':len(manifest['files_sha256']),
             'baseline_files_verified':len(manifest['baseline_sha256']), 'jobs_verified':len(rows),
             'reference_matches':sum(r['reference_matches'] for r in rows), 'scoring_matches':sum(r['scoring_matches'] for r in rows),
             'summary_matches':matches, 'independent_primary_summary':derived, 'records':rows,
             'all_match':matches and all(r['reference_matches'] and r['scoring_matches'] and r['reference_restored'] for r in rows)}
    args.receipt.parent.mkdir(parents=True,exist_ok=True)
    args.receipt.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in receipt.items() if k!='records'},ensure_ascii=False),flush=True)
    if not receipt['all_match']:
        raise SystemExit('Replay differences require inspection; original records unchanged')


if __name__ == '__main__':
    main()
