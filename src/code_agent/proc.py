"""进程执行层：带超时、进程树清理与输出采集的子进程运行器。

为什么单独成模块而不是塞进工具里：**超时与进程树清理是最容易出错、也最难在
集成测试里复现的部分**。把它抽成纯函数后，可以直接用 `time.sleep` 写确定性测试。

三个必须处理的问题：

1. **超时后必须杀掉整棵进程树。** `subprocess` 的 timeout 只终止直接子进程。
   以 `python -m pytest` 为例，pytest 会再 fork 出自己；只杀父进程会留下孤儿进程
   持续占用 CPU，在并行评测 30 个实例时直接拖垮机器。Windows 上用
   `taskkill /T /F`，POSIX 上用进程组。
2. **readline 阻塞会导致超时永不触发。** 典型写法 `for line in proc.stdout` 在子进程
   不换行地持续输出时会卡死，超时逻辑根本没机会执行。这里用后台收集线程 +
   `join(timeout)`，让超时始终由主线程掌控。
3. **仓库工作区必须保持干净。** 评测时工作区是"被测代码 + Agent 产物"，多出
   `__pycache__` 会污染快照与后续比对，因此默认禁止写字节码缓存。
"""
from __future__ import annotations

import os
import re
import shlex
import signal
import subprocess
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Sequence

IS_WINDOWS = os.name == "nt"

# 杀进程树时等待其退出的时间上限。超时后仍会继续清理，不阻塞主流程。
_KILL_WAIT_SEC = 5.0
_DRAIN_JOIN_SEC = 2.0
# 采集线程的单次读取块大小（字符）。这是"无换行持续输出"场景下
# 单次内存分配的上界——readline() 在该场景下没有上界。
_CHUNK_CHARS = 65_536


@dataclass
class ProcResult:
    """一次命令执行的完整结果，不抛异常——失败通过字段表达。"""

    argv: List[str] = field(default_factory=list)
    exit_code: Optional[int] = None
    stdout: str = ""
    stderr: str = ""
    timed_out: bool = False
    # 输出采集达到上限后被丢弃。上限在**采集阶段**强制，而不是只在展示层截断——
    # 否则 `cat` 一个巨大文件仍会把原始输出全部吞进内存。
    output_truncated: bool = False
    duration_sec: float = 0.0
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.error is None and not self.timed_out and self.exit_code == 0


# 子进程环境白名单：只传运行必需的系统变量，**不继承父进程的其余环境**。
# 父进程环境里可能带着 API Key 等敏感值（.env 会加载进 os.environ），
# 原样继承等于把凭据交给模型执行的任意命令读取。
CHILD_ENV_ALLOWLIST = (
    "PATH", "PATHEXT", "SYSTEMROOT", "SYSTEMDRIVE", "COMSPEC", "WINDIR",
    "TEMP", "TMP", "TMPDIR", "HOME", "USERPROFILE", "APPDATA", "LOCALAPPDATA",
    "LANG", "LC_ALL", "PYTHONIOENCODING", "PYTHONUNBUFFERED",
    "PYTHONDONTWRITEBYTECODE", "PYTHONPATH", "VIRTUAL_ENV",
)


