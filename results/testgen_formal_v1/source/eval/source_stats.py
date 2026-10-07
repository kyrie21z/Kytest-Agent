"""被测代码的可执行行数：用 AST 独立计算，不依赖覆盖率工具。

存在的理由是一个真实的坑：当测试文件导入失败时，`coverage` 只把 `def` 这一条语句
算作可执行行，函数体根本没被计入，于是报告 `executable_lines=1, percent=100%`。
也就是说**"测量失败"伪装成了"测了满分"**。

用一个独立于覆盖率工具的口径（AST 语句数）做交叉校验，就能识破这种情况：
真跑起来时两者数量级一致；导入失败时覆盖率的口径会小得离谱。
测量仪器需要这种"第二意见"，否则错误会静默地变成数据。
"""
from __future__ import annotations

import ast
from pathlib import Path

# 覆盖率口径与 AST 口径的允许偏差。coverage 会把多行语句、隐式分支算得更细，
# 因此这里只用它识别"数量级不符"的退化情况，不要求严格相等。
_MIN_RATIO = 0.5


def executable_statements(source: str) -> int:
    """统计源码里的可执行语句数（AST 口径）。

    与 `coverage` 的口径差异：这里把每条 `ast.stmt` 记一次，不展开隐式分支、
    不计算多行表达式的中间行。它不需要精确，只需要在覆盖率口径明显失真时能发现。
    """
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return 0
    return sum(1 for node in ast.walk(tree) if isinstance(node, ast.stmt))


def count_file(path: Path) -> int:
    try:
        text = Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return 0
    return executable_statements(text)
