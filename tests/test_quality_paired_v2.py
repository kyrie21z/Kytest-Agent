"""Task-clustered repeated reporting, frozen admission and actual feedback observations."""
import hashlib
import json
from pathlib import Path

import pytest

from code_agent.config import Settings
from code_agent.tools.factories import build_registry
from eval.dataset import Instance
from scripts.freeze_mbpp_quality import adapt, select_rows
from scripts.run_quality_paired_v2 import (MEASUREMENT_VERSION, independent_pools,
    observer_factory, result_path, summarize, verify_frozen)
from tests.helpers import ScriptedLLM, tool_response


def fixture_output(tmp_path):
    source='def choose(n):\n    """Return n plus one if positive, else zero."""\n    return n+1 if n>0 else 0\n'
    dataset=tmp_path/'source/benchmarks/new.jsonl'
    dataset.parent.mkdir(parents=True)
    instances=[Instance(f'D/{i}', '', source, 'choose', '') for i in range(2)]
    dataset.write_text(''.join(json.dumps(vars(x))+'\n' for x in instances))
    jobs=[(r,v,x.instance_id) for r in range(1,4) for v in ('A0','A4','A5') for x in instances]
    (tmp_path/'manifest.json').write_text(json.dumps({'schema':'testgen-quality-paired-v2',
        'measurement_version':MEASUREMENT_VERSION,'dataset':'benchmarks/new.jsonl','jobs':jobs,
        'files_sha256':{'benchmarks/new.jsonl':hashlib.sha256(dataset.read_bytes()).hexdigest()}}))
    for job in jobs:
        r,v,iid=job
        instance=next(x for x in instances if x.instance_id==iid)
        total=len(independent_pools(instance.solution_source)[1])
        passed=v!='A0' or r==1
        final={'measurement_version':MEASUREMENT_VERSION,'all_pass':passed,
               'mutants_total':total,'mutants_killed':total if passed else 0,
               'mutation_score':1 if passed else 0,'mutation_completion_rate':1 if passed else 0,
               'mutation_upper_bound':1 if passed else 0}
        path=result_path(tmp_path,job)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_text(json.dumps({'variant':v,'instance_id':iid,'status':'all_pass' if passed else 'no_tests',
            'final':final,'agent':{'input_tokens':10,'output_tokens':20}}))
    return jobs


def test_repeated_runs_are_clustered_by_task_and_failed_repeats_count_zero(tmp_path):
    fixture_output(tmp_path)
    report=summarize(tmp_path)
    assert report['complete'] and report['completed_jobs']==18
    assert report['variants']['A0']['confirmed_score_mean']==pytest.approx(1/3)
    assert report['variants']['A4']['confirmed_score_mean']==1
    assert report['comparisons']['A4-A0']['task_n']==2
    assert report['comparisons']['A4-A0']['mean_difference']==pytest.approx(2/3)
    assert report['comparisons']['A5-A4']['wilcoxon_p']==1
    assert len(report['paired_task_means'][0]['A0']['samples'])==3


def test_missing_run_prevents_complete_quality_claim(tmp_path):
    jobs=fixture_output(tmp_path)
    result_path(tmp_path,jobs[0]).unlink()
    report=summarize(tmp_path)
    assert not report['complete'] and not report['comparisons']


def test_mixed_measurement_is_rejected_and_frozen_input_tampering_detected(tmp_path):
    jobs=fixture_output(tmp_path)
    path=result_path(tmp_path,jobs[0]); row=json.loads(path.read_text())
    row['final']['measurement_version']='old-v1'
    path.write_text(json.dumps(row))
    with pytest.raises(ValueError,match='Mixed measurement'):
        summarize(tmp_path)
    (tmp_path/'source/benchmarks/new.jsonl').write_text('changed')
    with pytest.raises(ValueError,match='Frozen source mismatch'):
        verify_frozen(tmp_path)


def test_mbpp_selection_is_order_independent_and_uses_official_test_partition():
    root=Path(__file__).resolve().parents[1]
    rows=json.loads((root/'benchmarks/mbpp_quality_v2/sanitized-mbpp.json').read_text())
    chosen,metadata=select_rows(rows)
    repeated,_=select_rows(list(reversed(rows)))
    assert chosen==repeated and len(chosen)==20
    assert all(11<=x['source_task_id']<=510 for x in chosen)
    assert not metadata['selection_uses_model_outcomes']
    selected=json.loads((root/'benchmarks/mbpp_quality_v2/selection.json').read_text())
    assert metadata['selected_ids']==selected['selected_ids']


def test_mbpp_adaptation_preserves_code_and_original_task_text():
    row={'task_id':20,'prompt':'Return the input plus one.',
         'code':'def add(n):\n    return n+1\n','test_imports':[],'test_list':['assert add(2)==3']}
    adapted=adapt(row)
    assert repr(row['prompt']) in adapted['solution']
    assert 'return n+1' in adapted['solution']
    assert 'add = candidate' in adapted['official_tests']


def test_observer_records_feedback_suite_and_actual_next_model_input(tmp_path,monkeypatch):
    import scripts.run_quality_paired_v2 as runner
    from scripts.demo_fault_feedback import SOURCE,candidate
    from eval.runner import default_variant
    (tmp_path/'solution.py').write_text(SOURCE)
    settings=Settings(workspace=tmp_path)
    registry=build_registry(settings,('submit_tests','inspect_survivors'))
    llm=ScriptedLLM([tool_response(('submit_tests',{'cases':[candidate('test_inside',5,0)]})),
        tool_response(('submit_tests',{'cases':[candidate('test_below',1,-1),candidate('test_above',9,1),
            candidate('test_low',2,0),candidate('test_high',8,0)]}))])
    monkeypatch.setattr(runner,'build_llm',lambda _:(llm,'scripted'))
    trace={'requests':[],'development_stages':[]}
    path=tmp_path/'observation.json'
    agent=observer_factory(trace,path,[])(default_variant('A5'),settings,registry,tmp_path)
    agent.state.add_user('generate tests')
    result=agent.run()
    assert result.status=='stopped' and len(trace['development_stages'])==2
    first=trace['development_stages'][0]
    assert hashlib.sha256(first['suite_source'].encode()).hexdigest()==first['report']['suite_sha256']
    assert first['response'] in trace['requests'][1]['messages'][-1]['content']
    assert len(registry.get('submit_tests').generation.snapshot()['accepted'])==5
