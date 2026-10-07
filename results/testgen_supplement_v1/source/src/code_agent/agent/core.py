"""Agent 主循环。

这是全项目唯一的主循环。所有变体（A0 通用 / A1 测试感知 / A2 执行反馈 / A3 覆盖率引导）
共用这一份实现，差异只能通过构造参数注入：

    tools            —— 工具集（阶段 2 落地）
    system_prompt    —— 策略文本
    max_turns 等     —— 预算
    before_turn      —— 每轮开始前的编排钩子
    finish_turn      —— 每轮结束后的编排钩子，可决定提前终止

这样"每加入一个变量就换一份代码"的结构性风险被排除：变体之间的 diff 全部是配置，
混叠变量在架构层就不可能发生。

关键 API 约束：`run_until(turns)` 必须在任意 turn 数处可返回、且之后能继续运行。
固定预算质量曲线（在第 1/2/4/8 个 turn 处取样）依赖这条约束；一跑到底的
`run()` 实现无法做预算对照实验。

循环内约定：
- 一次 turn = 一次 LLM 调用 + 它触发的全部工具执行；
- 每个 tool_call 无论成功失败都必须产生恰好一条 tool 消息，否则消息序列非法；
- 未知工具、参数非法、工具抛异常都只是"一条 is_error 的观察结果"，不是崩溃；
- LLM 请求失败不抛异常，而是转成 stop_reason="error" 的消息并结束本次 run。
"""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Literal, Optional

from ..llm import BaseLLM, LLMResponse
from ..message import AssistantMessage, TextBlock, ToolCallBlock, Usage
from .events import (
    AssistantMessageEvent,
    ErrorEvent,
    RunEnd,
    RunStart,
    ToolCallEnd,
    ToolCallStart,
    TurnEnd,
    TurnStart,
)
from .state import AgentState, estimate_chars

RunStatus = Literal[
    "completed",        # 模型自然结束（无工具调用且策略未要求继续）
    "stopped",          # 策略钩子或工具主动要求终止
    "paused",           # 到达 run_until() 指定的 turn 检查点，可继续运行
    "max_turns",        # 触达 turn 预算
    "max_tokens",       # 触达 token 预算
    "llm_error",        # LLM 请求失败
    "aborted",          # 被 abort() 或 LLM 返回 aborted
]


@dataclass
class TurnDecision:
    """`finish_turn` 钩子的返回值：决定循环是否继续。"""

    end: bool = False
    reason: str = ""
    # 主动要求再跑一轮（即使本轮没有工具调用）。A2 的"修完再跑一次"用它。
    continue_: bool = False


@dataclass
class TurnOutcome:
    """单个 turn 的结果，供钩子与测试使用。"""

    turn: int
    assistant: AssistantMessage
    tool_results: List[Dict[str, Any]] = field(default_factory=list)
    errors: int = 0


@dataclass
class RunResult:
    """一次 run()/run_until() 调用的结构化结果。字段直接对应评测 result schema。

    注意：turns 是**本次调用**跑了几个 turn，而 llm_calls/tool_calls/token 是
    **累计值**。固定预算采样时需要前者来判断"这次推进了多少"，需要后者来算成本。
    """

    status: RunStatus
    turns: int = 0
    llm_calls: int = 0
    tool_calls: int = 0
    tool_errors: int = 0
    tool_calls_skipped: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0
    runtime_sec: float = 0.0
    error: Optional[str] = None
    final_text: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "status": self.status,
            "turns": self.turns,
            "llm_calls": self.llm_calls,
            "tool_calls": self.tool_calls,
            "tool_errors": self.tool_errors,
            "tool_calls_skipped": self.tool_calls_skipped,
            "input_tokens": self.input_tokens,
            "output_tokens": self.output_tokens,
            "total_tokens": self.total_tokens,
            "runtime_sec": round(self.runtime_sec, 3),
            "error": self.error,
            "final_text": self.final_text,
        }


