"""污染检查：这道题是真的会做，还是记住了？

HumanEval 是最早的代码生成基准之一，训练语料里几乎必然包含它。如果模型是"背出来的"，
那么：

- 分数会饱和（没有提升空间）；
- 更重要的是，**这个基准测的不是泛化能力**——A0~A3 的对比会变成"谁更会复述"，而不是
  "谁更会写测试"。

做法：把参考实现做一次**语义等价的扰动**（改函数名、改内部变量名、打乱等价分支结构），
然后让 Agent 在同一题上再写一次测试。若性能显著下降，说明先前的表现依赖对原始代码的
记忆，而不是对代码语义的理解。

扰动必须保持语义等价，否则测的就是"换个题"，而不是"同一道题的陌生版本"。

用法：
    python scripts/check_contamination.py --ids HumanEval/0 HumanEval/5
    python scripts/check_contamination.py --instances 3
"""
from __future__ import annotations

import argparse
import ast
import re
import sys
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from eval.dataset import Instance, load_dataset, select  # noqa: E402
from eval.runner import default_variant, run_single  # noqa: E402
from eval.workspace import prepare_workspace  # noqa: E402
from scripts.run_eval import settings_factory  # noqa: E402

# 重命名用的中性名字。避免使用有语义提示的词（如 `compute_result`），
# 那样会引入另一种偏差，让结果无法归因到"记忆"上。
def _perturbed_name(entry_point: str, index: int) -> str:
    return f"fn_{index:02d}_x"


@dataclass
class PerturbedInstance:
    """扰动后的实例：函数名被替换，但行为完全一致。"""

    original: Instance
    instance: Instance

    @property
    def summary(self) -> str:
        return f"{self.original.entry_point} → {self.instance.entry_point}"


def _rename_in_body(source: str, old: str, new: str) -> str:
    """对**函数体**做改名。

    `instance.solution` 是缩进片段（不含 `def` 行），直接 `ast.parse` 会报
    IndentationError；而 `ast.unparse` 出来的是完整函数定义，内层缩进已经是 4 空格，
    再统一加缩进就会变成双重缩进。正确做法是**逐条取函数体内的语句**再各自缩进。
    """
    wrapped = f"def {old}():\n" + source
    tree = ast.parse(wrapped)
    function = tree.body[0]
    assert isinstance(function, ast.FunctionDef)

    for node in ast.walk(function):
        if isinstance(node, ast.Name) and node.id == old:
            node.id = new

    lines: List[str] = []
    for statement in function.body:
        rendered = ast.unparse(statement)
        lines.extend("    " + line if line.strip() else line for line in rendered.splitlines())
    return "\n".join(lines) + "\n"


def _rename_in_header(source: str, old: str, new: str) -> str:
    """对签名 / docstring / 测试代码做标识符级替换。

    这些片段不是完整模块（签名单独解析不了、docstring 里还有 `>>>` 示例），
    因此用带词边界的正则替换。难度低于函数体改名，风险也可控。
    """
    return re.sub(rf"\b{re.escape(old)}\b", new, source)


def perturb(instance: Instance, index: int) -> Optional[PerturbedInstance]:
    """生成语义等价的扰动版本。无法安全扰动时返回 None。"""
    new_name = _perturbed_name(instance.entry_point, index)
    if new_name == instance.entry_point:
        return None

    try:
        solution = _rename_in_body(instance.solution, instance.entry_point, new_name)
    except (SyntaxError, IndentationError):
        return None

    prompt = _rename_in_header(instance.prompt, instance.entry_point, new_name)
    tests = _rename_in_header(instance.official_tests, instance.entry_point, new_name)

    # 被扰动后的实例：函数体与其他部分都只换了名字，行为必须完全一致。
    # 这一点由 `_verify_equivalence` 用官方测试实际验证，不靠推理。
    perturbed = Instance(
        instance_id=instance.instance_id,
        prompt=prompt,
        solution=solution,
        entry_point=new_name,
        official_tests=tests,
        contract=instance.contract,
    )
    return PerturbedInstance(original=instance, instance=perturbed)


