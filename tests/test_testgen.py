"""Behavioral acceptance for contract-grounded, isolated, additive proposals."""
import json
from pathlib import Path

import pytest

from code_agent.agent import Agent
from code_agent.config import Settings
from code_agent.testgen import SubmitTestsTool, make_testgen_hook
from code_agent.tools.factories import build_registry
from tests.helpers import ScriptedLLM, text_response, tool_response

SOURCE = '''def count(n):
    """Given a positive integer n, return n plus one."""
    return n + 1
'''


def case(name="test_two", code=None, **overrides):
    return {"name": name, "code": code or f"from solution import count\ndef {name}():\n    assert count(2) == 3\n",
            "contract_quote": "Given a positive integer n", "input_domain": "positive integers",
            "oracle_reason": "two plus one is three", "fault_hypothesis": "off-by-one in returned count", **overrides}


@pytest.fixture
def tool(tmp_path):
    (tmp_path / "solution.py").write_text(SOURCE)
    return SubmitTestsTool(Settings(workspace=tmp_path, allow_code_execution=True))


def results(tool, candidates):
    result = tool.run(cases=candidates)
    assert result.ok, result.content
    return json.loads(result.content)["results"]


def test_mixed_batch_keeps_good_case_and_identifies_wrong_oracle(tool):
    bad = case("test_wrong", "from solution import count\ndef test_wrong():\n    assert count(2) == 99\n")
    report = results(tool, [bad, case()])
    assert [r["status"] for r in report] == ["FAIL", "ACCEPTED"]
    assert "99" in report[0]["diagnostic"]
    assert set(tool.accepted) == {"test_two"}
    assert "test_wrong" not in (tool.workspace / "test_solution.py").read_text()


def test_positive_precondition_refuses_zero_before_execution(tool):
    bad = case("test_zero", "from solution import count\ndef test_zero():\n    assert count(0) == 1\n")
    assert results(tool, [bad])[0]["status"] == "REJECTED"
    assert tool.subprocess_runs == 0


def test_numeric_and_length_ranges_are_checked_without_execution(tmp_path):
    (tmp_path / "solution.py").write_text('''def pick(arr, k):
    """Sum the first k elements. 1 <= len(arr) <= 100. 1 <= k <= len(arr)."""
    return sum(arr[:k])
''')
    tool = SubmitTestsTool(Settings(workspace=tmp_path))
    bad = case("test_range", "from solution import pick\ndef test_range():\n    assert pick([1], 2) == 1\n",
               contract_quote="1 <= k <= len(arr)", input_domain="nonempty list and valid prefix length")
    row = results(tool, [bad])[0]
    assert row["status"] == "REJECTED" and "len(arr)" in row["diagnostic"]
    assert tool.subprocess_runs == 0


def test_hanging_candidate_does_not_poison_other_tests(tool):
    tool.case_timeout = .6
    bad = case("test_hang", "from solution import count\ndef test_hang():\n    while True:\n        count(2)\n    assert count(2) == 3\n")
    report = results(tool, [bad, case()])
    assert [r["status"] for r in report] == ["TIMEOUT", "ACCEPTED"]
    assert set(tool.accepted) == {"test_two"}


def test_failed_revision_and_direct_overwrite_preserve_accepted_suite(tool):
    results(tool, [case()])
    previous = (tool.workspace / "test_solution.py").read_text()
    assert results(tool, [case(code="from solution import count\ndef test_two():\n    assert count(2) == 99\n")])[0]["status"] == "NAME_LOCKED"
    (tool.workspace / "test_solution.py").write_text("assert False")
    tool.publish()
    assert (tool.workspace / "test_solution.py").read_text() == previous


def test_conflicting_import_aliases_keep_original_bindings(tool):
    one = case("test_one", "from solution import count as f\ndef test_one():\n    assert f(2) == 3\n")
    two = case("test_sqrt", "from math import sqrt as f\nfrom solution import count\ndef test_sqrt():\n    assert count(3) == f(16)\n")
    assert [r["status"] for r in results(tool, [one, two])] == ["ACCEPTED", "ACCEPTED"]
    assert tool._execute(tool.suite_source(), 5)["status"] == "PASS"


def test_modifying_sut_cannot_be_accepted(tool):
    altered = case("test_tamper", "from solution import count\ndef test_tamper():\n    open('solution.py', 'w').write('def count(n): return 0')\n    assert count(2) == 3\n")
    assert results(tool, [altered])[0]["status"] == "SUT_MODIFIED"
    assert not tool.accepted and (tool.workspace / "solution.py").read_text() == SOURCE