def _result_text(result: Any) -> str:
    """把工具的返回值规范成纯文本，**不带任何协议标记**。

    标记由 `_record_tool_result` 唯一负责添加。这个分工是有教训的：早先
    `_execute_tool` 和 `_record_tool_result` 各自加了一次前缀，消息里就出现了
    `[OK] [OK]`。加标记的位置只能有一个。
    """
    if result is None:
        return "(工具没有返回内容)"
    if isinstance(result, str):
        return result
    return str(getattr(result, "content", None) or result)


class Agent:
    """无 IO 的 Agent 运行时。

    Args:
        llm: LLM 客户端，需实现 `chat(messages, tools) -> LLMResponse`。
        tools: 工具注册表，需提供 `names()`、`schemas()`、`execute(name, args)`。
        system_prompt: 策略文本。变体之间的主要差异在这里。
        max_turns: turn 预算（一次 LLM 调用 + 工具执行 = 1 turn）。
        max_llm_calls: LLM 调用次数上限，与 max_turns 双保险。
        max_total_tokens: 累计 token 上限，0 表示不限。**这不是单次输出上限**——
        max_context_chars: 单次请求的上下文预算。
        before_turn: 每轮开始前调用，签名 (agent, state) -> None。
        finish_turn: 每轮结束后调用，签名 (agent, outcome) -> TurnDecision | None。
        on_event: 事件订阅者。CLI、harness、测试都通过它观察运行过程。
    """

    def __init__(
        self,
        *,
        llm: BaseLLM,
        tools: Any,
        system_prompt: str,
        max_turns: int = 8,
        max_llm_calls: int = 16,
        max_total_tokens: int = 0,
        max_context_chars: int = 32000,
        before_turn: Optional[Callable[["Agent", AgentState], None]] = None,
        finish_turn: Optional[Callable[["Agent", TurnOutcome], Optional[TurnDecision]]] = None,
        on_event: Optional[Callable[[Any], None]] = None,
        state: Optional[AgentState] = None,
    ) -> None:
        self.llm = llm
        self.tools = tools
        self.max_turns = max(1, int(max_turns))
        self.max_llm_calls = max(1, int(max_llm_calls))
        self.max_total_tokens = max(0, int(max_total_tokens))
        self.max_context_chars = max(1000, int(max_context_chars))
        self.before_turn = before_turn
        self.finish_turn = finish_turn
        self._on_event = on_event

        self.state = state or AgentState(system_prompt=system_prompt)
        self.state.system_prompt = system_prompt
        self._aborted = False
        self._done = False
        # 任务预算基线：begin_task() 时点上的累计计数。预算检查用的是
        # "当前值 − 基线"（任务内消耗），而不是累计值——否则交互模式下
        # 第二个任务会立即继承第一个任务耗尽的预算，turns=0 直接拒绝。
        # 未调用 begin_task() 时基线为 0，行为与旧版完全一致。
        self._task_base_turns = 0
        self._task_base_llm_calls = 0
        self._task_base_total_tokens = 0

    # ------------------------------------------------------------------
    # 对外接口
    # ------------------------------------------------------------------
    def begin_task(self) -> None:
        """标记一个新任务的开始：预算从本任务重新计量，取消状态一并解除。

        交互式 CLI 在每个用户任务前调用。三件事都以任务为作用域：
        1. 轮数/调用数/token 预算的基线重置——同一任务内的多次 run()/run_until()
           （checkpoint 分段、中断恢复）**共享同一基线**，不会每段都重置；
        2. `_aborted` 清除——上一个任务的 Ctrl-C 只应终止那一个任务，
           不能让复用的 Agent 拒绝后续所有任务；
        3. 会话历史保留，后续任务仍可引用此前信息。
        """
        self._task_base_turns = self.state.turn_index
        self._task_base_llm_calls = self.state.llm_calls
        self._task_base_total_tokens = self.state.usage.total_tokens
        self._aborted = False

    def abort(self) -> None:
        """请求终止。协作式：在下一个 turn 边界生效。"""
        self._aborted = True

    def run(self) -> RunResult:
        """跑到自然结束或预算耗尽。"""
        return self._run(None)

    def run_until(self, turns: int) -> RunResult:
        """跑到累计 `turns` 个 turn 为止，然后返回（可继续调用）。

        用于固定预算质量曲线：在第 1/2/4/8 个 turn 处取样并评测。
        """
        return self._run(max(0, int(turns)))

    # ------------------------------------------------------------------
    # 主循环
    # ------------------------------------------------------------------
    def _run(self, stop_after_turn: Optional[int]) -> RunResult:
        started = time.monotonic()
        base_turn = self.state.turn_index
        status: RunStatus = "completed"
        error: Optional[str] = None
        final_text = ""

        self._emit(
            RunStart(
                system_prompt_chars=len(self.state.system_prompt),
                tools=list(self.tools.names()),
            )
        )

        while True:
            if self._aborted:
                status, error = "aborted", "运行被主动终止"
                break
            # 预算检查用"任务内消耗"（当前值 − begin_task 基线），不是累计值。
            turns_used = self.state.turn_index - self._task_base_turns
            if turns_used >= self.max_turns:
                status = "max_turns"
                break
            if stop_after_turn is not None and self.state.turn_index >= stop_after_turn:
                status = "paused"
                break
            if self.state.llm_calls - self._task_base_llm_calls >= self.max_llm_calls:
                status = "max_turns"
                error = f"达到 LLM 调用上限 {self.max_llm_calls}"
                break
            if (
                self.max_total_tokens
                and self.state.usage.total_tokens - self._task_base_total_tokens >= self.max_total_tokens
            ):
                status = "max_tokens"
                break

            if self.before_turn is not None:
                self.before_turn(self, self.state)
            # 钩子是唯一能在两步之间叫停的位置（例如交互式 CLI 收到 Ctrl-C），
            # 因此在钩子之后立刻复查一次，而不是拖到下一轮开头。
            if self._aborted:
                status, error = "aborted", "运行被主动终止"
                break

            turn_no = self.state.turn_index + 1
            request = self.state.build_request_messages(self.max_context_chars)
            self._emit(
                TurnStart(
                    turn=turn_no,
                    request_messages=len(request),
                    request_chars=sum(estimate_chars(m) for m in request),
                )
            )

            assistant, failure = self._call_llm(request)
            if failure is not None:
                status, error = "llm_error", failure
                self._emit(ErrorEvent(where="llm", message=failure))
                break

            assert assistant is not None  # failure 为 None 时必有消息
            self.state.turn_index = turn_no
            self.state.llm_calls += 1
            self.state.usage += assistant.usage
            self.state.add_assistant(assistant)
            final_text = assistant.text or final_text

            self._emit(
                AssistantMessageEvent(
                    turn=turn_no,
                    text=assistant.text,
                    tool_calls=[call.to_dict() for call in assistant.tool_calls],
                    stop_reason=assistant.stop_reason,
                    usage=assistant.usage.to_dict(),
                )
            )

            if assistant.stop_reason == "aborted":
                status, error = "aborted", assistant.error_message
                break
            if assistant.stop_reason == "error":
                status, error = "llm_error", assistant.error_message
                break

            outcome = TurnOutcome(turn=turn_no, assistant=assistant)
            calls = assistant.tool_calls

            if calls and assistant.stop_reason == "length":
                # 输出被 max_tokens 截断，工具参数可能是半截 JSON：一律不执行。
                # 执行它会用错误参数污染工作区，比拒绝执行危险得多。
                # 这**不计入 tool_errors**——工具本身没失败，是模型输出不完整，
                # 混进同一个计数器会让失败分类的分析失去意义。
                # 但 tool_call_start/end 事件必须照常发出：被跳过的调用对
                # harness 必须是可见的，否则失败分类里会凭空少掉一整类。
                for call in calls:
                    self.state.tool_calls_skipped += 1
                    # 独立变量：不能覆盖外层的运行起点 `started`——
                    # 那会让 RunResult.runtime_sec 只统计到截断分支本身，
                    # 此前所有 turn 的耗时全部丢失。
                    tool_started = self._emit_tool_start(turn_no, call)
                    message = (
                        "输出达到 token 上限被截断，本次调用未执行。"
                        "请重新发起该工具调用并给出完整参数。"
                    )
                    self._emit_tool_end(turn_no, call, message, True, False, tool_started)
                    outcome.tool_results.append(
                        self._record_tool_result(turn_no, call, message, is_error=True)
                    )
                    outcome.errors += 1
                terminate_all = False
            else:
                terminations = []
                for call in calls:
                    if self._aborted:
                        self.state.tool_calls_skipped += 1
                        content, is_error, terminate = "当前任务已取消，此工具调用未执行。", True, False
                        tool_started = self._emit_tool_start(turn_no, call)
                        self._emit_tool_end(turn_no, call, content, True, False, tool_started)
                    else:
                        content, is_error, terminate = self._execute_tool(turn_no, call)
                    terminations.append(terminate)
                    outcome.tool_results.append(
                        self._record_tool_result(turn_no, call, content, is_error, terminate)
                    )
                    if is_error:
                        outcome.errors += 1
                # 只有当这批工具**全部**要求终止时才提前结束，与 Pi 的语义一致：
                # 混合批次照常继续，避免单个工具劫持整轮对话。
                terminate_all = bool(terminations) and all(terminations)

            self._emit(
                TurnEnd(turn=turn_no, tool_calls=len(calls), errors=outcome.errors)
            )

            if self._aborted:
                status, error = "aborted", "运行被主动终止"
                break

            decision = self.finish_turn(self, outcome) if self.finish_turn else None
            if decision is not None and decision.end:
                status, error = "stopped", decision.reason or None
                break
            if terminate_all:
                status = "stopped"
                break
            if not calls and not (decision is not None and decision.continue_):
                status = "completed"
                break

        self._emit(RunEnd(status=status, turns=self.state.turn_index, error=error))

        return RunResult(
            status=status,
            turns=self.state.turn_index - base_turn,
            llm_calls=self.state.llm_calls,
            tool_calls=self.state.tool_calls,
            tool_errors=self.state.tool_errors,
            tool_calls_skipped=self.state.tool_calls_skipped,
            input_tokens=self.state.usage.input_tokens,
            output_tokens=self.state.usage.output_tokens,
            total_tokens=self.state.usage.total_tokens,
            runtime_sec=time.monotonic() - started,
            error=error,
            final_text=final_text,
        )

    # ------------------------------------------------------------------
    # 步骤实现
    # ------------------------------------------------------------------
    def _call_llm(self, request: List[Dict[str, Any]]) -> tuple[Optional[AssistantMessage], Optional[str]]:
        """调用 LLM，把异常翻译成 `(None, 错误信息)`。

        错误是数据：网络/鉴权/服务端失败不应该让整个评测批次崩溃，
        而应该记成一次 llm_error 的 run，由 harness 计入失败分类。
        """
        try:
            response: LLMResponse = self.llm.chat(request, self.tools.schemas())
        except Exception as exc:  # noqa: BLE001 - LLM 层任何异常都在此收口
            return None, f"{type(exc).__name__}: {exc}"
        return _to_assistant_message(response), None

    def _emit_tool_start(self, turn: int, call: ToolCallBlock) -> float:
        """发出 tool_call_start 事件并返回计时起点。"""
        self._emit(
            ToolCallStart(turn=turn, id=call.id, name=call.name, arguments=call.arguments)
        )
        return time.monotonic()

    def _emit_tool_end(
        self,
        turn: int,
        call: ToolCallBlock,
        content: str,
        is_error: bool,
        terminate: bool,
        started: float,
    ) -> None:
        self._emit(
            ToolCallEnd(
                turn=turn,
                id=call.id,
                name=call.name,
                is_error=is_error,
                content=content,
                duration_sec=time.monotonic() - started,
                terminate=terminate,
            )
        )

    def _execute_tool(self, turn: int, call: ToolCallBlock) -> tuple[str, bool, bool]:
        """执行一次工具调用，返回 (给模型的文本, 是否出错, 是否请求终止)。"""
        self.state.tool_calls += 1
        started = self._emit_tool_start(turn, call)

        try:
            raw = self.tools.execute(call.name, call.arguments)
            is_error = not bool(getattr(raw, "ok", True))
            terminate = bool(getattr(raw, "terminate", False))
        except KeyboardInterrupt:
            self.abort()
            raw = f"工具 `{call.name}` 被用户中断；可能已有副作用，不自动重试。"
            is_error, terminate = True, False
        except Exception as exc:  # noqa: BLE001 - 工具异常必须变成可观察的结果
            raw = f"工具 `{call.name}` 执行异常：{type(exc).__name__}: {exc}"
            is_error, terminate = True, False

        text = _result_text(raw)
        if is_error:
            self.state.tool_errors += 1

        self._emit_tool_end(turn, call, text, is_error, terminate, started)
        return text, is_error, terminate

    def _record_tool_result(
        self,
        turn: int,
        call: ToolCallBlock,
        content: str,
        is_error: bool,
        terminate: bool = False,
    ) -> Dict[str, Any]:
        """写入规范历史，并返回给钩子/harness 用的富信息记录。

        注意两者是分开的：`state.messages` 必须保持 OpenAI 合法载荷，
        多出的 `is_error`/`terminate` 字段会让部分服务商直接拒绝请求。
        """
        text = f"[{'ERROR' if is_error else 'OK'}] {content}"
        self.state.add_tool_result(call.id, call.name, text)
        meta = self.state.record_tool_meta(call.id, call.name, is_error, terminate)
        return {
            "turn": turn,
            "id": call.id,
            "name": call.name,
            "content": text,
            "is_error": meta["is_error"],
            "terminate": meta["terminate"],
        }

    # ------------------------------------------------------------------
    # 事件
    # ------------------------------------------------------------------
    def _emit(self, event: Any) -> None:
        if self._on_event is None:
            return
        try:
            self._on_event(event)
        except Exception:  # noqa: BLE001 - 订阅者出错不能影响 Agent 运行
            pass


