"""Verify the HTTP interface, actual tools, cancellation, and truthful validation."""
import json
from pathlib import Path
import threading
import time
import urllib.error
import urllib.request

import pytest

from code_agent.config import Settings
from code_agent.llm import LLMResponse
from code_agent.web import server as web
from code_agent.web.demo import DemoLLM, SOURCE, TASK, TESTS
from code_agent.web.quality import evaluate_quality, pytest_counts
from tests.helpers import ScriptedLLM, text_response, tool_response


def wait(run):
    deadline=time.monotonic()+15
    while not run.done:
        assert time.monotonic()<deadline, "UI worker did not finish"
        time.sleep(.01)
    return run.snapshot()


def payload(**overrides):
    return {"source":SOURCE,"task":TASK,"mode":"demo","variant":"A0",**overrides}


@pytest.fixture
def app(tmp_path,monkeypatch):
    monkeypatch.setattr(web,"DemoLLM",lambda variant="A0":DemoLLM(delay=0,variant=variant))
    monkeypatch.setattr(web,"evaluate_quality",lambda *args:{"status":"not_measured","reason":"Lifecycle test"})
    application=web.Application(Settings(workspace=tmp_path))
    yield application
    application.close()


def test_demo_runs_real_tools_and_final_verification(app):
    run=app.start(payload());data=wait(run)
    assert data['result']['validation']['passed']
    assert '5 passed' in data['result']['validation']['content']
    assert data['result']['tool_calls']==3 and data['result']['turns']==4
    assert run.file('solution.py')==SOURCE
    assert 'test_single_point_interval' in run.file('test_solution.py')
    assert [e['name'] for e in data['events'] if e['type']=='tool_call_start']==['read_file','write_file','run_command']
    assert data['events'][-1]['type']=='evaluation_end'
    assert run.snapshot(data['next'])['events']==[]
    time.sleep(.02)
    assert run.snapshot()['elapsed_sec']==data['elapsed_sec']


@pytest.mark.parametrize('changes',[
    {'source':SOURCE+'# edited'}, {'task':'another task'}, {'variant':'A5'},
    {'mode':'invalid'}, {'source':32_001*'x'}, {'task':4_001*'x'},
])
def test_invalid_or_custom_scripted_requests_rejected(app,changes):
    with pytest.raises(web.RequestError):app.start(payload(**changes))
    assert not app.runs


def test_real_mode_requires_credentials_without_mock_fallback(app):
    with pytest.raises(web.RequestError,match='真实模型未配置'):
        app.start(payload(mode='real'))
    assert not app.runs


def scripted_real(app,monkeypatch,responses):
    app.settings.api_key='private-demo-credential-123456'
    app.settings.base_url='https://example.invalid/v1'
    app.settings.model='test-model'
    original=web.build_agent
    def factory(*args,**kwargs):
        agent,store,description=original(*args,**kwargs)
        agent.llm=ScriptedLLM(responses)
        return agent,store,description
    monkeypatch.setattr(web,'build_agent',factory)


def test_no_generated_test_file_is_not_reported_as_success(app,monkeypatch):
    scripted_real(app,monkeypatch,[text_response('done without producing a file')])
    result=wait(app.start(payload(mode='real')))['result']
    assert result['status']=='completed' and not result['validation']['passed']
    assert '未生成' in result['validation']['content']


def test_test_failures_keep_actual_output(app,monkeypatch):
    scripted_real(app,monkeypatch,[tool_response(('write_file',{'path':'test_solution.py','content':'def test_failure():\n    assert False\n'})),text_response('done')])
    result=wait(app.start(payload(mode='real')))['result']
    assert not result['validation']['passed']
    assert '1 failed' in result['validation']['content']


@pytest.mark.parametrize('when',['agent','pytest'])
def test_source_rewrite_is_restored_and_rejected(app,monkeypatch,when):
    if when=='agent':
        responses=[tool_response(('write_file',{'path':'solution.py','content':'# altered','overwrite':True})),text_response('done')]
    else:
        tests="from pathlib import Path\nPath('solution.py').write_text('# altered')\ndef test_trivial():\n    assert True\n"
        responses=[tool_response(('write_file',{'path':'test_solution.py','content':tests})),text_response('done')]
    scripted_real(app,monkeypatch,responses)
    run=app.start(payload(mode='real'));data=wait(run)
    assert not data['result']['validation']['passed']
    assert not data['result']['validation']['source_unchanged']
    assert (run.workspace/'solution.py').read_text()==SOURCE


