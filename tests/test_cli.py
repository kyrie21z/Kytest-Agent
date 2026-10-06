"""CLI 测试：三种模式、流分离、退出码、轨迹落盘。

这些测试通过真实子进程调用 CLI，而不是直接调 `main()`。理由是这一层的价值
恰恰在"进程边界"上：stdout/stderr 是否分离、退出码是否正确、零安装能否运行——
只有真跑一个进程才能验证。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MAIN = PROJECT_ROOT / "main.py"

SOLUTION = '''def clamp(value, low, high):
    if low > high:
        raise ValueError("low must not exceed high")
    if value < low:
        return low
    if value > high:
        return high
    return value
'''


def run_cli(*args: str, stdin: str = "", timeout: int = 180) -> subprocess.CompletedProcess:
    """在干净的环境下调用 CLI，确保测试不依赖外部已配置的凭据。

    必须清掉 `CODE_AGENT_WORKSPACE`：它会让 `.env` 与工作区都指向别处，
    使"未配置凭据"这类测试变成一次真实的网络请求。
    """
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    for key in (
        "LLM_API_KEY",
        "OPENAI_API_KEY",
        "LLM_BASE_URL",
        "LLM_MODEL",
        "CODE_AGENT_WORKSPACE",
    ):
        env.pop(key, None)
    return subprocess.run(
        [sys.executable, str(MAIN), *args],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
        env=env,
        cwd=str(PROJECT_ROOT),
    )


@pytest.fixture()
def workspace(tmp_path: Path) -> Path:
    (tmp_path / "solution.py").write_text(SOLUTION, encoding="utf-8")
    return tmp_path


# ----------------------------------------------------------------------
# --print
# ----------------------------------------------------------------------
def test_print_mode_writes_only_the_final_answer_to_stdout(workspace: Path):
    """stdout 必须只有最终回答，过程信息走 stderr——否则无法安全重定向。"""
    completed = run_cli("-C", str(workspace), "--print", "--mock", "--no-session", "解释 solution.py")

    assert completed.returncode == 0, completed.stderr
    assert completed.stdout.strip(), "stdout 不能为空"
    # 过程信息（turn 标题、工具调用行）不应出现在 stdout
    assert "── Turn" not in completed.stdout
    assert "→ read_file" not in completed.stdout
    assert "▶ 开始" not in completed.stdout


def test_print_mode_shows_progress_on_stderr(workspace: Path):
    completed = run_cli("-C", str(workspace), "--print", "--mock", "--no-session", "解释 solution.py")

    assert "── Turn" in completed.stderr
    assert "▶ 开始" in completed.stderr
    # 运行摘要也必须可被脚本提取
    assert "[completed]" in completed.stderr


def test_print_mode_requires_a_task(workspace: Path):
    completed = run_cli("-C", str(workspace), "--print", "--mock")
    assert completed.returncode == 2
    assert "需要一个任务描述" in completed.stderr


def test_mock_mode_actually_runs_the_agent_loop(workspace: Path):
    """离线模式必须真的走完循环，而不是直接吐一段固定文案。"""
    completed = run_cli("-C", str(workspace), "--print", "--mock", "--no-session", "解释 solution.py")

    assert completed.returncode == 0
    assert "list_files" in completed.stderr   # 第一轮先列目录
    assert "read_file" in completed.stderr    # 第二轮读真实文件
    assert "turns=3" in completed.stderr      # 列目录 → 读文件 → 收尾
    # 最终回答里应包含真实读到的代码内容
    assert "def clamp" in completed.stdout


# ----------------------------------------------------------------------
# --mode json
# ----------------------------------------------------------------------
def test_json_mode_emits_one_valid_event_per_line(workspace: Path):
    completed = run_cli(
        "-C", str(workspace), "--mode", "json", "--print", "--mock", "--no-session", "解释 solution.py"
    )
    assert completed.returncode == 0, completed.stderr

    lines = [line for line in completed.stdout.splitlines() if line.strip()]
    assert lines, "JSON 模式必须至少输出一个事件"
    events = [json.loads(line) for line in lines]  # 每行都必须是合法 JSON
    types = [event["type"] for event in events]

    assert types[0] == "run_start"
    assert types[-1] == "run_end"
    assert "turn_start" in types
    assert "tool_call_start" in types
    assert "tool_call_end" in types
    assert events[-1]["status"] == "completed"


def test_json_mode_keeps_stdout_free_of_human_text(workspace: Path):
    """JSON 模式的 stdout 是协议通道，不能混入任何人类可读文本。"""
    completed = run_cli(
        "-C", str(workspace), "--mode", "json", "--print", "--mock", "--no-session", "解释 solution.py"
    )
    for line in completed.stdout.splitlines():
        if line.strip():
            json.loads(line)  # 任何非 JSON 行都会在这里炸掉
            assert not line.startswith("▶")
            assert "思考" not in line


def test_json_mode_includes_tool_arguments_and_results(workspace: Path):
    completed = run_cli(
        "-C", str(workspace), "--mode", "json", "--print", "--mock", "--no-session", "解释 solution.py"
    )
    events = [json.loads(line) for line in completed.stdout.splitlines() if line.strip()]
    starts = [event for event in events if event["type"] == "tool_call_start"]
    ends = [event for event in events if event["type"] == "tool_call_end"]

    assert starts and ends
    assert starts[0]["name"] == "list_files"
    assert starts[0]["arguments"] == {"path": ".", "recursive": True}
    assert ends[0]["is_error"] is False
    # 事件携带工具原始输出；协议标记由 Agent 循环加在消息层，不重复出现在事件里
    assert "solution.py" in ends[0]["content"]
    assert "[OK]" not in ends[0]["content"]


# ----------------------------------------------------------------------
# 交互模式
# ----------------------------------------------------------------------
def test_interactive_mode_runs_a_task_then_exits_on_eof(workspace: Path):
    completed = run_cli("-C", str(workspace), "--mock", "--no-session", stdin="解释 solution.py\n")

    assert completed.returncode == 0, completed.stderr
    assert "交互模式" in completed.stdout
    assert "›" in completed.stdout
    assert "【离线 Mock 模式】" in completed.stdout


def test_interactive_mode_survives_empty_lines_and_reports_trace_path(workspace: Path):
    completed = run_cli(
        "-C", str(workspace), "--mock", stdin="\n\n解释 solution.py\nexit\n"
    )
    assert completed.returncode == 0, completed.stderr
    assert "轨迹已保存" in completed.stdout
    assert "[completed]" in completed.stderr


# ----------------------------------------------------------------------
# 轨迹落盘
# ----------------------------------------------------------------------
def test_session_file_is_written_with_expected_structure(workspace: Path):
    completed = run_cli("-C", str(workspace), "--print", "--mock", "解释 solution.py")
    assert completed.returncode == 0, completed.stderr

    sessions = list((workspace / ".sessions").glob("*.jsonl"))
    assert len(sessions) == 1, "应当恰好产生一份轨迹文件"

    entries = [json.loads(line) for line in sessions[0].read_text(encoding="utf-8").splitlines()]
    types = [entry["type"] for entry in entries]

    assert types[0] == "session"
    assert entries[0]["workspace"] == str(workspace.resolve())
    assert entries[0]["tools"], "会话头必须记录可用工具，便于事后核对"
    assert types.count("user") == 1
    assert "assistant" in types
    assert "tool_call" in types and "tool_result" in types
    assert types[-1] == "result"
    assert entries[-1]["status"] == "completed"
    assert entries[-1]["turns"] == 3


def test_session_records_tool_results_with_full_content(workspace: Path):
    """轨迹是复现证据，工具结果必须完整保存而不是摘要。"""
    run_cli("-C", str(workspace), "--print", "--mock", "解释 solution.py")
    session = next((workspace / ".sessions").glob("*.jsonl"))
    entries = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]

    results = [entry for entry in entries if entry["type"] == "tool_result"]
    assert results
    read_result = next(entry for entry in results if entry["name"] == "read_file")
    assert "def clamp(value, low, high)" in read_result["content"]
    assert read_result["duration_sec"] >= 0


def test_no_session_flag_writes_nothing(workspace: Path):
    completed = run_cli("-C", str(workspace), "--print", "--mock", "--no-session", "解释 solution.py")
    assert completed.returncode == 0
    assert not (workspace / ".sessions").exists()


def test_session_dir_can_be_overridden(workspace: Path, tmp_path: Path):
    target = tmp_path / "traces"
    completed = run_cli(
        "-C", str(workspace), "--print", "--mock", "--session-dir", str(target), "解释 solution.py"
    )
    assert completed.returncode == 0, completed.stderr
    assert list(target.glob("*.jsonl"))


def test_sessions_are_append_only_so_a_crash_keeps_earlier_evidence(workspace: Path):
    """两次独立运行写两份文件；同一份文件里的记录逐行追加，不重写整份。"""
    run_cli("-C", str(workspace), "--print", "--mock", "第一次")
    run_cli("-C", str(workspace), "--print", "--mock", "第二次")
    sessions = list((workspace / ".sessions").glob("*.jsonl"))
    assert len(sessions) == 2
    for session in sessions:
        entries = [json.loads(line) for line in session.read_text(encoding="utf-8").splitlines()]
        assert entries[-1]["type"] == "result"


# ----------------------------------------------------------------------
# 参数校验与退出码
# ----------------------------------------------------------------------
def test_help_lists_the_three_modes():
    completed = run_cli("--help")
    assert completed.returncode == 0
    assert "--print" in completed.stdout
    assert "--mode" in completed.stdout
    assert "--mock" in completed.stdout


def test_unknown_tool_name_is_rejected_before_running(workspace: Path):
    completed = run_cli("-C", str(workspace), "--print", "--mock", "-t", "read_file,no_such_tool", "任务")
    assert completed.returncode == 2
    assert "未知工具" in completed.stderr


def test_missing_workspace_is_rejected(workspace: Path, tmp_path: Path):
    completed = run_cli("-C", str(tmp_path / "nope"), "--print", "--mock", "任务")
    assert completed.returncode == 2
    assert "工作目录不存在" in completed.stderr


def test_max_turns_budget_is_respected(workspace: Path):
    completed = run_cli(
        "-C", str(workspace), "--print", "--mock", "--no-session", "--max-turns", "1", "解释 solution.py"
    )
    assert "turns=1" in completed.stderr
    assert "[max_turns]" in completed.stderr


def test_missing_credentials_fall_back_to_mock_without_crashing(workspace: Path):
    """没有 API Key 也必须能跑——这是"5 分钟可运行"硬性要求的关键一环。

    用 `--no-env-file` 让测试密闭：否则它会读到本仓库的 `.env` 并发起真实请求，
    结果依赖于开发机的配置状态。测试套件不能有这种依赖。
    """
    completed = run_cli(
        "-C", str(workspace), "--no-env-file", "--print", "--no-session", "解释 solution.py"
    )
    assert completed.returncode == 0, completed.stderr
    # 退回离线模式必须在 stderr 上明确告知，否则用户会以为拿到的是真实模型回答
    assert "未配置 LLM_API_KEY" in completed.stderr
    assert "离线" in completed.stderr
    assert "【离线 Mock 模式】" in completed.stdout

# ----------------------------------------------------------------------
# 评审整改：任务生命周期、日志脱敏、写盘失败可见
# ----------------------------------------------------------------------
def test_two_tasks_each_get_their_own_budget(workspace: Path):
    """交互模式下连续任务不得继承上一个任务耗尽的预算（评审 F3）。

    旧实现：第二个任务立即返回 max_turns、turns=0，什么都没做。
    修复后：每个任务从自己的预算基线开始计量。
    """
    completed = run_cli(
        "-C", str(workspace), "--mock", "--no-session", "--max-turns", "2",
        stdin="解释 solution.py\n再解释一次 solution.py\n",
    )
    assert completed.returncode == 0, completed.stderr
    assert "[max_turns] turns=2" in completed.stderr  # 任务 1 按预算停止
    assert "[completed]" in completed.stderr          # 任务 2 真的执行了
    assert "turns=0" not in completed.stderr          # 旧行为：任务 2 零轮被拒


def test_session_redacts_known_secret_shapes(workspace: Path):
    """工具读到的凭据原文不能出现在会话轨迹里（评审 A4）。

    工作区里放一个带模拟密钥的文本文件，让 Agent 读它；轨迹文件里必须只有
    脱敏标记，不出现 sk- 原文。模拟值仅存在于临时工作区。
    （用 credentials.txt 而不是 .env：MockLLM 的文件名正则不识别 .env。）
    """
    (workspace / "credentials.txt").write_text(
        "api_key=sk-sentinel12345678\npassword=hunter2secret\n",
        encoding="utf-8",
    )
    completed = run_cli(
        "-C", str(workspace), "--no-env-file", "--print",
        "读取 credentials.txt 并显示它的内容",
    )
    assert completed.returncode == 0, completed.stderr
    sessions = sorted((workspace / ".sessions").glob("*.jsonl"))
    assert sessions, "应产出会话轨迹"
    content = "\n".join(p.read_text(encoding="utf-8") for p in sessions)
    assert "sk-sentinel12345678" not in content, "轨迹中泄漏了模拟密钥原文"
    assert "hunter2secret" not in content, "轨迹中泄漏了模拟口令"
    assert "***REDACTED***" in content, "应有可见的脱敏标记"


def test_session_write_failure_is_visible(tmp_path: Path):
    """写盘失败不能静默：失败计数、原因、警告必须可见（评审 Q3）。"""
    from code_agent.session import SessionStore

    warnings: list[str] = []
    store = SessionStore.create(
        tmp_path / "sessions", secrets=(), warn=warnings.append
    )
    store.write({"type": "user", "content": "第一条应成功"})
    assert store.write_errors == 0

    # 注入故障：写入目标变成一个目录 → open("a") 抛 OSError
    store.path.unlink()
    store.path.mkdir()
    store.write({"type": "user", "content": "第二条应失败"})
    store.write({"type": "user", "content": "第三条也失败"})

    assert store.write_errors == 2
    assert "OSError" in store.last_write_error or "Error" in store.last_write_error
    assert len(warnings) == 1, "警告只发一次，不逐条刷屏"
    assert "写入失败" in warnings[0]
    # 内存副本完整保留——轨迹不能因为写盘故障而丢内容
    assert len(store.entries) == 3
    summary = store.summary()
    assert summary["write_errors"] == 2
