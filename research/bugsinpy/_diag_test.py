#!/usr/bin/env python3
"""诊断：目标测试为什么不暴露这个 bug。"""
import subprocess
import sys
from pathlib import Path

REPO = Path.home() / "ws-f2p" / "youtube-dl"
VENV_BIN = Path.home() / "ws-f2p" / "venv" / "bin"


def sh(cmd, cwd=REPO):
    return subprocess.run(cmd, cwd=str(cwd), shell=True, capture_output=True, text=True, errors="replace")


def main() -> int:
    import os

    env = os.environ.copy()
    env["PATH"] = f"{VENV_BIN}{os.pathsep}" + env.get("PATH", "")

    print("=== 测试用例的源码 ===")
    result = subprocess.run(
        [str(VENV_BIN / "python"), "-c",
         "import inspect, test.test_utils as m; "
         "print(inspect.getsource(m.TestUtil.test_match_str))"],
        cwd=str(REPO), capture_output=True, text=True, errors="replace", env=env,
    )
    print(result.stdout or result.stderr)

    print("\n=== 该测试里与本 bug 相关的断言（filter / boolean）===")
    for line in (result.stdout or "").splitlines():
        low = line.lower()
        if "filter" in low or "true" in low or "false" in low or "match_str" in low:
            print("   ", line.strip())

    print("\n=== 直接手工验证 bug 行为（不经测试）===")
    probe = """
from youtube_dl.utils import match_str
import inspect
src = inspect.getsource(match_str)
# 复制 _match_one 里的布尔分支逻辑，确认当前实现的行为
from youtube_dl.utils import _match_one
try:
    print("  _match_one('', True, 'flag'): ", _match_one('', True, 'flag'))
except Exception as exc:
    print("  调用失败:", type(exc).__name__, exc)
try:
    print("  _match_one('', False, 'flag'):", _match_one('', False, 'flag'))
except Exception as exc:
    print("  调用失败:", type(exc).__name__, exc)
"""
    result = subprocess.run([str(VENV_BIN / "python"), "-c", probe], cwd=str(REPO),
                            capture_output=True, text=True, errors="replace", env=env)
    print(result.stdout or result.stderr)

    print("\n=== git 状态（确认在 buggy commit 且补丁未应用）===")
    print(sh("git log --oneline -1").stdout.strip())
    print(sh("git status --short").stdout.strip() or "  （工作区干净）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
