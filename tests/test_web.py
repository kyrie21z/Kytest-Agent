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
from code_agent.web.demo import DemoLLM, SOURCE, TASK
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
    monkeypatch.setattr(web,"DemoLLM",lambda:DemoLLM(delay=0))
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
    assert data['events'][-1]['type']=='validation_end'
    assert run.snapshot(data['next'])['events']==[]
    time.sleep(.02)
    assert run.snapshot()['elapsed_sec']==data['elapsed_sec']


@pytest.mark.parametrize('changes',[
    {'source':SOURCE+'# edited'}, {'task':'another task'}, {'variant':'A4'},
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
    monkeypatch.setattr(web,'DemoLLM',Blocking)
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