def build_child_env(overlay: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    """按白名单构造子进程环境：白名单变量（若存在于父环境）+ 显式 overlay。"""
    env: Dict[str, str] = {}
    for key in CHILD_ENV_ALLOWLIST:
        value = os.environ.get(key)
        if value is not None:
            env[key] = value
    if overlay:
        env.update(overlay)
    return env


def run_capture(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout: float,
    env: Optional[Dict[str, str]] = None,
    execution_mode: str = "sandbox",
) -> ProcResult:
    """按执行策略运行命令，保留采集上限、启动错误等全部进程事实。

    评测层需要"跑一个命令、拿到输出与退出码"，这个封装让它们复用同一套
    超时与进程树清理逻辑，而不是各自写一遍 `subprocess.run`——
    后者在超时后会留下孤儿进程，批量评测时是机器级故障。
    """
    # 评测器执行的是模型生成的测试，也必须隔离；它不能成为工具边界的旁路。
    directory = Path(cwd).resolve()
    command = list(argv)
    if execution_mode == "sandbox":
        from .sandbox import SandboxUnavailable, sandbox_command
        try:
            command = sandbox_command(argv, workspace=directory, cwd=directory, allow_write=True)
        except SandboxUnavailable as exc:
            return ProcResult(argv=list(argv), error=str(exc))
    elif execution_mode != "trusted":
        return ProcResult(argv=list(argv), error="命令执行已禁用或策略无效")
    return run_process(command, cwd=directory, timeout=timeout, env=env)


def split_command(command: str) -> List[str]:
    """把命令字符串切成 argv。

    平台差异是真实存在的，不能靠一个解析器通吃：

    - POSIX 用 `shlex.split`（POSIX 规则）；
    - Windows 不能用 `shlex(posix=False)`——它会**把引号原样保留**在 token 里，
      于是 `python "C:\\a b\\s.py"` 会把带引号的字符串当成路径传给子进程，必然失败。
      Windows 的规则也不是 POSIX：反斜杠只在引号前才有特殊含义。

    Windows 分两步，且两步都只依赖系统 API，不做字符串位置推算：

    1. 用 `CommandLineToArgvW` 解析出全部 token（引号已由系统剥掉）；
    2. 逐个 token 计算"规范化引用形式"，拼接后**重新解析**，返回 `[1:]`。

    为什么不能像常见写法那样"找到 argv[0] 的位置后切掉再递归"：`str.find` 会匹配到
    引号**内部**的同名文本。例如 `"C:\\tmp\\a b\\x.py" --flag` 中，argv[0] 出现在
    引号内的下标 1 处，切出来的剩余字符串是 `" --flag`，从引号中间断开，
    后续解析全部错位。逐 token 重建没有这个问题。
    """
    text = (command or "").strip()
    if not text:
        return []

    if IS_WINDOWS:
        tokens = _argv_w(text)
        if not tokens:
            return text.split()
        if len(tokens) == 1:
            return [tokens[0]]
        rebuilt = " ".join(_quote_arg(token) for token in tokens)
        reparsed = _argv_w(rebuilt)
        if len(reparsed) == len(tokens):
            return reparsed
        return tokens  # 重建失败时退回原始切分，仍然可用

    try:
        return shlex.split(text)
    except ValueError:
        # 引号不配对时退化为按空白切分，让命令仍能执行（由子进程报错更清晰）
        return text.split()


def _quote_arg(value: str) -> str:
    """把一个 token 转成"重新解析后仍是同一个 token"的引用形式。

    只有两种情况需要加引号：含空白，或含引号本身（此时引号需按 Windows 规则转义）。
    这样像 `--flag` 这类普通参数会原样保留，避免无意义的引号干扰轨迹可读性。
    """
    if not value or re.search(r'[\s"]', value):
        escaped = value.replace('"', '\\"')
        return f'"{escaped}"'
    return value


def _argv_w(text: str) -> List[str]:
    """调用系统 API 解析命令行，返回与 C 运行时会交给子进程的同一份 argv。"""
    try:
        import ctypes
        from ctypes import wintypes

        function = ctypes.windll.shell32.CommandLineToArgvW  # type: ignore[attr-defined]
        function.argtypes = [wintypes.LPCWSTR, ctypes.POINTER(ctypes.c_int)]
        function.restype = ctypes.POINTER(wintypes.LPWSTR)

        count = ctypes.c_int(0)
        pointer = function(text, ctypes.byref(count))
        if not pointer:
            return []
        try:
            return [pointer[index] for index in range(count.value)]
        finally:
            ctypes.windll.kernel32.LocalFree(pointer)  # type: ignore[attr-defined]
    except (AttributeError, OSError, ValueError):
        return []


def _popen_kwargs() -> Dict[str, Any]:
    """按平台构造安全且不弹窗的启动参数。"""
    if IS_WINDOWS:
        # CREATE_NO_WINDOW：避免在 GUI/无控制台环境下弹出黑框。
        return {"creationflags": getattr(subprocess, "CREATE_NO_WINDOW", 0)}
    # start_new_session：让子进程自成进程组，便于整组终止。
    return {"start_new_session": True}


def _kill_process_tree(pid: int) -> Optional[str]:
    """终止 pid 及其全部后代。返回错误信息（正常情况下为 None）。"""
    try:
        if IS_WINDOWS:
            subprocess.run(
                ["taskkill", "/F", "/T", "/PID", str(pid)],
                capture_output=True,
                timeout=_KILL_WAIT_SEC,
                creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0),
            )
        else:
            os.killpg(os.getpgid(pid), signal.SIGKILL)
    except (OSError, subprocess.SubprocessError) as exc:
        return f"{type(exc).__name__}: {exc}"
    return None


