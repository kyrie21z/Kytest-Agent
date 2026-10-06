"""工作区准备与清理：控制"Agent 能看到什么"。

这是实验有效性的第一道闸门。协议要求 Agent 只能看到 `solution.py`：

- 没有官方测试（否则 Agent 直接抄）；
- 没有 benchmark 目录（否则能读到 ground truth）；
- 没有 `.git`（否则可能拉出原始仓库）；
- 没有上一次运行的残留（否则覆盖率的可执行行数会被污染）。

同时提供"重置为原始状态"的能力，用于评测后恢复现场、
以及在同一实例上跑多个变体时保证起点完全一致。
"""
from __future__ import annotations

import shutil
from pathlib import Path
from typing import List

from .dataset import Instance

SOLUTION_FILENAME = "solution.py"
TESTS_FILENAME = "test_solution.py"
# 官方测试文件名必须符合 pytest 的默认收集模式（`test_*.py`）。
# 覆盖率测量用 `coverage run -m pytest`（不带目标路径）来跑，若文件名不匹配，
# pytest 会收集到 0 个测试、coverage 报 "No data to report"，
# 表现为"官方测试覆盖率 0%"——这个陷阱实际踩过。
OFFICIAL_TESTS_FILENAME = "test_official_baseline.py"

# 评测前必须清掉的产物。`.sessions` 是 Agent 轨迹，`.pytest_cache` 与
# `__pycache__` 会影响覆盖率统计的可执行行数。
EPHEMERAL = (".sessions", ".pytest_cache", "__pycache__", ".coverage", ".coverage.json")


def prepare_workspace(instance: Instance, directory: Path) -> Path:
    """建立一个只含 `solution.py` 的干净工作区。

    已存在时先清空：同一路径被复用会让上一次的产物泄漏进这一次的测量。

    **路径必须绝对化。** 相对路径会顺着子进程的 cwd 逐层解析：评测时以工作区为
    cwd 运行 `coverage json -o .coverage.json`，相对输出路径会被写到工作区**内部**
    的嵌套目录里，而检查逻辑仍在工作区根目录找，于是覆盖率静默变成 0%。
    这个坑真实踩过。
    """
    directory = Path(directory).expanduser().resolve()
    if directory.exists():
        shutil.rmtree(directory, ignore_errors=True)
    directory.mkdir(parents=True, exist_ok=True)
    (directory / SOLUTION_FILENAME).write_text(instance.solution_source, encoding="utf-8")
    return directory


def write_official_tests(instance: Instance, directory: Path) -> Path:
    """把官方测试写到工作区里，**仅在评测 baseline 时使用**。

    调用方必须在测完之后删除它，否则它会留在工作区里被后续测量看见。
    """
    target = Path(directory) / OFFICIAL_TESTS_FILENAME
    target.write_text(instance.official_test_source, encoding="utf-8")
    return target


def restore_solution(instance: Instance, directory: Path) -> Path:
    """把 `solution.py` 恢复成原始实现。

    变异测试会把变异体写进这个文件，测完必须还原，否则后续 checkpoint 的
    覆盖率与通过性测量都建立在被改坏的代码上。
    """
    target = Path(directory) / SOLUTION_FILENAME
    target.write_text(instance.solution_source, encoding="utf-8")
    return target


def clean_ephemeral(directory: Path) -> List[str]:
    """删除评测前不应存在的产物，返回被删掉的路径名。"""
    removed: List[str] = []
    root = Path(directory)
    for name in EPHEMERAL:
        target = root / name
        if target.is_dir():
            shutil.rmtree(target, ignore_errors=True)
            removed.append(name)
        elif target.exists():
            target.unlink(missing_ok=True)
            removed.append(name)
    return removed


def has_tests(directory: Path) -> bool:
    """工作区里是否存在 Agent 产出的测试文件。

    只看约定的文件名。Agent 写了别的名字也算"没产出"——协议冻结了任务提示，
    文件名是任务契约的一部分，允许它自由命名会让"是否产出测试"这个判定变得模糊。
    """
    return (Path(directory) / TESTS_FILENAME).is_file()


def read_tests(directory: Path) -> str:
    target = Path(directory) / TESTS_FILENAME
    if not target.is_file():
        return ""
    return target.read_text(encoding="utf-8", errors="replace")
