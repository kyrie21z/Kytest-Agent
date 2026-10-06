"""事件渲染：把 Agent 事件翻译成给人看或给机器看的输出。

这是"Agent 核心零 IO"这条设计约束的兑现处——CLI 是订阅者，不是循环的一部分。
因此这里没有任何业务逻辑，只有展示决策。

三种模式的差别只体现在这里：

- `--print` 只输出最终回答，中间过程写到 stderr（可重定向丢弃）；
- `--mode json` 每行一个事件，stdout 只放协议记录，便于 harness 消费；
- 交互模式逐轮显示思考与工具调用，并把工具输出做成单行预览。
"""
from __future__ import annotations

import json
import sys
from typing import Any, Optional, TextIO

from .agent.events import (
    AssistantMessageEvent,
    ErrorEvent,
    RunEnd,
    RunStart,
    ToolCallEnd,
    TurnStart,
)

# 单行预览宽度。太长会把终端刷乱，也让"这一步做了什么"难以扫读。
PREVIEW_WIDTH = 100


def one_line(text: str, width: int = PREVIEW_WIDTH) -> str:
    """压成一行并截断。"""
    flat = " ".join((text or "").split())
    if len(flat) <= width:
        return flat
    return flat[: width - 1] + "…"


def first_content_line(text: str, width: int = PREVIEW_WIDTH) -> str:
    """第一条非空行。多行输出直接压平会丢掉结构，取首行更可读。"""
    for line in (text or "").splitlines():
        stripped = line.strip()
        if stripped:
            return one_line(stripped, width)
    return ""


def last_content_line(text: str, width: int = PREVIEW_WIDTH) -> str:
    """最后一条非空行。命令输出的结论（退出码、测试摘要）总在末尾。"""
    for line in reversed((text or "").splitlines()):
        stripped = line.strip()
        if stripped:
            return one_line(stripped, width)
    return ""


def format_arguments(arguments: Any, width: int = 70) -> str:
    """把工具参数渲染成紧凑形式。长字符串值截断——完整内容在轨迹文件里。"""
    if not isinstance(arguments, dict):
        return one_line(str(arguments), width)
    parts = []
    for key, value in arguments.items():
        if isinstance(value, str) and len(value) > 40:
            parts.append(f"{key}={value[:37]!r}…")
        else:
            parts.append(f"{key}={value!r}")
    return one_line(", ".join(parts), width)


class EventRenderer:
    """给终端用户的渲染器。`verbose=False` 时中间过程写到 stderr。"""

    def __init__(self, *, stream: TextIO, verbose: bool = True, progress: Optional[TextIO] = None) -> None:
        self.stream = stream
        self.progress = progress if progress is not None else sys.stderr
        self.verbose = verbose

    def _out(self, text: str, *, intermediate: bool = False) -> None:
        target = self.stream if (self.verbose or not intermediate) else self.progress
        print(text, file=target, flush=True)

    def __call__(self, event: Any) -> None:
        renderer = getattr(self, f"_on_{event.type}", None)
        if renderer is not None:
            renderer(event)

    # ------------------------------------------------------------------
    def _on_run_start(self, event: RunStart) -> None:
        self._out(f"▶ 开始（工具：{', '.join(event.tools) or '无'}）", intermediate=True)

    def _on_turn_start(self, event: TurnStart) -> None:
        self._out(
            f"\n── Turn {event.turn}｜上下文 {event.request_messages} 条消息"
            f" / {event.request_chars} 字符",
            intermediate=True,
        )

    def _on_assistant_message(self, event: AssistantMessageEvent) -> None:
        if event.text:
            self._out(f"  思考：{event.text}", intermediate=True)
        for call in event.tool_calls:
            self._out(
                f"  → {call['name']}({format_arguments(call.get('arguments'))})",
                intermediate=True,
            )
        if not event.tool_calls:
            self._out("  （无工具调用，本轮结束）", intermediate=True)

    def _on_tool_call_end(self, event: ToolCallEnd) -> None:
        flag = "✗" if event.is_error else "✓"
        head = (
            f"  ← {flag} {event.name}（{event.duration_sec * 1000:.0f} ms）"
            f"{first_content_line(event.content)}"
        )
        self._out(head, intermediate=True)
        if event.name == "run_command":
            self._out(f"      {last_content_line(event.content)}", intermediate=True)

    def _on_error(self, event: ErrorEvent) -> None:
        self._out(f"  ! [{event.where}] {event.message}", intermediate=True)

    def _on_run_end(self, event: RunEnd) -> None:
        detail = f"status={event.status}"
        if event.error:
            detail += f"｜{event.error}"
        self._out(f"\n■ 结束：{detail}（累计 {event.turns} 个 turn）", intermediate=True)


class JsonRenderer:
    """JSONL 渲染器：每行一个事件，stdout 只放协议记录。"""

    def __init__(self, stream: TextIO) -> None:
        self.stream = stream

    def __call__(self, event: Any) -> None:
        record = event.to_dict()
        print(json.dumps(record, ensure_ascii=False), file=self.stream, flush=True)