def test_busy_run_and_cooperative_stop(app,monkeypatch):
    entered,release=threading.Event(),threading.Event()
    class Blocking:
        def chat(self,messages,tools=None):
            entered.set();assert release.wait(5)
            return LLMResponse(content='finished request')
    monkeypatch.setattr(web,'DemoLLM',lambda **kwargs:Blocking())
    run=app.start(payload())
    try:
        assert entered.wait(3)
        with pytest.raises(web.RequestError) as error:app.start(payload())
        assert error.value.status==409
        run.cancel()
        assert not run.done  # In-flight request is not falsely shown as terminated.
    finally:
        release.set()
    result=wait(run)['result']
    assert result['status']=='aborted' and not result['validation']['passed']


def test_secrets_redacted_and_file_allowlist_enforced(app):
    app.settings.api_key='private-demo-credential-123456'
    run=web.Run(app.settings,SOURCE,TASK,'demo','A0')
    try:
        run.emit({'type':'tool_call_end','content':app.settings.api_key})
        assert app.settings.api_key not in json.dumps(run.snapshot())
        with pytest.raises(web.RequestError):run.file('../.env')
        secret=run.workspace/'outside.txt';secret.write_text(app.settings.api_key)
        (run.workspace/'test_solution.py').symlink_to(secret)
        assert app.settings.api_key not in run.file('test_solution.py')
        (run.workspace/'test_solution.py').unlink()
        (run.workspace/'test_solution.py').symlink_to(Path(__file__))
        with pytest.raises(web.RequestError):run.file('test_solution.py')
    finally:run.directory.cleanup()


@pytest.fixture
def http(app):
    server=web.create_server(app.settings,0);server.app=app
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    yield 'http://127.0.0.1:'+str(server.server_address[1]),app
    server.shutdown();thread.join();server.server_close()


def request(url,data=None,headers=None):
    req=urllib.request.Request(url,data=data,headers=headers or {})
    try:
        opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        with opener.open(req,timeout=5) as response:return response.status,response.read()
    except urllib.error.HTTPError as exc:return exc.code,exc.read()


def test_http_page_poll_resume_and_download(http):
    url,app=http
    status,html=request(url+'/')
    assert status==200 and b'<title>Kytest' in html
    status,body=request(url+'/api/config')
    assert not json.loads(body)['real_configured'] and 'api_key' not in body.decode()
    status,body=request(url+'/api/runs',json.dumps(payload()).encode(),{'Content-Type':'application/json'})
    assert status==202
    run_id=json.loads(body)['id'];wait(app.get(run_id))
    _,body=request(url+'/api/config');assert json.loads(body)['latest_run']==run_id
    status,body=request(url+'/api/runs/'+run_id);assert status==200 and json.loads(body)['done']
    status,body=request(url+'/api/runs/'+run_id+'/files/test_solution.py')
    assert status==200 and b'test_inclusive_bounds' in body
    assert request(url+'/api/runs/'+run_id+'/files/.env')[0]==404


@pytest.mark.parametrize('path,body,headers,expected',[
    ('/api/config',None,{'Host':'attacker.example'},403),
    ('/api/config',None,{'Origin':'https://attacker.example'},403),
    ('/api/runs',b'{}',{'Content-Type':'text/plain'},415),
    ('/api/runs',b'[]',{'Content-Type':'application/json'},400),
    ('/api/runs',b'{broken',{'Content-Type':'application/json'},400),
    ('/api/runs',b'{}',{'Content-Type':'application/json','Origin':'null'},403),
    ('/api/runs/unknown?after=no',None,{},400),
    ('/api/runs/unknown?after=-1',None,{},400),
    ('/api/runs/unknown',None,{},404),
])
def test_http_rejects_cross_site_and_malformed_requests(http,path,body,headers,expected):
    url,_=http
    status,result=request(url+path,body,headers)
    assert status==expected and 'error' in json.loads(result)


def test_a4_uses_actual_candidate_validator_and_same_final_cases(app):
    run=app.start(payload(variant='A4'));data=wait(run)
    assert data['result']['validation']['passed']
    assert '5 passed' in data['result']['validation']['content']
    assert data['result']['turns']==5 and data['result']['tool_calls']==4
    report=data['report']
    assert len(report['accepted'])==5 and len(report['attempts'])==7
    assert [a['status'] for a in report['attempts']]==['ACCEPTED']*3+['FAIL','REJECTED','ACCEPTED','ACCEPTED']
    assert 'contract_quote' in report['attempts'][4]['diagnostic']
    assert 'submit_tests' in next(e for e in data['events'] if e['type']=='run_start')['tools']
    assert 'test_single_point_interval' in run.file('test_solution.py')
    assert run.file('solution.py')==SOURCE


def wait_comparison(app,comparison_id):
    for run_id in app.comparisons[comparison_id]:
        wait(app.get(run_id))
    return app.comparison(comparison_id)