@pytest.mark.parametrize("overrides", [
    {"contract_quote": "This quotation is invented"},
    {"oracle_reason": 12},
    {"code": "print('execution at module level')\ndef test_two():\n    assert True"},
    {"code": "def test_two(tmp_path):\n    assert True"},
    {"code": "from solution import *\ndef test_two():\n    assert True"},
    {"code": "from solution import count\ndef test_two():\n    count(2)"},
])
def test_invalid_metadata_or_code_has_no_execution(tool, overrides):
    assert results(tool, [case(**overrides)])[0]["status"] == "REJECTED"
    assert tool.subprocess_runs == 0


def test_permissions_fail_closed(tool):
    tool.settings.allow_code_execution = False
    assert not tool.run(cases=[case()]).ok
    assert tool.subprocess_runs == 0 and not (tool.workspace / "testgen_report.json").exists()


def test_attempt_budget_survives_multiple_calls(tool):
    tool.max_attempts = 1
    results(tool, [case(contract_quote="invented")])
    assert results(tool, [case()])[0]["status"] == "BUDGET_EXHAUSTED"
    assert tool.subprocess_runs == 0


def test_agent_repairs_rejected_case_and_preserves_good_test(tool):
    registry = build_registry(tool.settings, ("read_file", "submit_tests"))
    tool = registry.get("submit_tests")
    bad = case("test_three", "from solution import count\ndef test_three():\n    assert count(3) == 99\n")
    good = {**bad, "code": "from solution import count\ndef test_three():\n    assert count(3) == 4\n"}
    llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [case(), bad]})),
                      tool_response(("submit_tests", {"cases": [good]})), text_response("finished")])
    agent = Agent(llm=llm, tools=registry, system_prompt="generate tests", max_turns=4,
                  finish_turn=make_testgen_hook(tool))
    agent.state.add_user("generate tests")
    assert agent.run().status == "completed"
    assert len(tool.accepted) == 2
    assert "test_three" in llm.requests[1][-1]["content"]
    assert tool.attempts[1]["status"] == "FAIL" and tool.attempts[2]["status"] == "ACCEPTED"


def test_hook_restores_sut_and_refuses_direct_unvalidated_suite(tool):
    registry = build_registry(tool.settings, ("write_file", "submit_tests"))
    tool = registry.get("submit_tests")
    llm = ScriptedLLM([tool_response(("write_file", {"path": "test_solution.py", "content": "def test_fake(): assert True"})),
                      tool_response(("submit_tests", {"cases": [case()]})), text_response("done")])
    agent = Agent(llm=llm, tools=registry, system_prompt="generate", max_turns=4,
                  finish_turn=make_testgen_hook(tool))
    agent.state.add_user("generate")
    assert agent.run().status == "completed"
    assert "test_fake" not in (tool.workspace / "test_solution.py").read_text()
    assert (tool.workspace / "testgen_unvalidated.py").exists()


def test_a4_has_no_early_pass_stop_and_baseline_registry_stays_generic(tool):
    from eval.runner import default_variant
    assert "submit_tests" not in build_registry(tool.settings).names()
    assert "submit_tests" in default_variant("A4").tool_names
    assert default_variant("A4").system_runs_cap == 0


def test_unspecified_exception_promise_is_rejected(tool):
    bad = case("test_error", "import pytest\nfrom solution import count\ndef test_error():\n    with pytest.raises(ValueError):\n        count(2)\n")
    assert results(tool, [bad])[0]["status"] == "REJECTED"
    assert tool.subprocess_runs == 0


def test_constant_only_assertion_is_rejected(tool):
    bad = case(code="from solution import count\ndef test_two():\n    count(2)\n    assert True\n")
    assert results(tool, [bad])[0]["status"] == "REJECTED"
    assert tool.subprocess_runs == 0


