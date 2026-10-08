"""复评剩余问题的行为验收；所有凭据、外部文件和模型响应均为模拟。"""
from __future__ import annotations

import json
import math
import shlex
import shutil
import sys
import tracemalloc
from pathlib import Path

import pytest

from code_agent.agent import Agent, TurnDecision
from code_agent.config import Settings
from code_agent.proc import run_process
from code_agent.session import SessionStore
from code_agent.tools.file_tools import ReadFileTool
from code_agent.tools.shell_tools import RunCommandTool
from scripts import analyze_ablation as analysis
from .helpers import RecordingTool, ScriptedLLM, StubRegistry, text_response, tool_response


def test_cancelled_task_keeps_history_and_next_task_runs():
    llm = ScriptedLLM([text_response("next task completed")])
    agent = Agent(llm=llm, tools=StubRegistry(), system_prompt="test", max_turns=1)
    agent.state.add_user("first task")
    agent.begin_task()
    agent.abort()
    assert agent.run().status == "aborted"
    agent.state.add_user("next task")
    agent.begin_task()
    result = agent.run()
    assert result.status == "completed" and result.turns == 1
    assert any(m.get("content") == "first task" for m in llm.requests[0])


@pytest.mark.skipif(sys.platform == "win32", reason="真实 SIGINT 联调使用 POSIX 信号")
def test_cli_sigint_then_new_task_makes_a_second_http_request(tmp_path):
    import os
    import signal
    import subprocess
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    requested, release, cancelled = threading.Event(), threading.Event(), threading.Event()
    requests, errors, output = [], [], []
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            requested.set()
            if not release.wait(10):
                return
            body = json.dumps({"choices": [{"message": {"role": "assistant", "content": "completed"},
                                             "finish_reason": "stop"}],
                               "usage": {"prompt_tokens": 10, "completion_tokens": 2}}).encode()
            try:
                self.send_response(200)
                self.end_headers()
                self.wfile.write(body)
            except (BrokenPipeError, ConnectionResetError):
                pass

    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = os.environ.copy()
    env.update({"LLM_API_KEY": "signal-fixture", "LLM_MODEL": "synthetic-model",
                "LLM_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1", "PYTHONUNBUFFERED": "1"})
    process = subprocess.Popen(
        [sys.executable, str(Path(__file__).resolve().parents[1] / "main.py"),
         "-C", str(tmp_path), "--no-env-file", "--no-session"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        text=True, encoding="utf-8", env=env, start_new_session=True,
    )
    def read_errors():
        for line in process.stderr:
            errors.append(line)
            if "[aborted]" in line:
                cancelled.set()
    readers = [threading.Thread(target=read_errors, daemon=True),
               threading.Thread(target=lambda: output.append(process.stdout.read()), daemon=True)]
    for reader in readers:
        reader.start()
    try:
        process.stdin.write("first task\n")
        process.stdin.flush()
        assert requested.wait(5), "CLI 没有联系本地合成服务"
        process.send_signal(signal.SIGINT)
        assert cancelled.wait(5), "CLI 没有报告取消"
        release.set()
        process.stdin.write("next task\nexit\n")
        process.stdin.flush()
        process.stdin.close()
        assert process.wait(timeout=10) == 0
        for reader in readers:
            reader.join(timeout=2)
        assert len(requests) == 2
        assert "[completed] turns=1" in "".join(errors)
        assert sum("[aborted]" in line for line in errors) == 1
    finally:
        release.set()
        if process.poll() is None:
            process.kill()
            process.wait(timeout=5)
        server.shutdown()
        server.server_close()


@pytest.mark.parametrize("budget", ["turns", "llm_calls", "tokens"])
def test_checkpoint_cannot_refresh_task_budget(budget):
    options = {"max_turns": 2 if budget == "turns" else 10,
               "max_llm_calls": 2 if budget == "llm_calls" else 10,
               "max_total_tokens": 120 if budget == "tokens" else 0}
    agent = Agent(llm=ScriptedLLM([text_response("continue")] * 6), tools=StubRegistry(),
                  system_prompt="test", finish_turn=lambda *_: TurnDecision(continue_=True), **options)
    agent.begin_task()
    assert agent.run_until(1).turns == 1
    assert agent.run_until(2).turns == 1
    assert agent.run().turns == 0
    agent.begin_task()
    assert agent.run().turns == 2


def test_interrupted_tool_batch_is_balanced_without_executing_remaining_calls():
    def interrupt(**kwargs):
        raise KeyboardInterrupt()
    registry = StubRegistry([RecordingTool("interrupt", interrupt), RecordingTool("side_effect")])
    llm = ScriptedLLM([
        tool_response(("cancel-1", "interrupt", {}), ("cancel-2", "side_effect", {})),
        text_response("new task completed"),
    ])
    agent = Agent(llm=llm, tools=registry, system_prompt="test")
    agent.begin_task()
    result = agent.run()
    assert result.status == "aborted"
    assert [name for name, _ in registry.executed] == ["interrupt"]
    assert agent.state.pending_tool_calls() == []
    responses = [m for m in agent.state.messages if m["role"] == "tool"]
    assert [m["tool_call_id"] for m in responses] == ["cancel-1", "cancel-2"]
    assert result.tool_calls_skipped == 1
    agent.state.add_user("new task")
    agent.begin_task()
    assert agent.run().status == "completed"
    sent = llm.requests[-1]
    assert all(any(m.get("tool_call_id") == call["id"] for m in sent)
               for m in sent for call in m.get("tool_calls", []))


@pytest.mark.parametrize("text", [
    'LLM_API_KEY=fixture-secret-without-prefix',
    'SERVICE_ACCESS_TOKEN="fixture-secret-without-prefix"',
    '1| {"password": "fixture-secret-without-prefix"}',
    '2| {"accessToken": "fixture-secret-without-prefix"}',
    'AWS_SECRET_ACCESS_KEY=fixture-secret-without-prefix',
    'Authorization: Bearer fixture-secret-without-prefix',
    'password="fixture secret with spaces"',
])
def test_persisted_credentials_are_redacted(tmp_path, text):
    store = SessionStore.create(tmp_path)
    store.write({"type": "tool_result", "name": "read_file", "content": text,
                 "turn": 7, "total_tokens": 120})
    raw = store.path.read_text()
    assert "fixture" not in raw
    persisted = json.loads(raw)
    assert persisted["name"] == "read_file" and persisted["turn"] == 7
    assert persisted["total_tokens"] == 120 and "REDACTED" in raw


def test_structured_credentials_and_tool_arguments_keep_event_structure(tmp_path):
    store = SessionStore.create(tmp_path, secrets=("configured-fixture-value",))
    store.write({"type": "tool_call", "arguments": {
        "credentials": ["list-fixture", {"nested": "nested-fixture"}],
        "db_password": "pass-fixture", "apiKey": "api-fixture", "token": 123456789,
        "path": "ordinary.json", "max_tokens": 1024,
        "content": '{"password": "json-fixture", "normal": "visible"}',
    }, "content": "configured-fixture-value", "total_tokens": 10})
    raw = store.path.read_text()
    assert "fixture" not in raw and "123456789" not in raw
    row = json.loads(raw)
    assert row["type"] == "tool_call" and row["total_tokens"] == 10
    assert row["arguments"]["path"] == "ordinary.json"
    assert row["arguments"]["max_tokens"] == 1024
    assert json.loads(row["arguments"]["content"])["normal"] == "visible"


@pytest.fixture()
def sandbox_workspace(tmp_path):
    if sys.platform != "linux" or not shutil.which("bwrap"):
        pytest.skip("文件隔离的实际执行需要 Linux Bubblewrap")
    root = tmp_path / "workspace"
    root.mkdir()
    return root


def command(code):
    return shlex.join([sys.executable, "-c", code])


def test_sandbox_cannot_read_external_file_or_follow_escape_symlink(sandbox_workspace):
    outside = sandbox_workspace.parent / "sentinel.txt"
    outside.write_text("outside-fixture")
    (sandbox_workspace / "escape").symlink_to(outside)
    tool = RunCommandTool(Settings(workspace=sandbox_workspace))
    for path in (str(outside), "escape"):
        result = tool.run(command(f"from pathlib import Path; print(Path({path!r}).read_text())"))
        assert not result.ok and "outside-fixture" not in result.content
    result = tool.run(command("from pathlib import Path; Path('result').write_text('ok'); print('written')"))
    assert result.ok and (sandbox_workspace / "result").read_text() == "ok"


def test_readonly_sandbox_denies_command_writes(sandbox_workspace):
    tool = RunCommandTool(Settings(workspace=sandbox_workspace, allow_write=False))
    result = tool.run(command("from pathlib import Path; Path('result').write_text('unexpected')"))
    assert not result.ok and not (sandbox_workspace / "result").exists()
    assert tool.run(command("print('read-only command works')")).ok


def test_workspace_relative_executable_runs_in_the_selected_directory(sandbox_workspace):
    path = sandbox_workspace / "local-script"
    path.write_text(f"#!{sys.executable}\nprint('workspace executable works')\n")
    path.chmod(0o700)
    result = RunCommandTool(Settings(workspace=sandbox_workspace)).run("./local-script")
    assert result.ok and "workspace executable works" in result.content


def test_sandbox_blocks_network_and_secret_environment(sandbox_workspace, monkeypatch):
    monkeypatch.setenv("LLM_API_KEY", "environment-fixture")
    tool = RunCommandTool(Settings(workspace=sandbox_workspace))
    result = tool.run(command("import os; print(os.environ.get('LLM_API_KEY', 'CLEAN'))"))
    assert result.ok and "CLEAN" in result.content and "environment-fixture" not in result.content
    result = tool.run(command("import socket; socket.create_connection(('1.1.1.1', 80), timeout=1)"))
    assert not result.ok


def test_sandbox_unavailable_fails_closed(tmp_path, monkeypatch):
    from code_agent import sandbox
    original = sandbox.shutil.which
    monkeypatch.setattr(sandbox.shutil, "which", lambda name, **kwargs: None if name == "bwrap" else original(name, **kwargs))
    result = RunCommandTool(Settings(workspace=tmp_path)).run("python -c pass")
    assert not result.ok and "命令隔离不可用" in result.content
    assert not (tmp_path / "result").exists()


def test_trusted_mode_requires_writable_policy(tmp_path):
    tool = RunCommandTool(Settings(workspace=tmp_path, execution_mode="trusted", allow_write=False))
    assert not tool.run(command("print('must not execute')")).ok


def test_unterminated_output_allocation_is_bounded(tmp_path):
    tracemalloc.start()
    try:
        result = run_process([sys.executable, "-c", "import sys; sys.stdout.write('x' * (16 * 1024 * 1024))"],
                             cwd=tmp_path, timeout=15, output_char_cap=1000)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert result.ok and result.output_truncated
    assert len(result.stdout) + len(result.stderr) <= 1000
    # 足以区分有界读取与整条16MiB行分配；不约束子进程内存或RSS。
    assert peak < 4 * 1024 * 1024


def test_large_file_long_lines_are_bounded_and_line_numbers_remain_correct(tmp_path):
    path = tmp_path / "large.txt"
    with path.open("w") as stream:
        for _ in range(128):
            stream.write("x" * 65536)
        stream.write("\nsecond line\n")
    reader = ReadFileTool(Settings(workspace=tmp_path, max_file_bytes=1000))
    tracemalloc.start()
    try:
        result = reader.run("large.txt", start_line=1, end_line=2)
        _, peak = tracemalloc.get_traced_memory()
    finally:
        tracemalloc.stop()
    assert result.ok and "本行过长已截断" in result.content
    assert "2| second line" in result.content and len(result.content) < 3000
    assert peak < 2 * 1024 * 1024
    result = reader.run("large.txt", start_line=2, end_line=2)
    assert result.ok and "second line" in result.content and "1|" not in result.content


def test_fractional_mutation_values_enter_wilcoxon_unchanged():
    table = {v: {str(i): {"mutation_score": x} for i, x in enumerate(xs)}
             for v, xs in [("A1", [0.1, 0.3, 0.5, 0.6]), ("A2", [0.2, 0.4, 0.5, 0.7])]}
    result = analysis.paired(table, "A1", "A2")
    expected = analysis.stats.wilcoxon([0.2, 0.4, 0.5, 0.7], [0.1, 0.3, 0.5, 0.6], zero_method="wilcox")
    assert result["nonzero_pairs"] == 3 and result["test_status"] == "computed"
    assert math.isfinite(result["wilcoxon_p"])
    assert result["wilcoxon_p"] == pytest.approx(expected.pvalue)


@pytest.mark.parametrize("p", [float("nan"), float("inf"), -0.1, 1.1])
def test_holm_rejects_invalid_pvalues(p):
    with pytest.raises(ValueError):
        analysis.holm({"bad": p})


def test_nonfinite_wilcoxon_is_reported_as_failure(monkeypatch):
    monkeypatch.setattr(analysis.stats, "wilcoxon", lambda *a, **k: (0.0, float("nan")))
    table = {"A1": {"x": {"mutation_score": 0.1}}, "A2": {"x": {"mutation_score": 0.2}}}
    with pytest.raises(ValueError, match="非有限"):
        analysis.paired(table, "A1", "A2")


def test_no_usable_pairs_is_an_explicit_error():
    table = {v: {"x": {"mutation_score": None}} for v in ["A1", "A2"]}
    with pytest.raises(ValueError, match="有效"):
        analysis.paired(table, "A1", "A2")


def test_derivation_uses_input_output_and_preserves_raw_bytes(tmp_path):
    sources = {}
    for v in ("A0", "A1", "A2", "A3"):
        path = tmp_path / v / "example.json"
        path.parent.mkdir()
        raw = json.dumps({"variant": v, "instance_id": "example", "status": "all_pass",
                          "agent": {"input_tokens": 100, "output_tokens": 20, "total_tokens": 900},
                          "final": {"mutation_score": 0.625, "all_pass": True}, "duration_sec": 1})
        path.write_text(raw)
        sources[path] = path.read_bytes()
    (tmp_path / "per_instance.csv").write_text("historical CSV, unchanged")
    output = analysis.derive_results(tmp_path)
    table = analysis.load_per_instance(output / "per_instance.csv")
    assert all(table[v]["example"]["total_tokens"] == 120 for v in table)
    assert all(table[v]["example"]["mutation_score"] == 0.625 for v in table)
    assert all(path.read_bytes() == raw for path, raw in sources.items())
    assert (tmp_path / "per_instance.csv").read_text() == "historical CSV, unchanged"
    assert json.loads((output / "manifest.json").read_text())["version"] == analysis.DERIVATION_VERSION


def test_evaluation_of_generated_tests_cannot_read_external_file(sandbox_workspace):
    from eval.metrics import run_pytest_on
    sentinel = sandbox_workspace.parent / "evaluation-secret.txt"
    sentinel.write_text("evaluation-fixture")
    (sandbox_workspace / "test_probe.py").write_text(
        "from pathlib import Path\n"
        "def test_no_host_access():\n"
        f"    assert not Path({str(sentinel)!r}).exists()\n"
    )
    result = run_pytest_on("test_probe.py", sandbox_workspace)
    assert result.all_pass, result.process


def test_evaluation_cannot_report_pass_when_isolation_is_missing(tmp_path, monkeypatch):
    from code_agent import sandbox
    from eval.hooks import _run_pytest
    monkeypatch.setattr(sandbox.shutil, "which", lambda _: None)
    result = _run_pytest(tmp_path)
    assert result["status"] == "FAIL" and result["passed"] == 0