def _to_assistant_message(response: LLMResponse) -> AssistantMessage:
    """把 LLM 层的 LLMResponse 转成统一的 AssistantMessage。"""
    blocks: List[Any] = []
    if response.content:
        blocks.append(TextBlock(text=response.content))
    for call in response.tool_calls:
        blocks.append(
            ToolCallBlock(id=call.id, name=call.name, arguments=call.parsed_arguments())
        )

    stop_reason: Any = "tool_use" if response.tool_calls else "stop"
    if _finish_reason(response) == "length":
        # 输出被 token 上限截断。即使带了工具调用也必须改判，否则会用
        # 半截 JSON 参数执行工具（循环里有专门的分支拒绝执行）。
        stop_reason = "length"

    return AssistantMessage(
        content=blocks,
        stop_reason=stop_reason,
        usage=_usage_from(response.usage),
    )


def _finish_reason(response: LLMResponse) -> str:
    choices = (response.raw or {}).get("choices") or []
    if not choices:
        return ""
    return str(choices[0].get("finish_reason") or "")


def _usage_from(raw: Any) -> Usage:
    """兼容两种 usage 写法：OpenAI 原始字段，或已规范化的本层字段。

    评测 harness 会直接构造 Usage 来复现成本数据，因此不能只认 OpenAI 形状。
    """
    if not isinstance(raw, dict) or not raw:
        return Usage()
    if "input_tokens" in raw or "output_tokens" in raw:
        return Usage(
            input_tokens=int(raw.get("input_tokens") or 0),
            output_tokens=int(raw.get("output_tokens") or 0),
            cache_read_tokens=int(raw.get("cache_read_tokens") or 0),
            cache_write_tokens=int(raw.get("cache_write_tokens") or 0),
        )
    return Usage.from_openai(raw)
