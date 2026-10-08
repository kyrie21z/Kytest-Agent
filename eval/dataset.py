"""Read explicitly supplied JSONL evaluation instances without network access."""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional


@dataclass(frozen=True)
class Instance:
    """一个评测实例。

    `solution` 是被测对象，`official_tests` 是 baseline 的测量依据——
    两者都必须按原样使用，任何裁剪都会破坏评测的有效性。
    """

    instance_id: str
    prompt: str
    solution: str
    entry_point: str
    official_tests: str
    contract: str = ""

    @property
    def solution_source(self) -> str:
        """`solution.py` 的完整内容：函数签名 + 参考实现。

        直接写成可导入的模块，因此 Agent 与评测器面对的是同一份事实。
        """
        prompt = self.prompt.rstrip("\n")
        body = self.solution
        if body and not body.startswith("\n"):
            body = "\n" + body
        if body and not body.endswith("\n"):
            body += "\n"
        return prompt + body + "\n"

    @property
    def official_test_source(self) -> str:
        """把官方测试包成独立 pytest 文件，用与 Agent 测试**完全相同**的方式执行。

        这是 baseline 可比的前提：同一个 runner、同一套指标、同一条代码路径。
        """
        return (
            "# 官方测试（HumanEval+, EvalPlus），仅用于评测 baseline，不进入 Agent 工作区。\n"
            "import pytest\n\n"
            f"from solution import {self.entry_point}\n\n\n"
            f"{self.official_tests}\n\n\n"
            "def test_official():\n"
            f"    check({self.entry_point})\n"
        )


def load_dataset(path: Path) -> List[Instance]:
    """按行读取实例。格式错误时立即报错，不静默跳过。"""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"找不到数据集 {source}")

    instances: List[Instance] = []
    with source.open("r", encoding="utf-8") as handle:
        for number, line in enumerate(handle, 1):
            line = line.strip()
            if not line:
                continue
            try:
                payload: Dict[str, Any] = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{source}:{number} 不是合法 JSON：{exc}") from exc
            missing = [
                key
                for key in ("instance_id", "prompt", "solution", "entry_point", "official_tests")
                if key not in payload
            ]
            if missing:
                raise ValueError(f"{source}:{number} 缺少字段：{', '.join(missing)}")
            instances.append(
                Instance(
                    instance_id=str(payload["instance_id"]),
                    prompt=str(payload["prompt"]),
                    solution=str(payload["solution"]),
                    entry_point=str(payload["entry_point"]),
                    official_tests=str(payload["official_tests"]),
                    contract=str(payload.get("contract") or ""),
                )
            )
    if not instances:
        raise ValueError(f"数据集 {source} 为空")
    return instances


def select(instances: Iterable[Instance], instance_ids: Optional[List[str]] = None) -> List[Instance]:
    """按 ID 过滤，保持数据集原顺序。未知 ID 直接报错——静默少跑实例最危险。"""
    ordered = list(instances)
    if not instance_ids:
        return ordered
    wanted = set(instance_ids)
    known = {instance.instance_id for instance in ordered}
    unknown = wanted - known
    if unknown:
        raise KeyError(f"数据集里没有这些实例：{', '.join(sorted(unknown))}")
    return [instance for instance in ordered if instance.instance_id in wanted]
