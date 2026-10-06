"""Independent follow-up probes. All credentials and files are synthetic fixtures."""
from __future__ import annotations

import json
from pathlib import Path
import sys
import tempfile
import time
import tracemalloc

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
sys.path[:0] = [str(REPO / "src"), str(REPO)]

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.proc import run_process
from code_agent.session import SessionStore
from code_agent.tools.factories import build_registry
from tests.helpers import ScriptedLLM, text_response, tool_response

checks = {}
with tempfile.TemporaryDirectory(prefix="rereview-extra-") as raw:
    workspace = Path(raw)
    (workspace / "solution.py").write_text("def add(a, b):\n    return a + b\n")
    registry = build_registry(Settings(workspace=workspace))

    fake_values = {
        "password": "review-json-password-not-a-real-secret",
        "api_key": "review-json-api-value-not-a-real-secret",
        "token": "review-json-token-not-a-real-secret",
    }
    (workspace / "credentials.json").write_text(json.dumps(fake_values))
    store = SessionStore.create(workspace / "sessions")
    agent = Agent(
        llm=ScriptedLLM([
            tool_response(("read_file", {"path": "credentials.json"})),
            text_response("done"),
        ]), tools=registry, system_prompt="independent redaction probe",
        on_event=store.record_event,
    )
    agent.state.add_user("Read the synthetic reviewer fixture")
    agent.begin_task()
    result = agent.run()
    logged = store.path.read_text()
    checks["structured_credentials_redaction"] = {
        "status": result.status,
        "fixture_uses_no_real_credentials": True,
        "plaintext_fields_in_log": [key for key, value in fake_values.items() if value in logged],
        "log_path_is_temporary": True,
    }
    known = SessionStore.create(workspace / "known", secrets=list(fake_values.values()))
    known.write({"type": "tool_call_start", "arguments": fake_values})
    checks["known_values_redaction"] = {
        "all_values_redacted": not any(value in known.path.read_text() for value in fake_values.values()),
    }

    warnings = []
    sink = workspace / "unwritable-directory"
    sink.mkdir()
    failing_store = SessionStore(path=sink, warn=warnings.append)
    for _ in range(2):
        failing_store.write({"type": "probe", "content": "synthetic"})
    checks["log_failure_diagnostic"] = {
        "write_errors": failing_store.write_errors,
        "warnings": len(warnings),
        "reason_present": bool(failing_store.last_write_error),
        "summary_write_errors": failing_store.summary().get("write_errors"),
        "memory_entries": len(failing_store.entries),
    }

    target = workspace / "protected.txt"
    target.write_text("original")
    outcomes = []
    for invalid in ("false", "true", 0, 1, None):
        result = registry.execute("write_file", {
            "path": target.name, "content": "changed", "overwrite": invalid,
        })
        outcomes.append({"argument": invalid, "rejected": not result.ok,
                         "original_preserved": target.read_text() == "original"})
    false_result = registry.execute("write_file", {
        "path": target.name, "content": "changed", "overwrite": False,
    })
    true_result = registry.execute("write_file", {
        "path": target.name, "content": "changed", "overwrite": True,
    })
    checks["strict_overwrite_types"] = {
        "invalid_values": outcomes,
        "false_prevents_overwrite": not false_result.ok,
        "true_permits_overwrite": true_result.ok and target.read_text() == "changed",
        "integer_rejects_bool": not registry.execute("read_file", {
            "path": target.name, "start_line": True,
        }).ok,
    }

    calls = [tool_response(("read_file", {"path": "solution.py"})) for _ in range(6)]
    budget_agent = Agent(llm=ScriptedLLM(calls), tools=registry,
                         system_prompt="task budget probe", max_turns=3)
    budget_agent.state.add_user("First task")
    budget_agent.begin_task()
    first = budget_agent.run_until(1)
    second = budget_agent.run_until(3)
    third = budget_agent.run()
    budget_agent.state.add_user("Second task")
    budget_agent.begin_task()
    fourth = budget_agent.run()
    checks["task_and_checkpoint_budgets"] = {
        "segment_statuses": [first.status, second.status, third.status],
        "segment_turns": [first.turns, second.turns, third.turns],
        "same_task_total_turns": first.turns + second.turns + third.turns,
        "next_task_status": fourth.status,
        "next_task_turns": fourth.turns,
        "session_total_turns": budget_agent.state.turn_index,
    }

    cancelled = Agent(llm=ScriptedLLM([text_response("new task answer")]),
                      tools=registry, system_prompt="abort lifecycle probe")
    cancelled.state.add_user("Cancelled task")
    cancelled.begin_task()
    cancelled.abort()
    cancelled_result = cancelled.run()
    cancelled.state.add_user("New task after cancellation")
    cancelled.begin_task()
    next_result = cancelled.run()
    checks["new_task_after_cancellation"] = {
        "cancelled_status": cancelled_result.status,
        "next_task_status": next_result.status,
        "next_task_turns": next_result.turns,
        "next_task_error": next_result.error,
    }

    cap = 1000
    tracemalloc.start()
    tracemalloc.reset_peak()
    proc = run_process([
        sys.executable, "-c", "import sys; sys.stdout.write('x' * (8 * 1024 * 1024)); sys.stdout.flush()",
    ], cwd=workspace, timeout=10, output_char_cap=cap)
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    checks["unterminated_output_peak_allocation"] = {
        "producer_output_chars": 8 * 1024 * 1024,
        "capture_cap_chars": cap,
        "stored_chars": len(proc.stdout) + len(proc.stderr),
        "output_truncated": proc.output_truncated,
        "exit_code": proc.exit_code,
        "reviewer_process_python_peak_bytes": peak,
        "runtime_sec": proc.duration_sec,
        "measurement_scope": "Python allocations in the reviewer process; excludes child memory and is not RSS",
    }

output = ROOT / "additional_checks.json"
output.write_text(json.dumps(checks, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(checks, ensure_ascii=False, indent=2))