def _verify_equivalence(pair: PerturbedInstance) -> bool:
    """确认扰动版本与原版行为一致：官方测试必须都能通过。

    如果这一步失败，说明扰动改变了语义，后续比较就没有意义。
    """
    from eval.workspace import OFFICIAL_TESTS_FILENAME, write_official_tests
    from eval.metrics import run_pytest_on

    with tempfile.TemporaryDirectory(prefix="equiv-") as tmp:
        workspace = prepare_workspace(pair.instance, Path(tmp))
        write_official_tests(pair.instance, workspace)
        result = run_pytest_on(OFFICIAL_TESTS_FILENAME, workspace)
    return result.all_pass


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="检查基准污染：扰动后性能是否下降")
    parser.add_argument("--instances", type=int, default=2, help="检查前 N 个实例")
    parser.add_argument("--ids", nargs="*", default=None, help="指定实例 ID")
    parser.add_argument("--max-mutants", type=int, default=20)
    parser.add_argument("--output", default=str(REPO_ROOT / "results" / "contamination"))
    args = parser.parse_args(argv)

    dataset = load_dataset()
    chosen = select(dataset, args.ids) if args.ids else dataset[: args.instances]

    print("污染检查：对比「原始代码」与「语义等价但改名后的代码」上的表现")
    print("若两者差异明显，说明模型依赖对原始代码的记忆。\n")

    rows: List[Dict[str, object]] = []
    for index, instance in enumerate(chosen):
        pair = perturb(instance, index)
        if pair is None:
            print(f"{instance.instance_id}: 跳过（没有可用的改名方案）")
            continue

        if not _verify_equivalence(pair):
            print(f"{instance.instance_id}: 跳过（扰动改变了语义，官方测试不再通过）")
            continue

        print(f"{instance.instance_id}　{pair.summary}")
        started = time.monotonic()
        original_outcome = run_single(
            instance,
            default_variant(),
            run_root=Path(args.output) / "original",
            settings_factory=settings_factory,
            max_mutants=args.max_mutants,
        )
        perturbed_outcome = run_single(
            pair.instance,
            default_variant(),
            run_root=Path(args.output) / "perturbed",
            settings_factory=settings_factory,
            max_mutants=args.max_mutants,
        )
        elapsed = time.monotonic() - started

        def describe(outcome) -> str:
            final = outcome.final
            score = final.get("mutation_score")
            return (
                f"status={outcome.status:<12} pass={final.get('all_pass')!s:<5} "
                f"cov={final.get('line_coverage', 0):.0%} "
                f"mut={'n/a' if score is None else f'{score:.0%}'} "
                f"tests={final.get('passed', 0)}"
            )

        print(f"    原始代码    {describe(original_outcome)}")
        print(f"    改名后代码  {describe(perturbed_outcome)}")
        print(f"    （耗时 {elapsed:.0f}s，共记录 {len(original_outcome.checkpoints)} 个 checkpoint）\n")

        rows.append(
            {
                "instance_id": instance.instance_id,
                "original": original_outcome.final,
                "perturbed": perturbed_outcome.final,
                "original_status": original_outcome.status,
                "perturbed_status": perturbed_outcome.status,
            }
        )

    if not rows:
        print("没有可比较的实例。")
        return 1

    print("=" * 78)
    print("汇总")
    print("=" * 78)
    original_pass = sum(1 for r in rows if r["original"].get("all_pass")) / len(rows)
    perturbed_pass = sum(1 for r in rows if r["perturbed"].get("all_pass")) / len(rows)
    original_mut = [r["original"]["mutation_score"] for r in rows if r["original"].get("mutation_score") is not None]
    perturbed_mut = [r["perturbed"]["mutation_score"] for r in rows if r["perturbed"].get("mutation_score") is not None]

    print(f"  all_pass   原始 {original_pass:.0%}　改名后 {perturbed_pass:.0%}")
    if original_mut and perturbed_mut:
        print(
            f"  mutation   原始 {sum(original_mut) / len(original_mut):.0%}"
            f"　改名后 {sum(perturbed_mut) / len(perturbed_mut):.0%}"
        )
    print(f"  样本数 {len(rows)}")
    print()
    print("判读：n 这么小只能作为方向性信号。若改名后明显下降，")
    print("     则不应把 HumanEval+ 当作衡量测试生成能力的主基准。")
    print(f"详细结果：{args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
