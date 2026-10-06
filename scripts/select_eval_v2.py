#!/usr/bin/env python3
"""从 A0 筛查结果中选出难度富集评测集 v2（纯 20 难例）+ 5 例冒烟池。

**本脚本的准则在任何 A1–A3 运行之前冻结**（协议修订 2，2026-10-06）。
它只消费 A0 筛查数据（results/A0_screen），这是选集合法性的前提：
选集依据里没有任何后来变体的结果。

准则（冻结，不得事后修改）：

1. 候选池 = 筛查集 134 例（构造上已排除冻结评测集 30 例）；
2. 排除 `mutants_total = 0`（杀伤率不可测量）与 `status = eval_error` 的实例；
3. 排序：`all_pass = false` 优先 → `mutation_score` 升序 → `instance_id` 字典序
   （保证确定性，无随机数）；
4. 取前 20 → **评测集 v2**；
5. 冒烟池：剩余实例按 `instance_id` 字典序等距取 5——它的唯一用途是 A1–A3
   开发期的冒烟测试，任何开发行为不得触碰评测集 v2 的实例。

消融主表中 A0 必须在 v2 上全新重跑（不沿用筛查分数），规避均值回归偏倚。

用法：
    python scripts/select_eval_v2.py            # 默认读取 results/A0_screen
    python scripts/select_eval_v2.py --screen results/A0_screen
"""
from __future__ import annotations

import csv
import json
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
V2_SIZE = 20
SMOKE_SIZE = 5
CRITERION = (
    "排除 mutants_total=0 与 eval_error；all_pass=false 优先 → mutation_score 升序 → "
    "instance_id 字典序；取前 20。冒烟池：剩余实例按 instance_id 字典序等距取 5。"
)


@dataclass(frozen=True)
class ScreeningRow:
    instance_id: str
    status: str
    all_pass: bool
    mutation_score: float | None
    mutants_total: int


def load_screening(screen_dir: Path) -> list[ScreeningRow]:
    path = screen_dir / "per_instance.csv"
    if not path.exists():
        raise FileNotFoundError(f"找不到筛查结果 {path}——先跑完筛查再选集")
    rows: list[ScreeningRow] = []
    with path.open("r", encoding="utf-8") as handle:
        for record in csv.DictReader(handle):
            raw_score = (record.get("mutation_score") or "").strip()
            rows.append(
                ScreeningRow(
                    instance_id=record["instance_id"],
                    status=record.get("status", ""),
                    all_pass=record.get("all_pass", "").strip().lower() == "true",
                    mutation_score=float(raw_score) if raw_score else None,
                    mutants_total=int(record.get("mutants_total") or 0),
                )
            )
    return rows


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:]
    screen_dir = Path(args[args.index("--screen") + 1]) if "--screen" in args else REPO_ROOT / "results" / "A0_screen"

    rows = load_screening(screen_dir)
    ids_seen = {row.instance_id for row in rows}

    # 冻结的 30 例不在筛查集里（构造上已排除）；这里再核一遍，双保险。
    eval30 = {
        json.loads(line)["instance_id"]
        for line in (REPO_ROOT / "benchmarks" / "humaneval_plus_30.jsonl").read_text(encoding="utf-8").splitlines()
        if line.strip()
    }
    overlap = ids_seen & eval30
    if overlap:
        print(f"错误：筛查集中混入了评测集实例 {sorted(overlap)}", file=sys.stderr)
        return 1

    eligible = [
        row for row in rows
        if row.mutants_total > 0 and row.mutation_score is not None and row.status != "eval_error"
    ]
    excluded = [row for row in rows if row not in eligible]

    ranked = sorted(
        eligible,
        key=lambda row: (row.all_pass, row.mutation_score, row.instance_id),
    )
    selected = ranked[:V2_SIZE]
    remaining_ids = {row.instance_id for row in eligible} - {row.instance_id for row in selected}

    # 冒烟池：剩余实例按 ID 字典序等距取 5
    remaining_sorted = sorted(remaining_ids)
    step = len(remaining_sorted) / SMOKE_SIZE
    smoke = [remaining_sorted[int(i * step)] for i in range(SMOKE_SIZE)]

    # 从全集数据里取出实例记录，写成评测可直接消费的 jsonl
    full_records: dict[str, str] = {}
    for line in (REPO_ROOT / "benchmarks" / "humaneval_plus_164.jsonl").read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        record = json.loads(line)
        full_records[record["instance_id"]] = line

    v2_path = REPO_ROOT / "benchmarks" / "humaneval_plus_v2_20.jsonl"
    smoke_path = REPO_ROOT / "benchmarks" / "smoke_pool_5.jsonl"
    v2_path.write_text("\n".join(full_records[i] for i in (r.instance_id for r in selected)) + "\n", encoding="utf-8")
    smoke_path.write_text("\n".join(full_records[i] for i in smoke) + "\n", encoding="utf-8")

    # 选集过程留档：准则、来源、每个入选实例的筛查指标
    provenance = {
        "date": "2026-10-06",
        "criterion": CRITERION,
        "screening_run": str(screen_dir),
        "pool_size": len(rows),
        "excluded": [
            {"instance_id": row.instance_id, "why": "mutants_total=0" if row.mutants_total == 0 else row.status or "score 不可测"}
            for row in excluded
        ],
        "eval_v2": [row.__dict__ | {"source": "screening"} for row in selected],
        "smoke_pool": smoke,
    }
    (REPO_ROOT / "benchmarks" / "eval_v2_selection.json").write_text(
        json.dumps(provenance, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"候选 {len(rows)} 例（排除 {len(excluded)}），选出评测集 v2 前 {V2_SIZE} 名：\n")
    print(f"{'instance':<18}{'status':<14}{'mutation':>9}  all_pass")
    for row in selected:
        print(f"{row.instance_id:<18}{row.status:<14}{row.mutation_score:>9.3f}  {row.all_pass}")
    print(f"\n评测集 v2 → {v2_path.relative_to(REPO_ROOT)}")
    print(f"冒烟池   → {smoke_path.relative_to(REPO_ROOT)}（{', '.join(smoke)}）")
    print(f"选集留档 → benchmarks/eval_v2_selection.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
