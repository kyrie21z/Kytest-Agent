"""工具抽象层：Tool 基类、ToolResult、注册表与路径沙箱。

设计要点：
- 每个工具自描述 JSON Schema，可直接转换为 OpenAI Function Calling 的 tools 参数；
- 注册表统一做参数校验、异常兜底与输出截断，单个工具出错不会中断 Agent 循环；
- 所有文件路径必须位于 workspace 内，防止提示注入导致的越权访问。
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from ..errors import ToolError

MAX_TOOL_OUTPUT_CHARS = 6000


def truncate(text: str, limit: int = MAX_TOOL_OUTPUT_CHARS) -> str:
    """截断过长输出，避免占满上下文窗口（保留开头，简单可预期）。"""
    text = text if isinstance(text, str) else str(text)
    if len(text) <= limit:
        return text
    return text[:limit] + f"\n...（输出过长已截断，原始长度 {len(text)} 字符）"


def truncate_middle(text: str, limit: int, head_ratio: float = 0.6) -> str:
    """保留头尾地截断输出，中间插入省略标记。

    命令输出用这个而不是 `truncate`：构建/测试输出的**关键信息在末尾**
    （失败摘要、错误堆栈、退出原因），只留开头会把这些全丢掉。
    """
    text = text if isinstance(text, str) else str(text)
    if limit <= 0 or len(text) <= limit:
        return text
    head = max(1, int(limit * head_ratio))
    tail = max(1, limit - head)
    dropped = len(text) - head - tail
    if dropped <= 0:
        return text
    return f"{text[:head]}\n...（此处省略 {dropped} 字符）...\n{text[-tail:]}"


def resolve_workspace_path(workspace: Path, raw: Any, must_exist: bool = False) -> Path:
    """把用户/模型给出的路径解析到工作区内，越界直接抛出 ToolError。"""
    if raw is None or not str(raw).strip():
        raise ToolError("路径参数不能为空")
    root = Path(workspace).expanduser().resolve()
    candidate = Path(str(raw).strip()).expanduser()
    if not candidate.is_absolute():
        candidate = root / candidate
    try:
        resolved = candidate.resolve()
    except OSError as exc:  # 某些非法路径在 Windows 上会直接抛 OSError
        raise ToolError(f"无法解析路径 `{raw}`：{exc}") from exc
    try:
        inside = resolved == root or resolved.is_relative_to(root)
    except AttributeError:  # Python 3.8 兼容
        inside = os.path.commonpath([str(resolved), str(root)]) == str(root)
    if not inside:
        raise ToolError(f"路径越界：`{raw}` 不在工作区 `{root}` 内")
    if must_exist and not resolved.exists():
        raise ToolError(f"路径不存在：`{raw}`")
    return resolved


@dataclass
class ToolResult:
    """工具执行结果。

    **不在这里做观察结果格式化。** `[OK]/[ERROR]` 这类协议标记由 Agent 循环
    统一添加（`agent/core.py` 的 `_result_text` / `_record_tool_result`）。
    原因：注册表只是工具的一种调用入口，直接调用 `tool.run()` 的代码不会经过
    `to_observation()`，两处各自格式化会导致前缀重复（真实发生过）。

    `terminate` 对应 Pi 的 `AgentToolResult.terminate`（`types.ts:424-446`）：
    工具可以请求"这批工具跑完后就结束本次 run"。Agent 循环只在**整批**工具
    都要求终止时才提前结束，避免单个工具劫持整轮对话。
    """

    ok: bool
    content: str
    terminate: bool = False

    @classmethod
    def success(cls, content: str, terminate: bool = False) -> "ToolResult":
        return cls(True, content, terminate)

    @classmethod
    def failure(cls, content: str, terminate: bool = False) -> "ToolResult":
        return cls(False, content, terminate)


class Tool(ABC):
    """所有工具的基类。

    `__init__` 同时接受两种入参：全局 `Settings` 对象，或直接的 workspace 路径。
    统一在这里处理而不是让每个子类各写一遍——否则漏写 `__init__` 的子类会
    悄悄继承 `(workspace)` 签名，直到装配时才崩（`ListFilesTool` 真实踩过这个坑）。
    """

    name: str = "tool"
    description: str = ""
    parameters: Dict[str, Any] = {"type": "object", "properties": {}, "required": []}

    def __init__(self, settings_or_workspace: Any = None) -> None:
        raw = getattr(settings_or_workspace, "workspace", settings_or_workspace)
        self.workspace = Path(raw).expanduser().resolve() if raw else Path.cwd().resolve()
        self.settings = settings_or_workspace

    def schema(self) -> Dict[str, Any]:
        """转换为 OpenAI Function Calling 工具格式。"""
        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }

    @abstractmethod
    def run(self, **kwargs: Any) -> ToolResult:
        """执行工具逻辑；实现方可以抛出 ToolError 表达可预期的失败。"""

    def describe(self) -> str:
        return f"{self.name}: {self.description}"


def _type_label(value: Any) -> str:
    """返回给错误信息看的实际类型名。"""
    if isinstance(value, bool):
        return "boolean"
    if isinstance(value, str):
        return "string"
    if isinstance(value, int):
        return "integer"
    if isinstance(value, float):
        return "number"
    if isinstance(value, list):
        return "array"
    if isinstance(value, dict):
        return "object"
    return type(value).__name__


def _matches_schema_type(value: Any, declared: Any) -> bool:
    """按 JSON Schema 的 type 字段校验单个值。

    两条来自真实缺陷的规则：
    - bool 是 int 的子类：声明 integer 时必须显式排除 bool，否则 `True`
      会被当成 1 通过校验；
    - 字符串 "false" 是非空字符串、为真值：声明 boolean 时绝不能让字符串
      混过校验——`overwrite="false"` 会变成"允许覆盖"（实际发生过）。
    """
    declared = declared or ""
    if declared == "boolean":
        return isinstance(value, bool)
    if declared == "string":
        return isinstance(value, str)
    if declared == "integer":
        return isinstance(value, int) and not isinstance(value, bool)
    if declared == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    if declared == "array":
        return isinstance(value, list)
    if declared == "object":
        return isinstance(value, dict)
    return True  # 未声明类型的参数不做校验


class ToolRegistry:
    """工具注册表：管理工具的生命周期，并统一执行入口。"""

    def __init__(self) -> None:
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool) -> Tool:
        self._tools[tool.name] = tool
        return tool

    def get(self, name: str) -> Tool:
        return self._tools.get(name, None)  # type: ignore[return-value]

    @property
    def tools(self) -> List[Tool]:
        return list(self._tools.values())

    def names(self) -> List[str]:
        return sorted(self._tools)

    def schemas(self) -> List[Dict[str, Any]]:
        return [tool.schema() for tool in self._tools.values()]

    def execute(self, name: str, arguments: Dict[str, Any]) -> ToolResult:
        """执行工具；所有异常都会被转换为 ToolResult(ok=False)，保证循环不中断。"""
        tool = self.get(name)
        if tool is None:
            return ToolResult.failure(f"未知工具 `{name}`。可用工具：{', '.join(self.names())}")
        if arguments is None:
            arguments = {}
        if not isinstance(arguments, dict):
            return ToolResult.failure("参数必须是 JSON 对象，例如 {\"path\": \"a.py\"}")

        # 参数在传输中被截断时，`parsed_arguments()` 会给出明确诊断。
        # 必须在这里优先返回它：否则用户看到的会是"缺少必填参数"这种
        # 指向性很弱的报错，模型会误以为是自己漏了字段而反复重试同一个大调用。
        malformed = arguments.get("_malformed")
        if isinstance(malformed, str) and malformed:
            return ToolResult.failure(str(malformed))

        properties = (tool.parameters.get("properties") or {})
        required = [key for key in tool.parameters.get("required", []) if arguments.get(key) in (None, "")]
        if required:
            return ToolResult.failure(f"缺少必填参数：{', '.join(required)}")
        unknown = [key for key in arguments if properties and key not in properties]
        if unknown:
            return ToolResult.failure(
                f"存在未知参数：{', '.join(unknown)}（可用参数：{', '.join(sorted(properties)) or '无'}）"
            )
        # 类型校验必须在 tool.run() 之前：带副作用的工具（写文件、执行命令）
        # 不能在非法参数下被调用——`overwrite: "false"` 是非空字符串、为真值，
        # 曾经把"禁止覆盖"骗成"允许覆盖"。
        for key, value in arguments.items():
            declared = (properties.get(key) or {}).get("type")
            if not _matches_schema_type(value, declared):
                return ToolResult.failure(
                    f"参数 `{key}` 必须是 {declared}，收到 {_type_label(value)}（值：{str(value)[:50]}）"
                )

        try:
            result = tool.run(**arguments)
        except ToolError as exc:
            return ToolResult.failure(str(exc))
        except Exception as exc:  # noqa: BLE001 - 兜底，避免工具异常打断 Agent
            return ToolResult.failure(f"工具 `{name}` 执行异常：{type(exc).__name__}: {exc}")
        if not isinstance(result, ToolResult):
            result = ToolResult.success(str(result))
        return ToolResult(result.ok, truncate(result.content))