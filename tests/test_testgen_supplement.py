"""Supplement admission, ITT reporting and real deferred guided-loop traces."""
import json
from pathlib import Path

import pytest

from code_agent.config import Settings
from eval.dataset import Instance, load_dataset
from eval.runner import default_variant, run_single
from scripts.analyze_testgen_supplement import summarize
from scripts.run_testgen_supplement import compatibility
from tests.helpers import ScriptedLLM, tool_response

SOLUTION = 'def classify(x):\n    """Return -1 below zero and 1 otherwise."""\n    if x < 0:\n        return -1\n    return 1\n'
WEAK = 'from solution import classify\ndef test_positive():\n    assert classify(1)==1\n'
STRONG = WEAK+'def test_negative():\n    assert classify(-1)==-1\n'
WRONG = 'from solution import classify\ndef test_wrong():\n    assert classify(1)==999\n'


@pytest.mark.parametrize('variant,first,decisions',[('A2',WRONG,['tests_failed','tests_passed']),('A3',WEAK,['coverage_incomplete','coverage_full'])])
def test_deferred_scoring_keeps_real_guided_trace(tmp_path,monkeypatch,variant,first,decisions):
    from code_agent import assembly
    llm=ScriptedLLM([tool_response(('write_file',{'path':'test_solution.py','content':first})),
                     tool_response(('write_file',{'path':'test_solution.py','content':STRONG,'overwrite':True}))])
    monkeypatch.setattr(assembly,'build_llm',lambda settings:(llm,'scripted'))
    outcome=run_single(Instance('D/1','',SOLUTION,'classify',''),default_variant(variant),run_root=tmp_path,
                       settings_factory=lambda workspace:Settings(workspace=workspace,allow_write=True),
                       defer_measurement=True,checkpoints=(),max_mutants=2,measurement_timeouts=(3,10,3))
    assert outcome.final['all_pass'] and outcome.agent['turns']==2
    assert [a['decision'] for a in outcome.agent['system_actions']]==decisions
    assert not outcome.checkpoints and outcome.agent['measurement_deferred']


def fixture_output(tmp_path):
    output=tmp_path/'new'; baseline=tmp_path/'baseline'; target=output/'source/benchmarks/data.jsonl'
    target.parent.mkdir(parents=True); baseline.mkdir()
    original=Path(__file__).resolve().parents[1]/'benchmarks/humaneval_plus_v2_20.jsonl'
    target.write_bytes(original.read_bytes())
    ids=[x.instance_id for x in load_dataset(target)]
    (output/'manifest.json').write_text(json.dumps({'baseline_directory':str(baseline),'baseline_sha256':{},
        'dataset':'benchmarks/data.jsonl','total_token_limit':30000,'jobs':[(v,iid) for v in ('A1','A2','A3') for iid in ids]}))
    for v in ('A0','A1','A2','A3','A4'):
        folder=(baseline if v in ('A0','A4') else output)/v; folder.mkdir()
        for iid in ids:
            (folder/(iid.replace('/','__')+'.json')).write_text(json.dumps({'variant':v,'instance_id':iid,'status':'no_tests','final':{},'agent':{}}))
    return output,ids


def test_no_suite_failures_stay_in_all_100_runs(tmp_path):
    output,ids=fixture_output(tmp_path); s=summarize(output)
    assert s['complete'] and s['new_jobs']==60 and s['reused_jobs']==40
    assert s['variants']['A3']['valid_mutation']==0
    assert all(c['n']==20 and c['all_pairs_tied'] and c['holm_p']==1 for c in s['comparisons'].values())


def test_hook_restoration_is_scored_as_modification(tmp_path):
    from eval.mutation import generate_mutants
    output,ids=fixture_output(tmp_path)
    instance=load_dataset(output/'source/benchmarks/data.jsonl')[0]
    total=len(generate_mutants(instance.solution_source))
    p=output/'A2'/(instance.instance_id.replace('/','__')+'.json')
    p.write_text(json.dumps({'variant':'A2','instance_id':instance.instance_id,'status':'all_pass',
        'final':{'all_pass':True,'mutation_score':1,'mutants_total':total,'mutants_killed':total},
        'agent':{'system_actions':[{'status':'PASS','decision':'tests_passed','solution_restored':True}]}}))
    s=summarize(output)
    assert s['variants']['A2']['valid_mutation']==0 and s['variants']['A2']['solution_modifications']==1


def test_extra_record_rejected(tmp_path):
    output,ids=fixture_output(tmp_path)
    (output/'A1'/'HumanEval__999.json').write_text(json.dumps({'variant':'A1','instance_id':'HumanEval/999'}))
    with pytest.raises(ValueError,match='Unexpected'):
        summarize(output)


def test_live_compatibility_allows_only_logging_assignment(tmp_path,monkeypatch):
    from scripts import run_testgen_supplement as supplement
    root=Path(__file__).resolve().parents[1]
    parent=json.loads((root/'results/testgen_formal_v1/manifest.json').read_text())
    parent['files_sha256']={'eval/runner.py':parent['files_sha256']['eval/runner.py']}
    baseline=tmp_path/'baseline'; frozen=baseline/'source/eval/runner.py'; frozen.parent.mkdir(parents=True)
    frozen.write_bytes((root/'results/testgen_formal_v1/source/eval/runner.py').read_bytes())
    current=tmp_path/'eval/runner.py'; current.parent.mkdir()
    # This is the frozen v1 compatibility contract, not the evolving live v2 engine.
    original=frozen.read_text()
    current.write_text(original.replace('                finish_hook = bounded_hook\n', supplement.STATE_LINE+'                finish_hook = bounded_hook\n', 1))
    (baseline/'manifest.json').write_text(json.dumps(parent))
    environment=json.loads((root/'results/testgen_formal_v1/environment.json').read_text())
    (baseline/'environment.json').write_text(json.dumps(environment))
    monkeypatch.setattr(supplement,'ROOT',tmp_path)
    monkeypatch.setattr(supplement,'environment_snapshot',lambda:environment)
    settings=Settings(workspace=tmp_path,model=parent['model'],base_url=parent['base_url'])
    delta=compatibility(baseline,settings)
    assert set(delta)=={'eval/runner.py'}
    current.write_text(current.read_text()+'\n# unapproved shared engine edit\n')
    with pytest.raises(ValueError,match='Shared baseline engine changed'):
        compatibility(baseline,settings)
    settings.model='different-model'
    with pytest.raises(ValueError,match='Model/provider'):
        compatibility(baseline,settings)