def test_comparison_freezes_identical_input_and_separate_workspaces(app):
    comparison_id=app.compare(payload())
    pair=wait_comparison(app,comparison_id)['runs']
    a0,a4=pair
    assert a0['variant']=='A0' and a4['variant']=='A4'
    assert a0['source_sha256']==a4['source_sha256']
    assert a0['source']==a4['source']==SOURCE and a0['task']==a4['task']==TASK
    assert a0['mode']==a4['mode']=='demo'
    assert a0['report'] is None and len(a4['report']['accepted'])==5
    assert all(run['result']['validation']['passed'] for run in pair)
    assert app.get(a0['id']).workspace!=app.get(a4['id']).workspace
    assert app.get(a0['id']).started < app.get(a4['id']).finished
    assert app.get(a4['id']).started < app.get(a0['id']).finished
    assert all(app.get(run['id']).settings.max_steps==app.settings.max_steps for run in pair)
    assert app.comparison(comparison_id,a0['next'],a4['next'])['runs'][0]['events']==[]


def test_comparison_requests_overlap_and_stop_cancels_both(app,monkeypatch):
    both_entered,release=threading.Event(),threading.Event();calls=[];lock=threading.Lock()
    class Blocking:
        def __init__(self,variant):self.variant=variant
        def chat(self,messages,tools=None):
            with lock:
                calls.append(self.variant)
                if len(calls)==2:both_entered.set()
            assert release.wait(5)
            return LLMResponse(content='finished request')
    monkeypatch.setattr(web,'DemoLLM',Blocking)
    comparison_id=app.compare(payload())
    try:
        assert both_entered.wait(3),'A4 must enter its request before A0 is released'
        assert all(run['phase']=='running' for run in app.comparison(comparison_id)['runs'])
        with pytest.raises(web.RequestError):app.start(payload())
        with pytest.raises(web.RequestError):app.compare(payload())
        app.stop_comparison(comparison_id)
    finally:release.set()
    pair=wait_comparison(app,comparison_id)['runs']
    assert all(run['result']['status']=='aborted' for run in pair)
    assert set(calls)=={'A0','A4'} and len(calls)==2


def test_http_comparison_resume_download_and_bad_cursor(http):
    url,app=http
    status,body=request(url+'/api/comparisons',json.dumps(payload()).encode(),{'Content-Type':'application/json'})
    assert status==202
    comparison_id=json.loads(body)['id'];pair=wait_comparison(app,comparison_id)['runs']
    _,body=request(url+'/api/config');assert json.loads(body)['latest_comparison']==comparison_id
    status,body=request(url+'/api/comparisons/'+comparison_id)
    assert status==200 and json.loads(body)['done']
    assert json.loads(body)['runs'][1]['report']['attempts'][4]['status']=='REJECTED'
    status,body=request(url+'/api/runs/'+pair[1]['id']+'/files/testgen_report.json')
    assert status==200 and len(json.loads(body)['accepted'])==5
    assert request(url+'/api/comparisons/'+comparison_id+'?after_a0=-1')[0]==400
    assert request(url+'/api/comparisons/unknown')[0]==404


def test_pruning_does_not_leave_partial_comparison(app,monkeypatch):
    def fast(self):
        self.done=True;self.phase='done';self.finished=time.monotonic()
    monkeypatch.setattr(web.Run,'execute',fast)
    comparison_id=app.compare(payload());wait_comparison(app,comparison_id)
    for _ in range(7):wait(app.start(payload()))
    with pytest.raises(web.RequestError):app.comparison(comparison_id)
    assert len(app.runs)==8


@pytest.mark.parametrize('test_code,killed',[
    ('from solution import classify\ndef test_inside_only():\n    assert classify(5, 2, 8) == 0\n',1),
    (TESTS,5),
])
def test_quality_distinguishes_weak_and_strong_passing_suites(tmp_path,test_code,killed):
    report=evaluate_quality(Settings(workspace=tmp_path,max_exec_timeout=15),SOURCE,
        lambda _:test_code,{'passed':True,'source_unchanged':True},threading.Event(),lambda _:None)
    assert report['status']=='measured',report
    faults=report['fault_detection'];assert faults['total']==5 and faults['confirmed_killed']==killed
    assert faults['percent']==20*killed and faults['uncertain']==0
    assert report['coverage']['status']=='measured'
    assert report['coverage']['branch_percent']==(50 if killed==1 else 100)
    assert sum(item['status']=='SURVIVED' for item in faults['results'])==5-killed


def test_failed_reference_blocks_quality_and_custom_source_has_no_fault_score(tmp_path):
    report=evaluate_quality(Settings(workspace=tmp_path),'def f():\n    return 1\n',
        lambda _: 'def test_ok():\n    from solution import f\n    assert f()==1\n',
        {'passed':True,'source_unchanged':True},threading.Event(),lambda _:None)
    assert report['coverage']['line_percent']==100
    assert report['fault_detection']['status']=='not_applicable'
    assert report['fault_detection']['percent'] is None and report['fault_detection']['total'] is None
    blocked=evaluate_quality(Settings(workspace=tmp_path),SOURCE,lambda _:pytest.fail('Must not read or execute'),
        {'passed':False,'source_unchanged':True},threading.Event(),lambda _:None)
    assert blocked['status']=='blocked' and blocked['fault_detection']['percent'] is None


