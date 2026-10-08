"""Two fixed-seed diagnostic controls of one unstable scoring case; no score replacement."""
import hashlib
import json
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'src'),str(ROOT)]
from eval.dataset import load_dataset
from eval.metrics import run_pytest_on
from eval.mutation import generate_mutants


def main():
    output=ROOT/'results/testgen_supplement_v1'
    record_path=output/'A1/HumanEval__39.json'; suite_path=record_path.with_suffix('.tests.py')
    record_bytes=record_path.read_bytes(); suite_bytes=suite_path.read_bytes()
    instance=next(x for x in load_dataset(output/'source/benchmarks/humaneval_plus_v2_20.jsonl') if x.instance_id=='HumanEval/39')
    mutants=generate_mutants(instance.solution_source)
    def trial(seed):
        rows=[]
        with tempfile.TemporaryDirectory(prefix='prime-fib-control-') as tmp:
            w=Path(tmp); (w/'test_solution.py').write_bytes(suite_bytes)
            for mutant in mutants:
                (w/'solution.py').write_text(f'import random\nrandom.seed({seed})\n'+mutant.source)
                result=run_pytest_on('test_solution.py',w,timeout=5)
                killed=not result.process.timed_out and (result.failed>0 or result.errors>0)
                rows.append({'mutant_id':mutant.mutant_id,'operator':mutant.operator,'line':mutant.line,
                             'description':mutant.description,'killed':killed,'timed_out':result.process.timed_out,
                             'passed':result.passed,'failed':result.failed,'errors':result.errors})
                print(f'seed={seed} {mutant.mutant_id} killed={killed} timeout={result.process.timed_out}',flush=True)
        return {'seed':seed,'mutants_total':len(rows),'mutants_killed':sum(r['killed'] for r in rows),
                'mutants_errors':sum(r['timed_out'] for r in rows),'per_mutant':rows}
    with ThreadPoolExecutor(max_workers=2) as pool:
        trials=list(pool.map(trial,(0,1)))
    different=[a['mutant_id'] for a,b in zip(trials[0]['per_mutant'],trials[1]['per_mutant'])
               if (a['killed'],a['timed_out'])!=(b['killed'],b['timed_out'])]
    original=json.loads(record_bytes)
    replay=json.loads((ROOT/'verification/testgen-supplement-v1/replay.json').read_text())
    unseeded=next(r for r in replay['records'] if r['record']=='A1/HumanEval__39.json')
    assert record_path.read_bytes()==record_bytes and suite_path.read_bytes()==suite_bytes
    receipt={'scope':'Post-hoc diagnostic only, seeds 0 and 1 prepended to the private mutant modules; neither primary scoring nor saved source/suite is changed',
             'case':'A1/HumanEval/39','tool_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
             'original_record_sha256':hashlib.sha256(record_bytes).hexdigest(),'original_suite_sha256':hashlib.sha256(suite_bytes).hexdigest(),
             'original_unseeded_counts':{k:original['final'][k] for k in ('mutants_total','mutants_killed','mutants_errors')},
             'replay_unseeded_counts':{k:unseeded[k] for k in ('mutants_total','mutants_killed','mutation_errors')},
             'seed_controls':trials,'different_mutants_between_seeds':different,
             'effective_primary_score':0,'reason':'Original and replay reference both fail; raw score variability cannot inflate the valid primary score',
             'limitation':'Two seed controls are diagnostic, not a new primary estimate or an exhaustive variance study'}
    (ROOT/'verification/testgen-supplement-v1/prime-fib-variability.json').write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'seed_counts':[{k:t[k] for k in ('seed','mutants_total','mutants_killed','mutants_errors')} for t in trials],
                      'different_mutants':different}),flush=True)


if __name__=='__main__':
    main()
