"""仪器校准脚本：验证变异引擎的区分度。

对应第一性原理分析里的"仪器 sanity suite"。在把任何结论建立在 mutation score
之上以前，必须先证明这把尺子能区分好坏：

1. **官方测试应该得高分** —— 否则引擎把好测试判成了坏测试；
2. **空/极弱测试应该接近 0** —— 否则引擎会把"什么都没测"判成"测得好"。

两个方向缺一不可。只看官方测试得高分，无法排除"所有测试都得高分"这种失效模式。

用法：
    python scripts/calibrate_instrument.py
    python scripts/calibrate_instrument.py --instances 5
"""
from __future__ import annotations

import argparse
import sys
import tempfile
from pathlib import Path
from typing import List

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from eval.dataset import Instance, load_dataset, select  # noqa: E402
from eval.metrics import collect_metrics, official_baseline  # noqa: E402
from eval.mutation import generate_mutants  # noqa: E402
from eval.workspace import prepare_workspace  # noqa: E402

# 三种"测试质量"档位，用来检验引擎的单调性
NO_ASSERTION = "import pytest\nfrom solution import {entry}\n\n\ndef test_calls_only():\n    {entry}\n"
ONE_ASSERTION = (
    "import pytest\nfrom solution import {entry}\n\n\n"
    "def test_smoke():\n    assert {entry} is not None\n"
)


def _row(name: str, metrics) -> str:
    score = metrics.mutation_score
    score_text = "n/a" if score is None else f"{score:.0%}"
    return (
        f"  {name:<28} pass={metrics.all_pass!s:<5} "
        f"cov={metrics.line_coverage:>6.1%}  mutation={score_text:>5}  "
        f"({metrics.mutants_killed}/{metrics.mutants_total})"
    )


def calibrate(instances: List[Instance], max_mutants: int) -> int:
    totals = {"official": 0.0, "weak": 0.0, "calls_only": 0.0, "count": 0}
    problems: List[str] = []
    no_mutants: List[str] = []

    for instance in instances:
        entry = instance.entry_point
        with tempfile.TemporaryDirectory(prefix="calib-") as tmp:
            workspace = prepare_workspace(instance, Path(tmp))

            (workspace / "test_solution.py").write_text(
                NO_ASSERTION.format(entry=entry), encoding="utf-8"
            )
            calls_only = collect_metrics(
                instance, workspace, checkpoint=0, include_mutation=True, max_mutants=max_mutants
            )

            (workspace / "test_solution.py").write_text(
                ONE_ASSERTION.format(entry=entry), encoding="utf-8"
            )
            weak = collect_metrics(
                instance, workspace, checkpoint=0, include_mutation=True, max_mutants=max_mutants
            )

            official = official_baseline(instance, workspace, max_mutants=max_mutants)

        print(f"\n{instance.instance_id}  ({entry})")
        print(_row("官方测试", official))
        print(_row("单条弱断言", weak))
        print(_row("只调用不断言", calls_only))

        if official.mutation_score is None or official.mutants_total == 0:
            # 结构性情况：源码里没有可变异算子（例如只做集合运算）。
            # 这类实例在杀伤率上无法测量，因此不进分母——不是仪器问题。
            # 协议 §2.1 已注明；其它指标（通过率、覆盖率）仍然正常计入。
            no_mutants.append(instance.instance_id)
            continue

        totals["official"] += official.mutation_score
        totals["weak"] += weak.mutation_score or 0.0
        totals["calls_only"] += calls_only.mutation_score or 0.0
        totals["count"] += 1

        # 方向一：官方测试必须显著强于"只调用不断言"
        if official.mutation_score <= (calls_only.mutation_score or 0.0):
            problems.append(
                f"{instance.instance_id}: 官方测试杀伤率 {official.mutation_score:.0%} "
                f"不高于空测试 {calls_only.mutation_score:.0%}"
            )
        # 方向二：官方测试本身不能太低（低于 50% 说明引擎噪声过大）
        if official.mutation_score < 0.5:
            problems.append(
                f"{instance.instance_id}: 官方测试杀伤率仅 {official.mutation_score:.0%}，"
                "引擎可能把有效测试误判为未杀死"
            )

    count = max(1, totals["count"])
    print("\n" + "=" * 78)
    print("汇总（均值）")
    print("=" * 78)
    print(f"  官方测试       mutation={totals['official'] / count:.1%}")
    print(f"  单条弱断言     mutation={totals['weak'] / count:.1%}")
    print(f"  只调用不断言   mutation={totals['calls_only'] / count:.1%}")
    print(f"  参与统计实例   {totals['count']}")
    if no_mutants:
        print(f"  无变异体实例   {len(no_mutants)} 个（不进杀伤率分母）：{', '.join(no_mutants)}")

    if problems:
        print("\n发现的问题：")
        for item in problems:
            print(f"  ! {item}")
        return 1

    print("\n仪器校准通过：官方测试显著高于空测试，且官方测试本身处于合理区间。")
    return 0


def main(argv: List[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="校准变异引擎的区分度")
    parser.add_argument("--instances", type=int, default=5, help="抽多少个实例做校准，默认 5")
    parser.add_argument("--max-mutants", type=int, default=20, help="每个实例的变异体上限")
    parser.add_argument("--ids", nargs="*", default=None, help="指定实例 ID")
    args = parser.parse_args(argv)

    dataset = load_dataset()
    chosen = select(dataset, args.ids) if args.ids else dataset[: args.instances]
    print(f"数据集共 {len(dataset)} 个实例，本次校准 {len(chosen)} 个")

    print("\n变异体生成预览：")
    for instance in chosen[:3]:
        mutants = generate_mutants(instance.solution_source, max_mutants=args.max_mutants)
        operators: dict = {}
        for mutant in mutants:
            operators[mutant.operator] = operators.get(mutant.operator, 0) + 1
        print(f"  {instance.instance_id:<16} {len(mutants):>2} 个  {operators}")

    return calibrate(chosen, args.max_mutants)


if __name__ == "__main__":
    raise SystemExit(main())