class _CaptureBudget:
    """stdout/stderr 共享的采集预算：达到上限后继续排空管道但丢弃内容。

    继续排空是必须的——停掉读取会让子进程因管道写满而阻塞，超时控制随之失效。
    按字符数近似计量（内存防护目的，不追求精确字节数）。
    """

    def __init__(self, cap: int) -> None:
        self.cap = max(0, int(cap))
        self.remaining = self.cap
        self.truncated = False
        self._lock = threading.Lock()

    def take(self, text: str) -> str:
        with self._lock:
            if self.remaining <= 0:
                self.truncated = True
                return ""
            allowed = text[: self.remaining]
            if len(allowed) < len(text):
                self.truncated = True
            self.remaining -= len(allowed)
            return allowed


def _collect(stream, sink: List[str], budget: _CaptureBudget) -> None:
    """后台线程：定长块读取管道，超预算部分丢弃但仍持续排空。

    用 `read(_CHUNK_CHARS)` 而不是 `readline()`：后者会把"没有换行符的持续
    输出"整行读进内存——8MiB 不换行输出就是 8MiB 的单次分配；块读的每次
    分配恒为块大小。TextIOWrapper 的增量解码保持跨块 UTF-8 字符完整。
    """
    try:
        for chunk in iter(lambda: stream.read(_CHUNK_CHARS), ""):
            kept = budget.take(chunk)
            if kept:
                sink.append(kept)
    except (ValueError, OSError):
        pass
    finally:
        try:
            stream.close()
        except (ValueError, OSError):
            pass


def run_process(
    argv: Sequence[str],
    *,
    cwd: Path,
    timeout: float,
    env: Optional[Dict[str, str]] = None,
    output_char_cap: int = 2_000_000,
) -> ProcResult:
    """执行命令并保证在超时后清理整棵进程树。

    Args:
        argv: 已切分好的参数列表。**不经过 shell**，因此 `;`、`&&`、`|` 等
            元字符没有特殊含义，注入面被结构性排除。
        cwd: 工作目录。
        timeout: 秒。必须为正数；调用方负责范围钳制。
        env: 追加/覆盖的环境变量（叠加在白名单环境之上；父进程环境的
            其余变量——包括可能的 API Key——不会传给子进程）。
        output_char_cap: stdout+stderr 合计的采集上限（字符）。超限部分
            仍被排空但丢弃，`output_truncated` 置位。
    """
    result = ProcResult(argv=list(argv))
    if not argv:
        result.error = "命令为空"
        return result

    started = time.monotonic()
    child_env = build_child_env(env)

    try:
        process = subprocess.Popen(
            list(argv),
            cwd=str(cwd),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=child_env,
            **_popen_kwargs(),
        )
    except FileNotFoundError:
        result.error = f"找不到可执行文件：{argv[0]}"
        result.duration_sec = time.monotonic() - started
        return result
    except (OSError, ValueError) as exc:
        result.error = f"无法启动进程：{type(exc).__name__}: {exc}"
        result.duration_sec = time.monotonic() - started
        return result

    stdout_chunks: List[str] = []
    stderr_chunks: List[str] = []
    budget = _CaptureBudget(output_char_cap)
    assert process.stdout is not None and process.stderr is not None
    readers = [
        threading.Thread(target=_collect, args=(process.stdout, stdout_chunks, budget), daemon=True),
        threading.Thread(target=_collect, args=(process.stderr, stderr_chunks, budget), daemon=True),
    ]
    for reader in readers:
        reader.start()

    deadline = started + max(0.1, float(timeout))
    try:
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                result.timed_out = True
                kill_error = _kill_process_tree(process.pid)
                if kill_error:
                    result.error = f"超时后终止进程失败：{kill_error}"
                break
            try:
                process.wait(timeout=min(0.25, remaining))
                break
            except subprocess.TimeoutExpired:
                continue
    except BaseException:
        # Ctrl-C 也必须清理正在执行的进程树，再交给 CLI/Agent 收尾。
        _kill_process_tree(process.pid)
        process.wait(timeout=_KILL_WAIT_SEC)
        for reader in readers:
            reader.join(_DRAIN_JOIN_SEC)
        raise

    if result.timed_out:
        try:
            process.wait(timeout=_KILL_WAIT_SEC)
        except subprocess.TimeoutExpired:
            result.error = result.error or "终止后进程仍未退出"

    for reader in readers:
        reader.join(_DRAIN_JOIN_SEC)

    result.duration_sec = time.monotonic() - started
    result.stdout = "".join(stdout_chunks)
    result.stderr = "".join(stderr_chunks)
    result.output_truncated = budget.truncated
    if result.timed_out:
        result.exit_code = None
    else:
        result.exit_code = process.returncode
    return result