def test_cli_real_http_drives_specialized_validation(tmp_path):
    import os
    import subprocess
    import sys
    import threading
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
    (tmp_path / "solution.py").write_text(SOURCE)
    requests = []
    responses = [tool_response(("submit_tests", {"cases": [case()]})), text_response("one validated test accepted")]
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass
        def do_POST(self):
            requests.append(json.loads(self.rfile.read(int(self.headers["Content-Length"]))))
            response = responses.pop(0)
            message = {"role": "assistant", "content": response.content,
                       "tool_calls": [c.to_message() for c in response.tool_calls]}
            body = json.dumps({"choices": [{"message": message, "finish_reason": "tool_calls" if response.tool_calls else "stop"}],
                               "usage": {"prompt_tokens": 10, "completion_tokens": 20}}).encode()
            self.send_response(200); self.end_headers(); self.wfile.write(body)
    server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    server.daemon_threads = True
    threading.Thread(target=server.serve_forever, daemon=True).start()
    env = {**os.environ, "LLM_API_KEY": "local-fixture", "LLM_MODEL": "scripted-http",
           "LLM_BASE_URL": f"http://127.0.0.1:{server.server_port}/v1"}
    try:
        root = Path(__file__).resolve().parents[1]
        completed = subprocess.run([sys.executable, str(root / "main.py"), "-C", str(tmp_path),
            "--test-generation", "--no-env-file", "--no-session", "--print", "generate tests"],
            env=env, text=True, capture_output=True, timeout=15)
        assert completed.returncode == 0, completed.stderr
        assert len(requests) == 2
        assert "submit_tests" in {t["function"]["name"] for t in requests[0]["tools"]}
        report = json.loads((tmp_path / "testgen_report.json").read_text())
        assert len(report["accepted"]) == 1
        assert "one validated" in completed.stdout
    finally:
        server.shutdown(); server.server_close()


def test_cli_missing_sut_is_configuration_error(tmp_path):
    from code_agent.cli import main
    assert main(["-C", str(tmp_path), "--test-generation", "--mock", "--no-env-file", "--no-session", "--print", "generate"]) == 2


def test_generic_python_uses_same_interpreter_and_pytest_as_validator(tool):
    import sys
    from code_agent.tools.shell_tools import RunCommandTool
    shell = RunCommandTool(tool.settings)
    version = shell.run(command="python -m pytest --version")
    assert version.ok, version.content
    executable = shell.run(command="python -c \"import sys; print(sys.executable)\"")
    assert executable.ok and sys.executable in executable.content


def test_command_timeout_cannot_bypass_configured_hard_cap(tool):
    from code_agent.tools.shell_tools import RunCommandTool
    tool.settings.max_exec_timeout = .5
    shell = RunCommandTool(tool.settings)
    result = shell.run(command="python -c \"while True: pass\"", timeout=100)
    assert not result.ok and "0.5s" in result.content
    assert "已超时" in result.content


def test_local_solution_import_is_recognized(tool):
    proposed = case(code="def test_two():\n    from solution import count\n    assert count(2) == 3\n")
    assert results(tool, [proposed])[0]["status"] == "ACCEPTED"


def test_existing_suite_survives_new_proposals_with_conflicting_aliases(tool):
    seed = "from math import sqrt as f\ndef test_seed():\n    assert f(16) == 4\n"
    (tool.workspace / "test_solution.py").write_text(seed)
    tool = SubmitTestsTool(tool.settings)
    assert results(tool, [case(code="from solution import count as f\ndef test_two():\n    assert f(2) == 3\n")])[0]["status"] == "ACCEPTED"
    assert "test_seed" in tool.suite_source()
    assert tool._execute(tool.suite_source(), 5)["status"] == "PASS"


def test_failed_existing_suite_is_preserved_instead_of_silently_replaced(tool):
    seed = "def test_seed():\n    assert 1 == 99\n"
    (tool.workspace / "test_solution.py").write_text(seed)
    tool = SubmitTestsTool(tool.settings)
    row = results(tool, [case()])[0]
    assert row["status"] == "REGRESSION_FAIL" and not tool.accepted
    assert (tool.workspace / "test_solution.py").read_text() == seed


def test_source_size_limit_applies_to_new_specialized_reader(tool):
    from code_agent.errors import ToolError
    tool.settings.max_file_bytes = 2
    with pytest.raises(ToolError, match="MAX_FILE_BYTES"):
        SubmitTestsTool(tool.settings)


def test_six_failures_fit_in_one_complete_registry_response(tool):
    registry = build_registry(tool.settings, ("submit_tests",))
    candidates = [case(f"test_wrong_{i}", f"from solution import count\ndef test_wrong_{i}():\n    assert count(2) == 99\n") for i in range(6)]
    result = registry.execute("submit_tests", {"cases": candidates})
    payload = json.loads(result.content)
    assert len(payload["results"]) == 6
    assert all(r["status"] == "FAIL" for r in payload["results"])


