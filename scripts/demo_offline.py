"""离线演示：不联网、不需要 API Key，跑通一次完整的 Agent 闭环。

用途：
1. 验收 Agent 主循环 —— 真实工具、真实文件系统、真实多轮工具调用；
2. 作为 CLI 轨迹渲染的雏形 —— 事件 → 人类可读文本的映射就在这里；
3. 排查"循环到底做了什么" —— 输出包含每个 turn 的请求规模与工具耗时。

运行：
    python scripts/demo_offline.py
"""
from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from code_agent.agent import Agent  # noqa: E402
from code_agent.config import Settings  # noqa: E402
from code_agent.tools.base import ToolRegistry  # noqa: E402
from code_agent.tools.factories import build_registry  # noqa: E402

# 用当前解释器的绝对路径，避免依赖 PATH 里的 `python` 是哪一个版本。
PYTHON = sys.executable

SOLUTION = '''def clamp(value, low, high):
    """把 value 夹在 [low, high] 区间内。"""
    if low > high:
        raise ValueError("low must not exceed high")
    if value < low:
        return low
    if value > high:
        return high
    return value
'''

GENERATED_TEST = '''import pytest

from solution import clamp


def test_value_inside_range_is_returned_unchanged():
    assert clamp(5, 1, 10) == 5


def test_value_below_lower_bound_is_clamped():
    assert clamp(0, 1, 10) == 1


def test_value_above_upper_bound_is_clamped():
    assert clamp(99, 1, 10) == 10


def test_bounds_are_inclusive():
    assert clamp(1, 1, 10) == 1
    assert clamp(10, 1, 10) == 10


def test_invalid_range_raises():
    with pytest.raises(ValueError):
        clamp(5, 10, 1)
'''


def _first_content_line(text: str, width: int = 90) -> str:
    """取第一条非空行做预览。多行输出取首行会显示空行，失去预览的意义。"""
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped:
            return stripped[:width]
    return ""


def _last_content_line(text: str, width: int = 100) -> str:
    """取最后一条非空行。命令输出的结论（退出码、测试摘要）总在末尾。"""
    for line in reversed((text or "").splitlines()):
        stripped = line.strip()
        if stripped:
            return stripped[:width]
    return ""


def render(event) -> str:
    """把事件渲染成一行人类可读的轨迹。"""
    if event.type == "run_start":
        return f"▶ 开始运行｜工具：{', '.join(event.tools)}"
    if event.type == "turn_start":
        return (
            f"\n── Turn {event.turn} ── 发送 {event.request_messages} 条消息 / "
            f"{event.request_chars} 字符"
        )
    if event.type == "assistant_message":
        lines = [f"  思考：{event.text}" if event.text else "  思考：（无文本输出）"]
        for call in event.tool_calls:
            preview = _json(call["arguments"])
            lines.append(f"  → 调用 {call['name']}({preview[:110]})")
        if not event.tool_calls:
            lines.append("  （未调用工具，循环将在此结束）")
        return "\n".join(lines)
    if event.type == "tool_call_end":
        flag = "✗ 失败" if event.is_error else "✓ 成功"
        head = (
            f"  ← {event.name} {flag}（{event.duration_sec * 1000:.1f} ms）"
            f"{_first_content_line(event.content)}"
        )
        if event.name == "run_command":
            # 命令输出的关键信息在末尾（退出码、测试摘要），单独补一行
            head += f"\n      {_last_content_line(event.content)}"
        return head
    if event.type == "error":
        return f"  ! [{event.where}] {event.message}"
    if event.type == "run_end":
        return f"\n■ 结束：status={event.status}，共 {event.turns} 个 turn"
    return ""


