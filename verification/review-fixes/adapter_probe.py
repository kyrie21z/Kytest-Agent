"""Exercise the HTTP adapter against a local synthetic service, never a real model."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else ROOT / 'code-agent'
sys.path.insert(0, str(REPO / 'src'))
from code_agent.agent import Agent
from code_agent.errors import LLMError
from code_agent.llm import OpenAICompatibleLLM
from code_agent.config import Settings
from code_agent.tools.factories import build_registry

seen = []
mode = 'tools'
counter = 0


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        global counter
        payload = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        seen.append({'mode': mode, 'path': self.path, 'payload': payload})
        counter += 1
        if mode == 'auth':
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b'{"error":"review synthetic auth failure"}')
            return
        if mode == 'retry' and counter == 1:
            self.send_response(429)
            self.send_header('Retry-After', '0')
            self.end_headers()
            self.wfile.write(b'{"error":"review synthetic rate limit"}')
            return
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        if mode == 'tools' and not any(m['role'] == 'tool' for m in payload['messages']):
            message = {'role': 'assistant', 'content': 'review scripted read', 'tool_calls': [{
                'id': 'review-call-1', 'type': 'function',
                'function': {'name': 'read_file', 'arguments': '{"path":"solution.py"}'},
            }]}
            finish = 'tool_calls'
        else:
            message = {'role': 'assistant', 'content': 'review synthetic response'}
            finish = 'stop'
        self.wfile.write(json.dumps({'choices': [{'message': message, 'finish_reason': finish}],
                                    'usage': {'prompt_tokens': 100, 'completion_tokens': 20, 'total_tokens': 120}}).encode())


server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
checks = {'kind': 'local_synthetic_http_service_not_a_real_model', 'external_network_requests': 0}

try:
    client = OpenAICompatibleLLM('review-dummy-key', f'http://127.0.0.1:{server.server_port}/v1',
                                 'review-synthetic-model', timeout=2, max_retries=1)
    with tempfile.TemporaryDirectory(prefix='review-http-') as raw:
        workspace = Path(raw)
        (workspace / 'solution.py').write_text('def add(a,b):\n    return a+b\n')
        agent = Agent(llm=client, tools=build_registry(Settings(workspace=workspace)),
                      system_prompt='review adapter integration probe')
        agent.state.add_user('Read solution.py')
        result = agent.run()
        checks['function_call_roundtrip'] = {
            'status': result.status, 'llm_calls': result.llm_calls, 'tool_calls': result.tool_calls,
            'tool_result_sent_in_next_request': any(m['role']=='tool' and 'def add' in m['content'] for m in seen[-1]['payload']['messages']),
            'request_path': seen[0]['path'],
        }
    mode, counter = 'retry', 0
    response = client.chat([{'role': 'user', 'content': 'review retry'}])
    checks['rate_limit_retry'] = {'attempts': counter, 'succeeded': bool(response.content)}
    mode, counter = 'auth', 0
    try:
        client.chat([{'role': 'user', 'content': 'review auth'}])
    except LLMError as exc:
        checks['authentication_failure'] = {'attempts': counter, 'error_type': type(exc).__name__, 'message': str(exc)}
finally:
    server.shutdown()
    server.server_close()
    thread.join(timeout=2)

output = ROOT / 'adapter_probe.json'
output.write_text(json.dumps(checks, ensure_ascii=False, indent=2))
print(json.dumps(checks, ensure_ascii=False, indent=2))
