"""项目入口：`python main.py [参数]`。

不做 `pip install` 也能直接跑，方便评审与演示。安装之后同样可以用
`code-agent [参数]`（见 pyproject.toml 的 console script 声明）。

用法示例：
    python main.py                                    交互模式
    python main.py --print "为 solution.py 生成单元测试"
    python main.py --mock                             离线演示，不需要 API Key
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "src"))

from code_agent.cli import main  # noqa: E402

if __name__ == "__main__":
    raise SystemExit(main())
