from __future__ import annotations

import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import time

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'code-agent'
sys.path[:0] = [str(REPO / 'src'), str(REPO)]

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.llm import LLMResponse, ToolCall
from code_agent.message import Usage
from code_agent.proc import run_process
from code_agent.session import SessionStore
from code_agent.tools.base import Tool, ToolRegistry, ToolResult
from code_agent.tools.factories import build_registry
from tests.helpers import ScriptedLLM, FailingLLM, text_response, tool_response

checks = {}


def cli(workspace, args, input_text=None):
    result = subprocess.run(
        [sys.executable, str(REPO / 'main.py'), '-C', str(workspace),
         '--no-env-file', '--mock', *args],
        input=input_text, text=True, capture_output=True, timeout=15,
        cwd=REPO,
    )
    return {'returncode': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}


with tempfile.TemporaryDirectory(prefix='review-probes-') as raw:
    area = Path(raw)
    workspace = area / 'workspace'
    workspace.mkdir()
    (workspace / 'solution.py').write_text('def add(a, b):\n    return a + b\n')
    settings = Settings(workspace=workspace)
    registry = build_registry(settings)

    checks['cli_print'] = cli(workspace, ['--no-session', '--print', '解释 solution.py'])
    checks['cli_json'] = cli(workspace, ['--no-session', '--mode', 'json', '--print', '解释 solution.py'])
    json_events = [json.loads(line) for line in checks['cli_json']['stdout'].splitlines()]
    checks['cli_json']['event_types'] = [event['type'] for event in json_events]
    checks['cli_empty_task'] = cli(workspace, ['--no-session', '--print'])
    checks['cli_unknown_tool'] = cli(workspace, ['--no-session', '--tools', 'unknown', '--print', '解释 solution.py'])
    checks['cli_two_tasks'] = cli(
        workspace, ['--no-session', '--max-turns', '3'],
        '解释 solution.py\n再次解释 solution.py\nexit\n',
    )

    outside = area / 'outside-review-sentinel.txt'
    outside.write_text('review sentinel; created by reviewer')
    rejected = registry.execute('read_file', {'path': '../outside-review-sentinel.txt'})
    command = shlex.join([sys.executable, '-c',
                          f'from pathlib import Path; print(Path({str(outside)!r}).read_text())'])
    allowed = registry.execute('run_command', {'command': command})
    checks['workspace_boundary'] = {
        'file_tool_rejected': not rejected.ok,
        'command_tool_read_outside': allowed.ok and 'review sentinel' in allowed.content,
        'file_result': rejected.content,
    }

    no_write = build_registry(Settings(workspace=workspace, allow_write=False))
    target = workspace / 'command-wrote.txt'
    command = shlex.join([sys.executable, '-c',
                          f'from pathlib import Path; Path({str(target)!r}).write_text("review")'])
    rejected = no_write.execute('write_file', {'path': target.name, 'content': 'review'})
    allowed = no_write.execute('run_command', {'command': command})
    checks['allow_write_false'] = {
        'write_file_rejected': not rejected.ok,
        'command_write_succeeded': allowed.ok and target.exists(),
    }

    target = workspace / 'overwrite-probe.txt'
    target.write_text('original reviewer content')
    result = registry.execute('write_file', {'path': target.name, 'content': 'new reviewer content', 'overwrite': 'false'})
    checks['invalid_boolean_parameter'] = {
        'argument': {'overwrite': 'false'},
        'tool_ok': result.ok,
        'file_was_overwritten': target.read_text() == 'new reviewer content',
        'result': result.content,
    }

    invalid = registry.execute('write_file', {'path': 'x.py'})
    unknown = registry.execute('unknown', {})
    failing = Agent(llm=FailingLLM(), tools=registry, system_prompt='review probe')
    failing.state.add_user('Generate tests')
    failure = failing.run()
    checks['basic_error_paths'] = {
        'missing_required_rejected': not invalid.ok,
        'unknown_tool_rejected': not unknown.ok,
        'llm_failure_status': failure.status,
        'llm_failure_message': failure.error,
    }

    large = workspace / 'large.py'
    large.write_text('x = 1\n' * 40000)
    whole = registry.execute('read_file', {'path': large.name})
    partial = registry.execute('read_file', {'path': large.name, 'start_line': 1, 'end_line': 2})
    checks['oversized_file_feedback'] = {
        'bytes': large.stat().st_size,
        'whole_read_ok': whole.ok,
        'whole_read_message': whole.content,
        'suggested_partial_read_ok': partial.ok,
        'partial_read_message': partial.content,
    }

    timeout_command = shlex.join([sys.executable, '-c', 'import time; time.sleep(3)'])
    timed_out = registry.execute('run_command', {'command': timeout_command, 'timeout': 0.5})
    checks['tool_timeout_feedback'] = {'ok': timed_out.ok, 'content': timed_out.content}

    sink = workspace / 'unwritable-session-sink'
    sink.mkdir()
    bad_store = SessionStore(path=sink)
    returned = bad_store.write({'type': 'review_probe'})
    checks['session_write_failure'] = {
        'target_is_directory': sink.is_dir(),
        'returned_success_shaped_entry': returned == {'type': 'review_probe'},
        'in_memory_entries': len(bad_store.entries),
        'failure_signaled': bool(getattr(bad_store, 'write_errors', 0)),
        'write_errors': getattr(bad_store, 'write_errors', None),
        'last_write_error': getattr(bad_store, 'last_write_error', None),
    }

    fake_key = 'review-dummy-key-not-a-real-credential'
    (workspace / '.env').write_text('LLM_API_KEY=' + fake_key + '\n')
    store = SessionStore.create(workspace / '.sessions')
    agent = Agent(
        llm=ScriptedLLM([tool_response(('read_file', {'path': '.env'})), text_response('done')]),
        tools=registry, system_prompt='review probe', on_event=store.record_event,
    )
    agent.state.add_user('Read a reviewer-created configuration fixture')
    agent.run()
    checks['session_redaction'] = {
        'dummy_credential_logged_in_plaintext': fake_key in store.path.read_text(),
        'fixture_contains_no_real_credential': True,
    }

    prior = os.environ.get('REVIEW_DUMMY_SECRET')
    os.environ['REVIEW_DUMMY_SECRET'] = fake_key
    try:
        command = shlex.join([sys.executable, '-c', 'import os; print(os.environ.get("REVIEW_DUMMY_SECRET"))'])
        result = registry.execute('run_command', {'command': command})
        checks['child_environment'] = {'dummy_secret_inherited': result.ok and fake_key in result.content}
    finally:
        if prior is None:
            os.environ.pop('REVIEW_DUMMY_SECRET', None)
        else:
            os.environ['REVIEW_DUMMY_SECRET'] = prior

    raw_output = run_process(
        [sys.executable, '-c', 'print("x" * 700000)'],
        cwd=workspace, timeout=3, output_char_cap=400000,
    )
    checks['output_capture_limit'] = {
        'exit_code': raw_output.exit_code,
        'captured_bytes': len(raw_output.stdout.encode()),
        'declared_shell_limit_chars': 400000,
        'output_truncated': raw_output.output_truncated,
        'exceeds_declared_limit': len(raw_output.stdout) + len(raw_output.stderr) > 400000,
    }

    class SlowScripted(ScriptedLLM):
        def chat(self, messages, tools=None):
            time.sleep(0.15)
            return super().chat(messages, tools)

    agent = Agent(
        llm=SlowScripted([
            tool_response(('write_file', {'path': 'never.py', 'content': 'pass'}), finish_reason='length'),
            text_response('done'),
        ]), tools=registry, system_prompt='review probe',
    )
    agent.state.add_user('truncation probe')
    start = time.monotonic()
    result = agent.run()
    elapsed = time.monotonic() - start
    checks['truncated_output_runtime'] = {
        'wall_clock_sec': round(elapsed, 4),
        'reported_runtime_sec': round(result.runtime_sec, 4),
        'truncated_tool_was_not_executed': not (workspace / 'never.py').exists(),
    }

    class StopTool(Tool):
        name = 'stop_probe'
        parameters = {'type': 'object', 'properties': {}}
        def run(self):
            return ToolResult.success('done', terminate=True)

    stop_registry = ToolRegistry()
    stop_registry.register(StopTool(workspace))
    result = stop_registry.execute('stop_probe', {})
    checks['registry_terminate_flag'] = {'expected_terminate': True, 'actual_terminate': result.terminate}

    raw_usage = {'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120,
                 'prompt_tokens_details': {'cached_tokens': 80}}
    usage = Usage.from_openai(raw_usage)
    checks['token_usage'] = {'input_fixture': raw_usage, 'parsed_usage': usage.to_dict()}

path = ROOT / 'independent_checks.json'
path.write_text(json.dumps(checks, ensure_ascii=False, indent=2))
for key, value in checks.items():
    if key.startswith('cli_'):
        print(key, 'exit', value['returncode'], 'stderr', value['stderr'][-650:].replace('\n', ' | '))
    else:
        print(key, json.dumps(value, ensure_ascii=False))
print('SAVED', path)
