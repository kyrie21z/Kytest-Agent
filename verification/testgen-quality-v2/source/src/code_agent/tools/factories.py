"""工具集装配：变体之间**唯一**允许更换工具的开关点。

设计约束（对应开发计划的"原则 C：General Agent 保持真正通用"）：

- A0 只能拿到与任务无关的通用工具（读、写、列目录、检索、执行命令）。
  绝不允许内置 pytest 编排、覆盖率采集、变异测试这类**测试专用**能力——
  一旦内置，A0 就不再是通用 Agent，反事实对照失效。
- A0 完全可以用 `run_command` 自己跑 `pytest`。那是我们要观察的**涌现行为**，
  不是要禁止的行为；区别只在于"由谁触发"：模型自发 vs 系统确定性编排。

把装配集中到一个函数，还有一个具体理由：每个工具类的构造签名必须一致，
否则注册时才会崩（`ListFilesTool` 就曾因为缺 `__init__` 而接收不到 workspace）。
集中装配让这类问题在测试里一次性暴露。
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Sequence

from .base import Tool, ToolRegistry
from .code_tools import AnalyzeCodeTool, CheckSyntaxTool
from .file_tools import ListFilesTool, ReadFileTool, SearchCodeTool, WriteFileTool
from .shell_tools import RunCommandTool

# 通用编码 Agent 的工具集：与任务领域无关，任何软件工程任务都用得上。
# 搜索工具是有意保留的：它是通用代码检索能力（不含任何测试专用知识），
# 但没有它时模型会反复用 shell grep 代替，白白消耗 turn——而 turn 是实验的主成本单位。
#
# `run_command` 是这套工具里唯一能"与代码交互"的能力：没有它，模型只能读写文件，
# 无法验证自己写的东西能不能跑。它也是"A0 会不会自发运行 pytest"这一观察项的前提。
GENERAL_TOOL_NAMES: tuple = (
    "read_file",
    "write_file",
    "list_files",
    "search_code",
    "run_command",
)

# 代码静态分析工具。属于通用能力，但**不属于 A0 的最小工具集**：
# 它们是代码审查方向的遗留，A1 及以后的变体若需要可以显式开启。
ANALYSIS_TOOL_NAMES: tuple = (
    "check_syntax",
    "analyze_code",
)

_BUILDERS: Dict[str, Any] = {
    "read_file": ReadFileTool,
    "write_file": WriteFileTool,
    "list_files": ListFilesTool,
    "search_code": SearchCodeTool,
    "run_command": RunCommandTool,
    "check_syntax": CheckSyntaxTool,
    "analyze_code": AnalyzeCodeTool,
}


def build_tool(settings: Any, name: str) -> Tool:
    """按名字构造单个工具。名字非法时立即报错，不留到运行时才炸。"""
    # Lazy import: the generic tool registry remains free of testing policy.
    if name == "submit_tests":
        from ..testgen import SubmitTestsTool
        return SubmitTestsTool(settings)
    if name == "inspect_survivors":
        from ..fault_feedback import InspectSurvivorsTool
        return InspectSurvivorsTool(settings)
    builder = _BUILDERS.get(name)
    if builder is None:
        raise KeyError(f"未知工具 `{name}`，可用工具：{', '.join(sorted(_BUILDERS))}")
    return builder(settings)


def build_registry(
    settings: Any,
    tool_names: Optional[Sequence[str]] = None,
) -> ToolRegistry:
    """按名字列表装配工具注册表。

    Args:
        settings: 全局配置；工具从它读取 workspace 与各项限制。
        tool_names: 需要的工具名，默认为通用工具集。

    Raises:
        KeyError: 出现未注册的工具名。构造期失败优于运行期失败——
            评测跑完 30 个实例才发现工具名写错，代价是整轮实验。
    """
    names = list(tool_names) if tool_names is not None else list(GENERAL_TOOL_NAMES)
    registry = ToolRegistry()
    for name in names:
        registry.register(build_tool(settings, name))
    inspector = registry.get("inspect_survivors")
    if inspector is not None:
        inspector.submitter = registry.get("submit_tests")
        if inspector.submitter is not None:
            inspector.submitter.inspector = inspector
    return registry


def available_tool_names() -> List[str]:
    """返回所有可装配的工具名，便于 CLI 校验与文档生成。"""
    return sorted([*_BUILDERS, "submit_tests", "inspect_survivors"])
