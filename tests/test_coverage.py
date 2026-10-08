"""Collector failure paths and the caller's export policy."""
import json

import pytest

from code_agent.coverage import collect_coverage
from code_agent.proc import ProcResult

COMMAND = ["python", "-m", "coverage", "run", "-m", "pytest"]


def test_rejected_execution_never_exports_or_reads_a_stale_report(tmp_path):
    report = tmp_path / ".coverage.json"
    report.write_text('{"files":{"solution.py":{"summary":{"percent_covered":100}}}}')
    calls = []
    def execute(argv, limit):
        calls.append(argv)
        return ProcResult(exit_code=1, stdout="1 failed in 0.01s")
    result = collect_coverage(tmp_path, "solution.py", execute, command=COMMAND, timeout=3,
                              export_if=lambda execution: execution.exit_code == 0)
    assert result.error and result.target is None and len(calls) == 1
    assert not report.exists()


def test_measurement_may_export_after_failed_tests_and_preserves_raw_fields(tmp_path):
    target = {"summary":{"num_statements":2,"covered_lines":1}, "missing_lines":[3],
              "missing_branches":[[2,3]]}
    def execute(argv, limit):
        if argv[3] == "json":
            (tmp_path / ".coverage.json").write_text(json.dumps({"files":{"C:\\work\\solution.py":target}}))
            return ProcResult(exit_code=0)
        return ProcResult(exit_code=1)
    result = collect_coverage(tmp_path, "solution.py", execute, command=COMMAND, timeout=3)
    assert not result.error and result.target == target
    assert result.execution.exit_code == 1


@pytest.mark.parametrize("report", ["not json", '{"files":{}}', '{"files":{"other_solution.py":{}}}'])
def test_unreadable_or_missing_target_report_is_unavailable(tmp_path, report):
    def execute(argv, limit):
        if argv[3] == "json":
            (tmp_path / ".coverage.json").write_text(report)
        return ProcResult(exit_code=0)
    result = collect_coverage(tmp_path, "solution.py", execute, command=COMMAND, timeout=3)
    assert result.error and result.target is None


def test_failed_export_does_not_accept_a_report_written_by_the_failed_process(tmp_path):
    def execute(argv, limit):
        if argv[3] == "json":
            (tmp_path / ".coverage.json").write_text('{"files":{"solution.py":{}}}')
            return ProcResult(exit_code=1, stderr="export failed")
        return ProcResult(exit_code=0)
    result = collect_coverage(tmp_path, "solution.py", execute, command=COMMAND, timeout=3)
    assert result.target is None and "export failed" in result.error
