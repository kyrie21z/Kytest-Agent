"""评测入口：跑 A0 基线、官方测试 baseline，并汇总成报告。

用法：

    # 先算官方测试 baseline（最强的对照锚点，只需算一次）
    python scripts/run_eval.py baseline

    # 跑一个变体（默认 A0），4 并发
    python scripts/run_eval.py run --variant A0

    # 中途断了直接重跑同一条命令，已完成的实例会自动跳过
    python scripts/run_eval.py run --variant A0

    # 汇总成主表
    python scripts/run_eval.py report

    # 冒烟测试：2 个实例 + 离线 Mock，用来验证整条管线能跑通
    python scripts/run_eval.py run --variant A0 --instances 2 --mock
"""
from __future__ import annotations

import argparse
import json
import sys
import tempfile
import time
from pathlib import Path
from typing import List, Optional

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))

from code_agent.config import Settings  # noqa: E402

from eval.dataset import load_dataset, select  # noqa: E402
from eval.metrics import official_baseline  # noqa: E402
from eval.report import summarize_variant, write_report  # noqa: E402
from eval.runner import (  # noqa: E402
    CHECKPOINTS,
    RunOutcome,
    Variant,
    default_variant,
    load_results,
    run_batch,
)
from eval.workspace import prepare_workspace  # noqa: E402

DEFAULT_OUTPUT = REPO_ROOT / "results"
DEFAULT_DATASET = REPO_ROOT / "benchmarks" / "humaneval_plus_30.jsonl"


def settings_factory(workspace: Path, *, allow_execution: bool = True) -> Settings:
    """评测层自己的 Settings 构造器。

    Agent 的命令执行必须打开：A0 的关键观察项就是"它会不会自发运行测试"。
    关掉它等于把要测量的能力阉割掉。真正的隔离靠工作区目录 + 评测器在外部。
    """
    settings = Settings.from_env(workspace=workspace)
    settings.allow_code_execution = allow_execution
    settings.allow_write = True
    settings.exec_timeout = 120
    settings.max_context_chars = 32000
    return settings


