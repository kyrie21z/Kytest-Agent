"""进程执行层测试。

这组测试针对三个真实会出错的地方：
1. 超时后必须杀掉**整棵**进程树（否则留下孤儿进程，并行评测时拖垮机器）；
2. 超时必须在子进程持续输出时仍然生效（readline 阻塞会让超时永不触发）；
3. 输出必须完整采集（子进程写完管道前不能被误判为结束）。
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import pytest

from code_agent.proc import run_process, split_command


def test_split_command_handles_quotes():
    assert split_command("python -m pytest -q") == ["python", "-m", "pytest", "-q"]
    assert split_command('echo "hello world"') == ["echo", "hello world"]
    assert split_command("   ") == []


def test_split_command_survives_unbalanced_quotes():
    """引号不配对时退化为按空白切分，而不是抛异常中断 Agent。"""
    parts = split_command('echo "unterminated')
    assert parts[0] == "echo"
    assert len(parts) == 2


def test_split_command_keeps_windows_backslash_paths(tmp_path: Path):
    """Windows 上不能把反斜杠当转义符，否则路径会被拆坏。"""
    if sys.platform != "win32":
        pytest.skip("仅在 Windows 上验证反斜杠语义")
    target = tmp_path / "sub" / "script.py"
    parts = split_command(f'python "{target}"')
    assert parts[1] == str(target)


def test_split_command_does_not_leak_leading_spaces_into_arguments(tmp_path: Path):
    """带引号路径后面的参数不能带上前导空格。

    这是实际发生过的缺陷：切掉 argv[0] 后剩余字符串以空格开头，
    第一个参数会变成 ' --flag'，子进程收到错误的参数。
    """
    if sys.platform != "win32":
        pytest.skip("仅在 Windows 上验证 CommandLineToArgvW 语义")
    target = tmp_path / "a b" / "s.py"
    parts = split_command(f'python "{target}" --flag value')
    assert parts == ["python", str(target), "--flag", "value"], parts


def test_split_command_survives_argv0_text_appearing_inside_quotes(tmp_path: Path):
    """argv[0] 的文本若在引号内部也出现，解析不能被它带偏。

    真实踩过的坑：用 `str.find(argv0)` 定位切点会命中引号**内部**的同名文本，
    从引号中间切开后整个参数序列错位。
    """
    if sys.platform != "win32":
        pytest.skip("仅在 Windows 上验证 CommandLineToArgvW 语义")
    target = tmp_path / "python" / "run me.py"
    parts = split_command(f'python "{target}" python --flag')
    assert parts == ["python", str(target), "python", "--flag"], parts


def test_split_command_handles_empty_and_quoted_arguments():
    if sys.platform != "win32":
        pytest.skip("仅在 Windows 上验证 CommandLineToArgvW 语义")
    assert split_command('python -c ""') == ["python", "-c", ""]
    assert split_command('python script.py "a b" c') == ["python", "script.py", "a b", "c"]


def test_split_command_matches_what_the_child_process_actually_receives(tmp_path: Path):
    """解析结果必须与子进程真实收到的 argv 一致。

    这是唯一有意义的验收方式：拿一个真实子进程把 sys.argv 打印回来对比，
    而不是只和自己写的预期列表比。
    """
    target = tmp_path / "with space" / "echo_args.py"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("import sys; print(repr(sys.argv[1:]))", encoding="utf-8")

    command = f'{sys.executable} "{target}" --flag "a b" plain'
    parts = split_command(command)

    import subprocess

    completed = subprocess.run(parts, capture_output=True, text=True, timeout=60)
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip() == "['--flag', 'a b', 'plain']"


def test_run_process_captures_stdout_and_exit_code(tmp_path: Path):
    result = run_process(
        [sys.executable, "-c", "print('hello'); print('world')"],
        cwd=tmp_path,
        timeout=30,
    )
    assert result.ok
    assert result.exit_code == 0
    assert result.stdout.strip().splitlines() == ["hello", "world"]
    assert result.timed_out is False
    assert result.duration_sec >= 0


def test_run_process_separates_stderr_and_reports_failure(tmp_path: Path):
    result = run_process(
        [sys.executable, "-c", "import sys; print('out'); sys.stderr.write('boom'); sys.exit(3)"],
        cwd=tmp_path,
        timeout=30,
    )
    assert result.ok is False
    assert result.exit_code == 3
    assert "out" in result.stdout
    assert "boom" in result.stderr


def test_run_process_reports_missing_executable(tmp_path: Path):
    result = run_process(["definitely-not-a-real-binary-xyz"], cwd=tmp_path, timeout=10)
    assert result.ok is False
    assert result.exit_code is None
    assert "找不到可执行文件" in (result.error or "")


def test_run_process_times_out_and_kills_the_process(tmp_path: Path):
    result = run_process(
        [sys.executable, "-c", "import time; time.sleep(60)"],
        cwd=tmp_path,
        timeout=1.0,
    )
    assert result.timed_out is True
    assert result.exit_code is None
    assert result.duration_sec < 20  # 说明确实被终止，而不是等它自然结束


def test_timeout_still_fires_when_child_floods_output(tmp_path: Path):
    """子进程持续输出时，超时逻辑仍然必须生效。

    这是"用 for line in proc.stdout 收集输出"写法的经典死法：
    子进程不换行地一直写，主线程卡在 readline 上，超时永远不会被检查到。
    """
    code = "import sys, time\nwhile True:\n    sys.stdout.write('x' * 4096)\n    sys.stdout.flush()\n"
    started = time.monotonic()
    result = run_process([sys.executable, "-c", code], cwd=tmp_path, timeout=1.5)
    elapsed = time.monotonic() - started
    assert result.timed_out is True
    assert elapsed < 20
    assert len(result.stdout) > 0  # 已经产生的大量输出被采集到了


def test_grandchild_process_is_killed_too(tmp_path: Path):
    """孙进程也必须被清理。

    只杀直接子进程时，`python -m pytest` 之类会 fork 出自己、
    父进程被杀后子进程继续跑，在并行评测里会迅速累积成机器级故障。
    """
    if sys.platform == "win32":
        inner = "import time; time.sleep(60)"
        outer = (
            "import subprocess, sys, time\n"
            f"subprocess.Popen([sys.executable, '-c', {inner!r}])\n"
            "time.sleep(60)\n"
        )
    else:
        outer = "import subprocess, sys, time\nsubprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)'])\ntime.sleep(60)\n"

    result = run_process([sys.executable, "-c", outer], cwd=tmp_path, timeout=1.5)
    assert result.timed_out is True
    # 给 taskkill / SIGKILL 一点时间落地
    time.sleep(0.5)
    assert _count_sleep_children() == 0, "仍有残留的休眠子进程——进程树没有被完整清理"


def _count_sleep_children() -> int:
    """统计当前仍存活的 `time.sleep(60)` 测试进程数。"""
    if sys.platform == "win32":
        import subprocess

        completed = subprocess.run(
            [
                "wmic",
                "process",
                "where",
                "name='python.exe'",
                "get",
                "CommandLine",
            ],
            capture_output=True,
            text=True,
            timeout=30,
            creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
        )
        output = completed.stdout or ""
    else:
        import subprocess

        completed = subprocess.run(["ps", "-eo", "args"], capture_output=True, text=True, timeout=30)
        output = completed.stdout or ""
    return sum(1 for line in output.splitlines() if "time.sleep(60)" in line)


def test_env_overrides_are_applied(tmp_path: Path):
    result = run_process(
        [sys.executable, "-c", "import os; print(os.environ.get('CODE_AGENT_TEST_FLAG', 'missing'))"],
        cwd=tmp_path,
        timeout=30,
        env={"CODE_AGENT_TEST_FLAG": "on"},
    )
    assert result.stdout.strip() == "on"


def test_empty_argv_is_rejected_without_starting_anything(tmp_path: Path):
    result = run_process([], cwd=tmp_path, timeout=5)
    assert result.ok is False
    assert result.error == "命令为空"

# ----------------------------------------------------------------------
# 评审整改：子进程环境白名单、输出采集上限
# ----------------------------------------------------------------------
def test_child_env_excludes_parent_secrets(tmp_path: Path):
    """子进程环境按白名单构造，父进程的敏感变量（API Key）不得传递（评审 Q3）。"""
    import os

    secret = "sk-sentinel-test-value"
    os.environ["LLM_API_KEY"] = secret
    os.environ["MY_TEST_SECRET"] = secret
    try:
        probe = (
            "import os, sys; print('KEY_LEAK' if any("
            "'sk-sentinel' in str(v) for v in os.environ.values()) else 'CLEAN')"
        )
        result = run_process(
            [sys.executable, "-c", probe], cwd=tmp_path, timeout=30,
        )
        assert result.ok, result.stderr
        assert "CLEAN" in result.stdout
    finally:
        os.environ.pop("LLM_API_KEY", None)
        os.environ.pop("MY_TEST_SECRET", None)


def test_output_capture_cap_truncates_but_keeps_draining(tmp_path: Path):
    """采集上限在采集阶段强制：超限丢弃但继续排空，且标志可见（评审 Q3）。

    子进程持续输出超过上限的内容：若实现"到量即停读"，管道会塞满、
    子进程阻塞、超时失控。正确行为是排空到底 + output_truncated 置位。
    """
    result = run_process(
        [sys.executable, "-c", "print('x' * 100000)"], cwd=tmp_path, timeout=30,
        output_char_cap=1000,
    )
    assert result.ok
    assert result.output_truncated is True
    assert len(result.stdout) <= 2000  # 上限附近，不是 100000
    assert "x" in result.stdout
