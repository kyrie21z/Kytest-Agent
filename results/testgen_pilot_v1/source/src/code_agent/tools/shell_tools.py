"""命令执行工具：A0 唯一的"能与代码交互"的通用能力。

它存在的理由有两层：

1. **工程上**：没有它，Agent 只能读写文件，无法验证自己写的东西能不能跑。
   模型写测试却不执行，等同于凭猜测断言。
2. **实验上**：它是"A0 会不会自发运行 pytest"这一观察项的**前提**。A0 拿到的是
   通用 shell，不是测试编排；它自己决定要不要跑测试，这个行为本身是数据。

设计约束（对应开发计划的"原则 C"）：

- 本工具**不含任何测试专用知识**：不识别 pytest、不解析测试结果、不做自动重试。
  它只负责"执行命令并把真实输出带回来"，判断与编排留给模型自己。
- 命令**不经过 shell**：`;`、`&&`、`|`、反引号都没有特殊含义。这既排除了注入面，
  也让"Agent 到底执行了什么"在轨迹里可以逐参数核对。
- 超时、输出采集上限、工作目录边界都在这里强制，不由模型自行决定。

权限边界：默认使用 Bubblewrap 限制文件挂载并隔离网络；不可用时拒绝执行。
ALLOW_WRITE=false 使工作区只读；显式 trusted 模式具有宿主机权限，不能强制
只读时拒绝执行。环境白名单、输出上限及破坏性命令护栏继续生效。

"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from ..proc import IS_WINDOWS, run_process, split_command
from ..sandbox import SandboxUnavailable, sandbox_command
from .base import Tool, ToolResult, resolve_workspace_path, truncate_middle

# 命令输出的字符上限。超出部分保留头尾，因为失败信息通常在末尾。
MAX_OUTPUT_CHARS = 8000
# 采集阶段的上限（字符，stdout+stderr 合计）。达到后继续排空管道但丢弃内容，
# 防止 `cat` 一个巨大文件把内存打满——展示层截断不等于采集层限制。
MAX_CAPTURE_CHARS = 400_000
# 单次命令允许的最长超时，防止模型用超大 timeout 绕过整体预算控制。
MAX_TIMEOUT_SEC = 300

# 明显破坏性的命令直接拒绝。这不是安全边界，而是防误操作的护栏：
# 权限边界由 sandbox_command 的挂载和命名空间配置负责。
_DENY_PATTERNS = (
    "rm -rf /",
    "rm -rf ~",
    "mkfs",
    "diskpart",
    "format c:",
    ":(){:|:&};:",
    "shutdown",
    "reboot",
)


def _is_denied(command: str) -> Optional[str]:
    lowered = command.lower()
    for pattern in _DENY_PATTERNS:
        if pattern in lowered:
            return pattern
    return None


def _describe_exit(result) -> str:
    if result.error:
        return f"启动失败：{result.error}"
    if result.timed_out:
        return "已超时并被终止"
    return f"退出码 {result.exit_code}"


def _format(result, argv: List[str], timeout: float) -> ToolResult:
    """把进程结果格式化成给模型看的观察结果。"""
    header_lines = [
        f"$ {' '.join(argv)}",
        f"[{_describe_exit(result)}｜耗时 {result.duration_sec:.2f}s｜超时上限 {timeout:g}s]",
    ]
    if result.timed_out:
        header_lines.append(
            "命令在超时上限内没有结束，已连同其子进程一起终止。"
            "若确实需要更长时间，可提高 timeout；否则请检查是否进入了交互式等待或死循环。"
        )
    if result.output_truncated:
        header_lines.append(
            f"输出超过采集上限（{MAX_CAPTURE_CHARS} 字符），超出部分已丢弃；以上仅为可得部分。"
        )

    body: List[str] = []
    if result.stdout.strip():
        body.append("--- stdout ---\n" + result.stdout.rstrip())
    if result.stderr.strip():
        body.append("--- stderr ---\n" + result.stderr.rstrip())
    if not body:
        body.append("（命令没有产生任何输出）")

    text = truncate_middle("\n".join(header_lines + body), MAX_OUTPUT_CHARS)
    if result.error or result.timed_out or result.exit_code != 0:
        return ToolResult.failure(text)
    return ToolResult.success(text)


class RunCommandTool(Tool):
    name = "run_command"
    description = (
        "在工作区内执行一条命令并返回真实输出。命令不经过 shell，"
        "因此管道、重定向与 `&&` 等元字符无效；需要多个动作时请分多次调用。"
        "常见的用法是运行脚本或测试（例如 `python -m pytest -q`）。"
        "命令会被强制超时并在超时后终止整个进程树。"
        "子进程环境只包含系统必需变量（PATH 等），不包含 API Key 等父进程配置；"
        "输出超过采集上限的部分会被丢弃。默认在文件与网络隔离环境中执行；"
        "隔离不可用时返回错误，trusted 模式仅供受信本机代码使用。"
    )
    parameters: Dict[str, Any] = {
        "type": "object",
        "properties": {
            "command": {
                "type": "string",
                "description": "要执行的命令，例如 `python -m pytest -q` 或 `python solution.py`",
            },
            "cwd": {
                "type": "string",
                "description": "相对工作区的执行目录，默认工作区根目录",
            },
            "timeout": {
                "type": "number",
                "description": f"超时秒数，默认取配置值，上限 {MAX_TIMEOUT_SEC}",
            },
        },
        "required": ["command"],
    }

    def __init__(self, settings: Any) -> None:
        super().__init__(settings)
        self.allow_execution = bool(getattr(settings, "allow_code_execution", True))
        self.execution_mode = getattr(settings, "execution_mode", "sandbox")
        self.allow_write = bool(getattr(settings, "allow_write", True))
        self.default_timeout = float(getattr(settings, "exec_timeout", 10) or 10)

    def run(
        self,
        command: str,
        cwd: str = ".",
        timeout: Optional[float] = None,
        **_: Any,
    ) -> ToolResult:
        if not self.allow_execution:
            return ToolResult.failure("命令执行已被配置禁用（ALLOW_CODE_EXECUTION=false）")
        if self.execution_mode == "disabled":
            return ToolResult.failure("命令执行已被配置禁用（EXECUTION_MODE=disabled）")
        if self.execution_mode not in {"sandbox", "trusted"}:
            return ToolResult.failure("未知命令执行策略，命令未执行")
        if self.execution_mode == "trusted" and not self.allow_write:
            return ToolResult.failure("trusted 模式无法保证只读；ALLOW_WRITE=false 时拒绝执行命令")

        raw = (command or "").strip()
        if not raw:
            return ToolResult.failure("命令不能为空")

        denied = _is_denied(raw)
        if denied:
            return ToolResult.failure(
                f"该命令被安全护栏拒绝（匹配到 `{denied}`）。这只影响明显破坏性的操作。"
            )

        argv = split_command(raw)
        if not argv:
            return ToolResult.failure("命令解析后为空，请检查引号是否配对")

        try:
            workdir = resolve_workspace_path(self.workspace, cwd or ".", must_exist=True)
        except Exception as exc:  # ToolError：路径越界或不存在
            return ToolResult.failure(f"执行目录不可用：{exc}")
        if not workdir.is_dir():
            return ToolResult.failure(f"`{cwd}` 不是目录")

        effective_timeout = _clamp_timeout(timeout, self.default_timeout)

        # 工作区保持干净：不写 .pyc，避免被测仓库多出 __pycache__ 污染快照。
        env = {
            "PYTHONDONTWRITEBYTECODE": "1",
            "PYTHONIOENCODING": "utf-8",
            "PYTHONUNBUFFERED": "1",
        }

        execution_argv = argv
        if self.execution_mode == "sandbox":
            # 在启动前检查缺失的程序，保持可定位的错误反馈。
            import shutil
            program = argv[0]
            if os.path.dirname(program) and not os.path.isabs(program):
                program = str(workdir / program)
            if shutil.which(program) is None:
                return ToolResult.failure(f"启动失败：找不到可执行文件：{argv[0]}")
            try:
                execution_argv = sandbox_command(
                    argv, workspace=self.workspace, cwd=workdir, allow_write=self.allow_write,
                )
            except SandboxUnavailable as exc:
                return ToolResult.failure(str(exc))
        result = run_process(
            execution_argv, cwd=workdir, timeout=effective_timeout, env=env,
            output_char_cap=MAX_CAPTURE_CHARS,
        )
        return _format(result, argv, effective_timeout)


def _clamp_timeout(requested: Optional[float], default: float) -> float:
    """钳制超时：模型给的值只能落在 [0.5, MAX_TIMEOUT_SEC] 内。"""
    try:
        value = float(requested) if requested is not None else float(default)
    except (TypeError, ValueError):
        value = float(default)
    if value <= 0:
        value = float(default)
    return max(0.5, min(value, float(MAX_TIMEOUT_SEC)))


def platform_hint() -> str:
    """给 CLI/文档用的平台提示。"""
    return "Windows（PowerShell 语义，但命令不经过 shell）" if IS_WINDOWS else "POSIX"