# ----------------------------------------------------------------------
# 子命令
# ----------------------------------------------------------------------
def cmd_baseline(args: argparse.Namespace) -> int:
    """用官方测试跑一遍完整测量，得到主表的对照锚点。"""
    dataset = load_dataset(args.dataset)
    chosen = select(dataset, args.ids) if args.ids else dataset
    if args.instances:
        chosen = chosen[: args.instances]

    target = Path(args.output) / "official_baseline.json"
    existing = {}
    if target.exists() and args.resume:
        try:
            existing = {
                item["instance_id"]: item
                for item in json.loads(target.read_text(encoding="utf-8")).get("per_instance", [])
            }
        except (OSError, json.JSONDecodeError, KeyError):
            existing = {}

    per_instance: List[dict] = []
    print(f"官方测试 baseline：{len(chosen)} 个实例，变异体上限 {args.max_mutants}")
    for index, instance in enumerate(chosen, 1):
        if instance.instance_id in existing:
            per_instance.append(existing[instance.instance_id])
            print(f"  [{index}/{len(chosen)}] {instance.instance_id} 跳过（已完成）")
            continue
        with tempfile.TemporaryDirectory(prefix="official-") as tmp:
            workspace = prepare_workspace(instance, Path(tmp))
            started = time.monotonic()
            metrics = official_baseline(instance, workspace, max_mutants=args.max_mutants)
            elapsed = time.monotonic() - started
        record = {
            "instance_id": instance.instance_id,
            "duration_sec": round(elapsed, 2),
            **metrics.to_dict(),
        }
        per_instance.append(record)
        print(
            f"  [{index}/{len(chosen)}] {instance.instance_id:<16} "
            f"cov={metrics.line_coverage:.0%} mut={metrics.mutation_score} ({elapsed:.1f}s)"
        )

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(
            json.dumps({"per_instance": per_instance}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    scores = [r["mutation_score"] for r in per_instance if r.get("mutation_score") is not None]
    coverage = [r["line_coverage"] for r in per_instance]
    summary = summarize_baseline(per_instance)
    print(
        f"\n官方测试汇总：all_pass={summary['all_pass_rate']:.1%} "
        f"cov={sum(coverage) / max(1, len(coverage)):.1%} "
        f"mutation={sum(scores) / max(1, len(scores)):.1%}（{len(scores)} 个实例可测）"
    )
    print(f"已写入 {target}")
    return 0


def summarize_baseline(records: List[dict]) -> dict:
    def mean(values: List[float]) -> float:
        return sum(values) / len(values) if values else 0.0

    return {
        "all_pass_rate": mean([1.0 if r.get("all_pass") else 0.0 for r in records]),
        "line_coverage": mean([float(r.get("line_coverage") or 0.0) for r in records]),
        "mutation_mean": mean([float(r["mutation_score"]) for r in records if r.get("mutation_score") is not None]),
    }


def cmd_run(args: argparse.Namespace) -> int:
    dataset = load_dataset(args.dataset)
    chosen = select(dataset, args.ids) if args.ids else dataset
    if args.instances:
        chosen = chosen[: args.instances]

    names = [name.strip() for name in args.variant.split(",") if name.strip()]
    variants = [default_variant(name) for name in names]

    factory = lambda workspace: settings_factory(workspace)  # noqa: E731
    if args.mock:
        variants = [_mock_variant(variant) for variant in variants]

    print(
        f"变体 {', '.join(v.name for v in variants)} | 实例 {len(chosen)} | "
        f"并发 {args.concurrency} | checkpoint {CHECKPOINTS} | 变异体上限 {args.max_mutants}"
    )
    if args.mock:
        print("注意：使用离线 Mock LLM，结果只用于验证管线，不可用于结论。")

    run_batch(
        chosen,
        variants,
        output_dir=Path(args.output),
        settings_factory=factory,
        checkpoints=CHECKPOINTS,
        max_mutants=args.max_mutants,
        concurrency=args.concurrency,
        resume=not args.no_resume,
    )
    return cmd_report(args)


def cmd_report(args: argparse.Namespace) -> int:
    outcomes = load_results(Path(args.output))
    if not outcomes:
        print("没有结果可汇总。先跑 run。")
        return 1

    official = _load_official_summary(Path(args.output))

    path = write_report(
        Path(args.output),
        outcomes,
        official=official,
        title="测试生成 Agent 评测结果",
    )
    print()
    print("=" * 78)
    print("主表")
    print("=" * 78)
    print(_main_table_only(path))
    print()
    print(f"完整报告 {path}")
    print(f"逐实例明细 {Path(args.output) / 'per_instance.csv'}")
    print(f"机器可读汇总 {Path(args.output) / 'summary.json'}")
    return 0


def _main_table_only(report_path: Path) -> str:
    """从报告里截出主表那一段，便于直接看结论。"""
    lines = report_path.read_text(encoding="utf-8").splitlines()
    collected: List[str] = []
    inside = False
    for line in lines:
        if line.strip() == "## 主表":
            inside = True
            continue
        if inside:
            if line.startswith("## "):
                break
            collected.append(line)
    return "\n".join(collected).strip()


def _load_official_summary(output_dir: Path):
    """读官方 baseline 并转成可汇总的对象。不存在时返回 None。"""
    baseline_path = output_dir / "official_baseline.json"
    if not baseline_path.exists():
        return None
    try:
        records = json.loads(baseline_path.read_text(encoding="utf-8"))["per_instance"]
    except (OSError, json.JSONDecodeError, KeyError):
        return None
    if not records:
        return None
    return summarize_variant(
        "官方测试（baseline）",
        [_baseline_as_outcome(record) for record in records],
    )


def _baseline_as_outcome(record: dict) -> RunOutcome:
    """把 baseline 记录包装成 RunOutcome，以便复用同一套汇总代码。"""
    payload = {key: value for key, value in record.items() if key not in ("instance_id", "duration_sec")}
    return RunOutcome(
        instance_id=str(record.get("instance_id", "")),
        variant="official",
        status="all_pass" if record.get("all_pass") else "partial_pass",
        final=payload,
        duration_sec=float(record.get("duration_sec") or 0.0),
    )


def _mock_variant(variant: Variant) -> Variant:
    """把变体换成离线 Mock，用于验证管线。"""
    return Variant(
        name=variant.name,
        description=variant.description + "（离线 Mock）",
        system_prompt=variant.system_prompt,
        tool_names=variant.tool_names,
        max_turns=variant.max_turns,
        max_total_tokens=variant.max_total_tokens,
    )


def _add_common_options(parser: argparse.ArgumentParser, *, suppress: bool = False) -> None:
    """加入常用选项。

    `suppress=True` 时不给这些选项设默认值，因此子命令上的副本只在显式给出时才
    覆盖全局值——否则子解析器的默认值会把用户写在子命令前面的值冲掉。
    这样 `--instances 2 run` 与 `run --instances 2` 都能用，避免"参数放错位置
    直接报错"这种纯属自找的摩擦。
    """
    default = argparse.SUPPRESS if suppress else None
    parser.add_argument(
        "--output", default=str(DEFAULT_OUTPUT) if not suppress else default, help="结果目录"
    )
    parser.add_argument(
        "--dataset", default=str(DEFAULT_DATASET) if not suppress else default, help="数据集路径"
    )
    parser.add_argument(
        "--instances", type=int, default=0 if not suppress else default, help="只跑前 N 个实例"
    )
    parser.add_argument(
        "--ids", nargs="*", default=None, help="指定实例 ID"
    )
    parser.add_argument(
        "--max-mutants", type=int, default=20 if not suppress else default, help="每实例变异体上限"
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="测试生成 Agent 评测入口")
    _add_common_options(parser)

    sub = parser.add_subparsers(dest="command", required=True)

    baseline = sub.add_parser("baseline", help="计算官方测试 baseline")
    baseline.add_argument("--resume", action="store_true", default=True)
    _add_common_options(baseline, suppress=True)

    run = sub.add_parser("run", help="运行变体并汇总")
    run.add_argument("--variant", default="A0", help="变体名，逗号分隔可多个")
    run.add_argument("--concurrency", type=int, default=4)
    run.add_argument("--mock", action="store_true", help="用离线 Mock 验证管线")
    run.add_argument("--no-resume", action="store_true", help="不跳过已完成实例")
    _add_common_options(run, suppress=True)

    report = sub.add_parser("report", help="只汇总已有结果")
    _add_common_options(report, suppress=True)

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    # 子命令与全局参数合并，便于 `run --mock` 这种写法
    if args.command == "baseline":
        return cmd_baseline(args)
    if args.command == "run":
        return cmd_run(args)
    if args.command == "report":
        return cmd_report(args)
    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