class ScriptedLLM:
    """离线脚本 LLM：模拟"读代码 → 写测试 → 收尾"的三轮真实工具调用。

    真实运行时这里换成 OpenAICompatibleLLM，其余代码一行不改——
    这正是"LLM 层可替换"的意义。
    """

    def __init__(self) -> None:
        self.calls = 0

    @property
    def name(self) -> str:
        return "ScriptedLLM（离线演示）"

    def chat(self, messages, tools=None):
        from code_agent.llm import LLMResponse, ToolCall

        self.calls += 1
        usage = {"prompt_tokens": 900, "completion_tokens": 120}
        if self.calls == 1:
            return LLMResponse(
                content="先读取目标代码，确认真实行为再写测试。",
                tool_calls=[
                    ToolCall(id="c1", name="read_file", arguments='{"path": "solution.py"}')
                ],
                usage=usage,
                raw={"choices": [{"finish_reason": "tool_calls"}]},
            )
        if self.calls == 2:
            return LLMResponse(
                content="代码含三个分支（下界、上界、非法区间），据此写测试。",
                tool_calls=[
                    ToolCall(
                        id="c2",
                        name="write_file",
                        arguments=_json({"path": "test_solution.py", "content": GENERATED_TEST}),
                    )
                ],
                usage=usage,
                raw={"choices": [{"finish_reason": "tool_calls"}]},
            )
        if self.calls == 3:
            return LLMResponse(
                content="测试文件已写好。现在真正运行它——不执行就无法确认断言是否正确。",
                tool_calls=[
                    ToolCall(
                        id="c3",
                        name="run_command",
                        arguments=_json({"command": f'"{PYTHON}" -m pytest test_solution.py -q'}),
                    )
                ],
                usage=usage,
                raw={"choices": [{"finish_reason": "tool_calls"}]},
            )
        return LLMResponse(
            content=(
                "完成：已生成 test_solution.py 并实际运行验证。"
                "5 个用例覆盖正常路径、上下边界与非法区间。"
            ),
            usage=usage,
            raw={"choices": [{"finish_reason": "stop"}]},
        )


def _json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False)


class RecordingRegistry(ToolRegistry):
    """记录工具调用的注册表。

    上线时用不到，但演示与实验都需要它回答同一个问题：
    **Agent 到底自己做了什么？** "A0 会不会自发运行 pytest"这类观察项，
    只能从真实调用记录里得到答案，不能靠看最终输出猜。
    """

    def __init__(self, inner: ToolRegistry) -> None:
        super().__init__()
        for tool in inner.tools:
            self.register(tool)
        self.executed: list = []

    def execute(self, name: str, arguments: dict):
        self.executed.append((name, arguments))
        return super().execute(name, arguments)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="code-agent-demo-") as tmp:
        workspace = Path(tmp)
        (workspace / "solution.py").write_text(SOLUTION, encoding="utf-8")

        settings = Settings(workspace=workspace, allow_write=True, exec_timeout=120)
        registry = RecordingRegistry(build_registry(settings))
        agent = Agent(
            llm=ScriptedLLM(),
            tools=registry,
            system_prompt=(
                "You are a coding agent. Inspect the workspace and complete the "
                "requested software engineering task using the available tools."
            ),
            max_turns=8,
            on_event=lambda event: print(render(event), flush=True),
        )

        print(f"工作区：{workspace}")
        print("任务：Generate unit tests for solution.py\n")
        agent.state.add_user("Generate unit tests for solution.py.")
        result = agent.run()

        print("\n" + "=" * 72)
        print("生成的文件内容：")
        print("=" * 72)
        generated = workspace / "test_solution.py"
        print(generated.read_text(encoding="utf-8") if generated.exists() else "（未生成）")

        print("=" * 72)
        print("关键观察：Agent 自发运行了 pytest 吗？")
        print("=" * 72)
        ran = [call for call in registry.executed if call[0] == "run_command"]
        for name, arguments in ran:
            print(f"  {name}({_json(arguments)})")
        if not ran:
            print("  （没有执行任何命令——在 A0 上这本身就是值得记录的观察结果）")

        print("=" * 72)
        print(f"最终回答：{result.final_text}")
        print(
            f"统计：turns={result.turns} llm_calls={result.llm_calls} "
            f"tool_calls={result.tool_calls} tool_errors={result.tool_errors} "
            f"tokens={result.total_tokens} runtime={result.runtime_sec:.2f}s"
        )
        print("=" * 72)

        assert result.status == "completed", result.status
        assert generated.exists(), "测试文件未生成"
        assert not agent.state.pending_tool_calls(), "存在未配对的工具调用"
        assert ran, "演示脚本预期 Agent 会自发运行命令验证测试"
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
