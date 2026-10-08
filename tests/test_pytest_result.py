"""Shared execution observations: summary selection, incomplete runs and real pytest."""
import sys

import pytest

from code_agent.proc import ProcResult, run_capture
from code_agent.pytest_result import parse_pytest_result


@pytest.mark.parametrize("output,expected", [
    ("....\n3 failed, 5 passed in 0.12s", (5, 3, 0, 0)),
    ("1 error, 2 passed, 1 skipped in 0.30s", (2, 0, 1, 1)),
    ("1 passed in 0.01s\n2 passed in 0.02s", (2, 0, 0, 0)),
    ("1 passed in 0.01s\n5 skipped in 0.02s", (0, 0, 0, 5)),
    ("1 passed in 0.01s\n5 xfailed in 0.02s", (0, 0, 0, 0)),
    ("Claims: 90 passed\n1 failed, 2 passed in 0.01s", (2, 1, 0, 0)),
    ("=== 2  PASSED, 1 warning in 61.20s (0:01:01) ===", (2, 0, 0, 0)),
    ("\x1b[32m2 passed, 1 deselected in 0.01s\x1b[0m", (2, 0, 0, 0)),
    ("1 passed in 0.01s\nno tests ran in 0.02s", (0, 0, 0, 0)),
    ("2 passed in banana", (0, 0, 0, 0)),
    ("Claims: 2 passed in 0.01s", (0, 0, 0, 0)),
    ("some random output", (0, 0, 0, 0)),
])
def test_final_whole_summary_determines_counts(output, expected):
    result = parse_pytest_result(ProcResult(exit_code=0, stdout=output))
    assert tuple(result.counts.values()) == expected


@pytest.mark.parametrize("process", [
    None,
    ProcResult(error="executable not found"),
    ProcResult(exit_code=0, stdout="0 passed in 0.01s"),
    ProcResult(exit_code=0, stdout="5 skipped in 0.01s"),
    ProcResult(exit_code=0, stdout="Claims: 90 passed"),
    ProcResult(exit_code=0, stdout="1 passed, 1 error in 0.01s"),
    ProcResult(exit_code=0, stdout="1 passed, 1 failed in 0.01s"),
    ProcResult(exit_code=2, stdout="1 passed in 0.01s"),
    ProcResult(exit_code=0, timed_out=True, stdout="1 passed in 0.01s"),
    ProcResult(exit_code=0, output_truncated=True, stdout="1 passed in 0.01s"),
])
def test_unexecuted_empty_failed_or_incomplete_run_cannot_pass(process):
    assert not parse_pytest_result(process).all_pass


def test_raw_evidence_survives_diagnostic_excerpt_and_separate_streams():
    process = ProcResult(exit_code=1, stdout=(
        "PASSED test_solution.py::test_good\n"
        "FAILED test_solution.py::test_bad - AssertionError\n"
        "1 failed, 1 passed in 0.01s\n" + "diagnostic " * 1000),
        stderr='File "solution.py", line 3\n')
    result = parse_pytest_result(process)
    assert result.complete and not result.all_pass and result.import_ok
    assert result.counts == {"passed": 1, "failed": 1, "errors": 0, "skipped": 0}
    assert result.passed_nodes == ["test_solution.py::test_good"]
    assert result.failure_nodes == ["test_solution.py::test_bad"]
    assert result.failure_lines == ["FAILED test_solution.py::test_bad - AssertionError"]
    assert result.failure_in_solution and result.process is process


@pytest.mark.parametrize("code,exit_code,counts,all_pass", [
    ("def test_ok():\n    assert True\n", 0, (1, 0, 0, 0), True),
    ("def test_bad():\n    assert False\n", 1, (0, 1, 0, 0), False),
    ("import pytest\n@pytest.mark.skip\ndef test_skip():\n    assert False\n", 0, (0, 0, 0, 1), False),
    ("import missing_fixture_xyz\n", 2, (0, 0, 1, 0), False),
])
def test_observations_match_real_pytest(tmp_path, code, exit_code, counts, all_pass):
    (tmp_path / "test_solution.py").write_text(code)
    process = run_capture([sys.executable, "-m", "pytest", "test_solution.py", "-q",
                           "-p", "no:cacheprovider", "-rA"],
                          cwd=tmp_path, timeout=10, execution_mode="trusted",
                          env={"PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"})
    result = parse_pytest_result(process)
    assert process.exit_code == exit_code, process
    assert result.complete and tuple(result.counts.values()) == counts
    assert result.all_pass is all_pass
    assert result.passed_nodes == (["test_solution.py::test_ok"] if all_pass else [])


def test_startup_failure_is_retained_without_fabricated_test_counts(tmp_path):
    process = run_capture(["missing-executable-for-pytest-result-test"],
                          cwd=tmp_path, timeout=2, execution_mode="trusted")
    result = parse_pytest_result(process)
    assert process.error and process.exit_code is None
    assert not result.complete and not result.to_dict()["ran"]
    assert result.to_dict()["execution_error"] == process.error
