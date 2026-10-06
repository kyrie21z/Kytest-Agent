"""展示一次完整的评测运行：Agent 到底做了什么。

用于复盘与文档，不参与评测。它在临时目录里跑一个实例，然后把
"Agent 看到的输入 → 每一步工具调用 → 评测怎么打分"完整打印出来。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT))

from eval.dataset import load_dataset, select  # noqa: E402
from eval.runner import TASK_PROMPT, default_variant, run_single  # noqa: E402
from scripts.run_eval import settings_factory  # noqa: E402


def main() -> int:
    instance_id = sys.argv[1] if len(sys.argv) > 1 else "HumanEval/5"
    instance = select(load_dataset(), [instance_id])[0]

    print("=" * 78)
    print(f"实例 {instance_id}　入口函数 {instance.entry_point}")
    print("=" * 78)
    print("\n【1】工作区里只有一个文件 solution.py —— Agent 能看到的全部代码：")
    print("-" * 78)
    print(instance.solution_source)

    print("\n【2】Agent 收到的任务（协议冻结，所有变体完全一致）：")
    print("-" * 78)
    for line in TASK_PROMPT.strip().splitlines():
        print(f"  user: {line}")
    print("  system: You are a coding agent. Inspect the workspace and complete")
    print("          the requested software engineering task using the available tools.")
    print(f"  工具: {', '.join(default_variant().tool_names)}")

    print("\n【3】Agent 运行中（每一步都是模型自己决定的，没有编排）：")
    print("-" * 78)
    outcome = run_single(
        instance,
        default_variant(),
        run_root=Path("results/_showcase"),
        settings_factory=settings_factory,
        checkpoints=(1, 2, 4, 8),
    )
    for item in outcome.agent.get("tool_trace", []):
        flag = "✗" if item["is_error"] else "✓"
        args = json.dumps(item["arguments"], ensure_ascii=False)
        print(f"  T{item['turn']} {flag} {item['name']}({args[:90]})")
        print(f"       → {item['first_line'][:130]}")

    print("\n【4】评测（Agent 看不到，在工作区之外执行）：")
    print("-" * 78)
    final = outcome.final
    print(f"  status         : {outcome.status}")
    print(f"  pytest         : {final.get('pytest_summary')!r}")
    print(f"  通过/失败/错误 : {final.get('passed')}/{final.get('failed')}/{final.get('errors')}")
    print(f"  行覆盖率       : {final.get('line_coverage', 0):.0%}"
          f"  （{final.get('covered_lines')}/{final.get('executable_lines')} 行）")
    score = final.get("mutation_score")
    print(f"  变异杀伤率     : {'未采集' if score is None else f'{score:.0%}'}"
          f"  （杀死 {final.get('mutants_killed')}/{final.get('mutants_total')} 个人造 Bug）")
    print(f"  按算子         : {final.get('killed_by_operator')} / {final.get('mutant_operators')}")
    print(f"  成本           : {outcome.agent['turns']} turns，"
          f"{outcome.agent['total_tokens']:,} tokens，{outcome.duration_sec:.0f}s")

    print("\n【5】Agent 产出的测试文件（前 3 个用例）：")
    print("-" * 78)
    lines = outcome.tests_source.splitlines()
    shown = 0
    for line in lines:
        if line.startswith("    def test"):
            shown += 1
            if shown > 3:
                break
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
