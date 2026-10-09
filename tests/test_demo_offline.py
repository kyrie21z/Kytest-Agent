"""The offline CLI must reject failed or unconfirmed pytest execution."""
from dataclasses import replace

import pytest

from code_agent.proc import ProcResult
from code_agent.tools.base import ToolResult
from code_agent.tools.shell_tools import RunCommandTool
from scripts import demo_offline


@pytest.mark.parametrize("process", [
    None,
    ProcResult(exit_code=1, stdout="5 passed in 0.01s"),
    ProcResult(exit_code=0, stdout="5 skipped in 0.01s"),
    ProcResult(exit_code=0, stdout="1 passed in 0.01s"),
    ProcResult(exit_code=0, stdout="5 passed in 0.01s", timed_out=True),
    ProcResult(exit_code=0, stdout="5 passed in 0.01s", output_truncated=True),
    ProcResult(exit_code=0, stdout="5 passed in 0.01s", error="launch failed"),
])
def test_smoke_fails_without_five_confirmed_passes(monkeypatch, process):
    # The model can say "done" and the tool can display success while process facts disagree.
    monkeypatch.setattr(RunCommandTool, "run", lambda *args, **kwargs:
                        ToolResult(True, "5 passed", process=process))
    with pytest.raises(AssertionError):
        demo_offline.main()


def test_smoke_fails_when_the_tool_reports_an_error(monkeypatch):
    monkeypatch.setattr(RunCommandTool, "run", lambda *args, **kwargs:
                        ToolResult(False, "execution denied",
                                   process=ProcResult(exit_code=0, stdout="5 passed in 0.01s")))
    with pytest.raises(AssertionError, match="pytest 工具执行失败"):
        demo_offline.main()


def test_smoke_uses_actual_process_output_and_completes_without_model_calls(monkeypatch, capsys):
    original = RunCommandTool.run
    def changed_display(tool, **kwargs):
        return replace(original(tool, **kwargs), content="Localized display: 90 passed")
    monkeypatch.setattr(RunCommandTool, "run", changed_display)
    assert demo_offline.main() == 0
    assert "pytest exit=0；5 passed" in capsys.readouterr().out
