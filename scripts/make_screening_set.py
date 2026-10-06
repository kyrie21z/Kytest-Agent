#!/usr/bin/env python3
"""生成筛查集：全集 164 例减去冻结评测集 30 例 = 134 例。

筛查跑（A0 全量难度测量）的候选池必须**排除评测集实例**——
后续的难度富集选集（评测集 v2）只允许从这个池子里取，
这是修订 2 的污染防线之一。选择规则是简单的集合差，无随机数。

用法：
    python scripts/make_screening_set.py
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
FULL = REPO_ROOT / "benchmarks" / "humaneval_plus_164.jsonl"
EVAL = REPO_ROOT / "benchmarks" / "humaneval_plus_30.jsonl"
OUTPUT = REPO_ROOT / "benchmarks" / "humaneval_plus_134_screen.jsonl"


def main() -> int:
    eval_ids = {json.loads(line)["instance_id"] for line in EVAL.read_text(encoding="utf-8").splitlines() if line.strip()}
    kept: list[str] = []
    for line in FULL.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        if record["instance_id"] not in eval_ids:
            kept.append(line)
    if len(kept) != len(eval_ids) and len(kept) + len(eval_ids) != 164:
        print(f"错误：全集 164 = 筛查 {len(kept)} + 评测 {len(eval_ids)} 不成立", file=sys.stderr)
        return 1
    OUTPUT.write_text("\n".join(kept) + "\n", encoding="utf-8")
    print(f"筛查集 {len(kept)} 例（已排除评测集 {len(eval_ids)} 例）→ {OUTPUT.relative_to(REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
