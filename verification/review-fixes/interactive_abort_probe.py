"""Reproduce Ctrl-C followed by a new CLI task using a local synthetic HTTP server."""
from __future__ import annotations

from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import threading

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
requested = threading.Event()
allow_response = threading.Event()
cancelled_visible = threading.Event()
requests = []


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass

    def do_POST(self):
        payload = json.loads(self.rfile.read(int(self.headers["Content-Length"])))
        requests.append(payload)
        requested.set()
        if not allow_response.wait(10):
            return
        response = {
            "choices": [{"message": {"role": "assistant", "content": "synthetic response"},
                         "finish_reason": "stop"}],
            "usage": {"prompt_tokens": 10, "completion_tokens": 2, "total_tokens": 12},
        }
        try:
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
        except (BrokenPipeError, ConnectionResetError):
            pass


server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
server.daemon_threads = True
thread = threading.Thread(target=server.serve_forever, daemon=True)
thread.start()
stderr_lines = []
process = None

try:
    with tempfile.TemporaryDirectory(prefix="rereview-abort-cli-") as raw:
        env = dict(os.environ)
        env.update({"LLM_API_KEY": "review-fake-key-no-real-credential",
                    "LLM_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1",
                    "LLM_MODEL": "review-synthetic-model", "PYTHONUNBUFFERED": "1"})
        process = subprocess.Popen([
            sys.executable, str(REPO / "main.py"), "-C", raw,
            "--no-env-file", "--no-session",
        ], cwd=REPO, env=env, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
            stderr=subprocess.PIPE, text=True, encoding="utf-8", start_new_session=True)
        stdout_parts = []

        def read_stdout():
            stdout_parts.append(process.stdout.read())

        def read_stderr():
            for line in process.stderr:
                stderr_lines.append(line)
                if "[aborted]" in line:
                    cancelled_visible.set()

        readers = [threading.Thread(target=read_stdout, daemon=True),
                   threading.Thread(target=read_stderr, daemon=True)]
        for reader in readers:
            reader.start()
        process.stdin.write("first task\n")
        process.stdin.flush()
        if not requested.wait(5):
            raise RuntimeError("CLI did not contact synthetic service")
        process.send_signal(signal.SIGINT)
        if not cancelled_visible.wait(5):
            raise RuntimeError("CLI did not report cancellation")
        allow_response.set()
        process.stdin.write("new task after cancellation\nexit\n")
        process.stdin.flush()
        process.stdin.close()
        returncode = process.wait(timeout=10)
        for reader in readers:
            reader.join(timeout=2)
        result = {
            "kind": "CLI signal integration with local synthetic HTTP service",
            "external_model_requests": 0,
            "returncode": returncode,
            "http_requests": len(requests),
            "stderr": "".join(stderr_lines),
            "stdout": "".join(stdout_parts),
            "both_tasks_aborted_without_new_model_call": len(requests) == 1
                and sum("[aborted]" in line for line in stderr_lines) == 2,
        }
finally:
    allow_response.set()
    if process is not None and process.poll() is None:
        process.kill()
        process.wait(timeout=5)
    server.shutdown()
    server.server_close()

(ROOT / "interactive_abort_probe.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(result, ensure_ascii=False, indent=2))
