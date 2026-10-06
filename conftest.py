"""让 `pytest` 直接可用，无需先 `pip install -e .`。

把 `src/` 加入 sys.path，因此测试在源码检出状态下即可运行——这是"5 分钟可运行"
这条硬性要求的组成部分。
"""
from __future__ import annotations

import sys
from pathlib import Path

SRC = Path(__file__).resolve().parent / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))