def test_reference_compatibility_does_not_claim_all_inputs_checked(tool):
    proposal = case("test_loop", "from solution import count\ndef test_loop():\n    for n in range(1, 4):\n        assert count(n) == n + 1\n")
    row = results(tool, [proposal])[0]
    assert row["status"] == "ACCEPTED"
    assert row["contract_checks"]["unchecked_calls"] == 1


def test_cli_specialized_mode_builds_the_real_tool_and_hook(tool, monkeypatch):
    from code_agent import cli
    args = cli.build_parser().parse_args(["--test-generation", "--print", "--mock", "--no-session", "generate"])
    llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [case()]})), text_response("done")])
    monkeypatch.setattr(cli, "build_llm", lambda *_: (llm, "scripted offline"))
    agent, _, _ = cli.build_agent(args, tool.settings, lambda _: None, session_enabled=False)
    agent.state.add_user("generate")
    assert agent.run().status == "completed"
    assert len(agent.tools.get("submit_tests").accepted) == 1
    assert agent.finish_turn is not None


def test_pilot_counts_no_tests_as_zero_for_mutable_reference(tmp_path):
    from scripts.run_testgen_pilot import summarize
    folder = tmp_path / "repeat_1" / "A4"
    folder.mkdir(parents=True)
    (folder / "HumanEval__1.json").write_text(json.dumps({"variant": "A4", "instance_id": "HumanEval/1",
        "status": "no_tests", "final": {"all_pass": False, "mutants_total": 0}, "agent": {}}))
    summary = summarize(tmp_path)
    assert summary["per_run"][0]["valid_mutation"] == 0
    assert summary["variants"]["A4"]["runs"] == 1 and not summary["complete"]


def test_incomparable_pilot_cannot_promote_apparent_gain_or_lose_report_label(tmp_path):
    from scripts.run_testgen_pilot import summarize
    ids = ("HumanEval/1", "HumanEval/122", "HumanEval/154", "HumanEval/4", "HumanEval/69")
    for repeat in range(1, 4):
        for variant, score in (("A0", .5), ("A4", 1)):
            folder = tmp_path / f"repeat_{repeat}" / variant
            folder.mkdir(parents=True)
            for iid in ids:
                (folder / (iid.replace("/", "__") + ".json")).write_text(json.dumps({
                    "variant": variant, "instance_id": iid, "status": "all_pass",
                    "final": {"all_pass": True, "mutation_score": score}, "agent": {}}))
    assert summarize(tmp_path)["candidate_for_independent_evaluation"] is True
    (tmp_path / "validity.json").write_text(json.dumps({"comparable": False, "reason": "Different pytest runtimes"}))
    assert summarize(tmp_path)["candidate_for_independent_evaluation"] is False
    report = (tmp_path / "report.md").read_text()
    assert "不可用于机制比较" in report and "进入独立评测候选：False" in report


def test_deferred_measurement_runs_once_after_generation(tmp_path, monkeypatch):
    from eval.dataset import Instance
    from eval.runner import default_variant, run_single
    from eval import runner
    inst = Instance("DEMO/0", 'def count(n):\n    """Given a positive integer n, return n plus one."""\n', '    return n + 1\n', "count", "")
    measurements = []
    actual = runner.collect_metrics
    def measure(*args, **kwargs):
        measurements.append(kwargs["checkpoint"])
        return actual(*args, **kwargs)
    def factory(variant, settings, registry, workspace):
        submitter = registry.get("submit_tests")
        llm = ScriptedLLM([tool_response(("submit_tests", {"cases": [case()]})), text_response("done")])
        return Agent(llm=llm, tools=registry, system_prompt=variant.resolve_system_prompt(),
                     finish_turn=make_testgen_hook(submitter))
    monkeypatch.setattr(runner, "collect_metrics", measure)
    outcome = run_single(inst, default_variant("A4"), run_root=tmp_path,
                         settings_factory=lambda w: Settings(workspace=w), agent_factory=factory,
                         defer_measurement=True, max_mutants=3, measurement_timeouts=(3, 10, 3))
    assert measurements == [0]
    assert outcome.final["all_pass"] is True
    assert outcome.agent["measurement_deferred"] is True
    assert outcome.agent["testgen"]["accepted"][0]["name"] == "test_two"
