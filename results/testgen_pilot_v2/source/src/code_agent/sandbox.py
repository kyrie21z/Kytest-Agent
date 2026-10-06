"""模型命令的文件及网络边界；隔离不可用时拒绝执行，不回落到宿主机。"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path
from typing import List, Sequence


class SandboxUnavailable(ValueError):
    pass


def sandbox_command(
    argv: Sequence[str], *, workspace: Path, cwd: Path, allow_write: bool
) -> List[str]:
    """Linux Bubblewrap：工作区 + 只读系统/Python 运行库 + 私有临时目录。

    运行库属于明确允许的工作区外路径。不会挂载整个 /、/home、/mnt 或
    宿主机 /tmp；不会继承宿主机网络、PID 命名空间或可提升权限的能力。
    """
    executable = shutil.which("bwrap") if sys.platform == "linux" else None
    if not executable:
        raise SandboxUnavailable(
            "命令隔离不可用：需要 Linux 和 Bubblewrap（bwrap）。"
            "命令未执行；仅对受信代码可显式选择 --execution-mode trusted。"
        )

    roots = [Path(p) for p in ("/usr", "/bin", "/lib", "/lib64") if Path(p).exists()]
    # Python/venv 的依赖必须能加载，只暴露这两个实际安装目录。
    for prefix in (sys.base_prefix, sys.prefix):
        root = Path(prefix).resolve()
        if not any(root == p or p in root.parents for p in roots):
            roots.append(root)
    workspace = workspace.resolve()
    for root in roots:
        if workspace == root or workspace in root.parents or root in workspace.parents:
            raise SandboxUnavailable("工作区与只读运行库重叠，请使用独立的项目目录。")

    command = [
        executable, "--unshare-all", "--die-with-parent", "--new-session",
        "--cap-drop", "ALL", "--proc", "/proc", "--dev", "/dev",
        "--tmpfs", "/tmp", "--tmpfs", "/run",
    ]
    for root in roots:
        command.extend(["--ro-bind", str(root), str(root)])
    for filename in ("/etc/ld.so.cache", "/etc/localtime"):
        if Path(filename).exists():
            command.extend(["--ro-bind", filename, filename])
    command.extend([
        "--bind" if allow_write else "--ro-bind", str(workspace), str(workspace),
        "--chdir", str(cwd), "--setenv", "HOME", "/tmp",
        "--setenv", "TMPDIR", "/tmp", "--", *argv,
    ])
    return command