def test_only_skipped_tests_are_not_a_valid_suite(app,monkeypatch):
    code='import pytest\n@pytest.mark.skip(reason="no executed assertion")\ndef test_skip():\n    assert True\n'
    scripted_real(app,monkeypatch,[tool_response(('write_file',{'path':'test_solution.py','content':code})),text_response('done')])
    result=wait(app.start(payload(mode='real')))['result']
    assert not result['validation']['passed'] and result['validation']['counts']['skipped']==1


def test_pytest_counts_use_final_summary_instead_of_model_claims():
    assert pytest_counts('Claims: 90 passed\n1 failed, 2 passed in 0.01s\n')['failed']==1
    assert pytest_counts('5 skipped in 0.02s')['passed']==0


def test_quality_does_not_score_timeout_or_abnormal_exit_with_failure_output(tmp_path,monkeypatch):
    from code_agent.tools.base import ToolResult
    from code_agent.web import quality
    original=quality.RunCommandTool.run
    for header in ('已超时并被终止','退出码 2'):
        def interrupted(tool,command,**kwargs):
            if command=='python -m pytest test_solution.py -q':
                return ToolResult.failure('$ '+command+'\n['+header+'｜耗时 5s｜超时上限 5s]\n1 failed in 0.01s')
            return original(tool,command,**kwargs)
        monkeypatch.setattr(quality.RunCommandTool,'run',interrupted)
        report=quality.evaluate_quality(Settings(workspace=tmp_path),SOURCE,lambda _:TESTS,
            {'passed':True,'source_unchanged':True},threading.Event(),lambda _:None)
        faults=report['fault_detection']
        assert faults['confirmed_killed']==0 and faults['uncertain']==5
        assert faults['percent'] is None
        assert all(item['status']=='UNCERTAIN' for item in faults['results'])


def test_rotation_quality_reproduces_saved_real_suite_and_keeps_full_pool(tmp_path):
    from code_agent.web.examples import ROTATION_SOURCE
    receipt=json.loads((Path(web.__file__).resolve().parents[3]/'submission/evidence/ui-rotation.json').read_text())
    saved=receipt['comparison']['runs'][1]
    report=evaluate_quality(Settings(workspace=tmp_path),ROTATION_SOURCE,
        lambda _:saved['saved_tests'],{'passed':True,'source_unchanged':True},threading.Event(),lambda _:None)
    faults=report['fault_detection']
    assert faults['profile']=='mbpp-304-ror-lcr-bcr-v2' and faults['total']==4
    assert faults['confirmed_killed']==3 and faults['percent']==75
    assert faults['uncertain']==0 and faults['results'][2]['status']=='SURVIVED'
    assert report['test_sha256']==saved['result']['quality']['test_sha256']


def test_saved_real_case_is_available_without_key_and_does_not_start_agents(http):
    import hashlib
    url,application=http
    _,body=request(url+'/api/config');config=json.loads(body)
    assert [e['id'] for e in config['examples']]==['rotation','classify']
    status,body=request(url+'/api/examples/rotation-record');saved=json.loads(body)
    assert status==200 and saved['origin']['kind']=='saved_real' and saved['done']
    a0,a4=saved['runs']
    assert a0['result']['validation']['counts']['failed']==6
    assert a4['result']['validation']['passed'] and a4['result']['quality']['fault_detection']['percent']==75
    assert a0['source_sha256']==a4['source_sha256'] and a0['task']==a4['task']
    assert hashlib.sha256(a4['saved_tests'].encode()).hexdigest()==a4['result']['quality']['test_sha256']
    assert not application.runs


def test_web_preserves_configured_model_request_timeout(tmp_path,monkeypatch):
    from types import SimpleNamespace
    monkeypatch.setattr('sys.argv',['web.py'])
    settings=Settings(workspace=tmp_path,request_timeout=87)
    monkeypatch.setattr(web.Settings,'from_env',lambda **kwargs:settings)
    captured=[]
    def interrupted():raise KeyboardInterrupt
    def factory(chosen,port):
        captured.append(chosen)
        return SimpleNamespace(server_address=('127.0.0.1',port),serve_forever=interrupted,
                               app=SimpleNamespace(close=lambda:None),server_close=lambda:None)
    monkeypatch.setattr(web,'create_server',factory)
    web.main()
    assert captured[0].request_timeout==87
    assert captured[0].max_steps==12 and captured[0].max_total_tokens==30000
