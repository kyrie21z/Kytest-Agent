"""结果汇总：把逐实例的 JSON 变成主表、质量–预算曲线与失败分类。

一条纪律：**汇总层不做任何筛选性处理**。所有启动过的运行都进入分母（协议 §5），
缺失的指标记为"未采集"而不是 0，剔除只发生在"该实例无法测量"这种结构性原因上，
并且剔除数量必须报告出来。任何一处静默丢弃都会让主表失去可信度。
"""
from __future__ import annotations

import csv
import json
import statistics
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Sequence

from .runner import CHECKPOINTS, RunOutcome


# ----------------------------------------------------------------------
# 取值工具：缺失与 0 必须区分开
# ----------------------------------------------------------------------
def get_path(payload: Dict[str, Any], *keys: str, default: Any = None) -> Any:
    current: Any = payload
    for key in keys:
        if not isinstance(current, dict) or key not in current:
            return default
        current = current[key]
    return current


def mutation_scores(outcomes: Iterable[RunOutcome]) -> List[float]:
    """取出**已采集**的杀伤率。未采集或无法测量的实例不进分母。"""
    values: List[float] = []
    for outcome in outcomes:
        score = outcome.final.get("mutation_score")
        if score is None:
            continue
        values.append(float(score))
    return values


def coverage_values(outcomes: Iterable[RunOutcome]) -> List[float]:
    """覆盖率：全部实例都计入（没有测试文件时协议规定为 0）。"""
    return [float(outcome.final.get("line_coverage") or 0.0) for outcome in outcomes]


def _mean(values: Sequence[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def _stdev(values: Sequence[float]) -> float:
    return statistics.stdev(values) if len(values) > 1 else 0.0


# ----------------------------------------------------------------------
# 聚合
# ----------------------------------------------------------------------
@dataclass
class VariantSummary:
    variant: str
    n: int = 0
    all_pass_rate: float = 0.0
    import_ok_rate: float = 0.0
    line_coverage: float = 0.0
    line_coverage_sd: float = 0.0
    mutation_mean: float = 0.0
    mutation_sd: float = 0.0
    mutation_n: int = 0
    turns_mean: float = 0.0
    tokens_mean: float = 0.0
    runtime_mean: float = 0.0
    status_counts: Dict[str, int] = field(default_factory=dict)
    network_attempts: int = 0
    eval_errors: int = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "variant": self.variant,
            "n": self.n,
            "all_pass_rate": round(self.all_pass_rate, 4),
            "import_ok_rate": round(self.import_ok_rate, 4),
            "line_coverage": round(self.line_coverage, 4),
            "line_coverage_sd": round(self.line_coverage_sd, 4),
            "mutation_mean": round(self.mutation_mean, 4),
            "mutation_sd": round(self.mutation_sd, 4),
            "mutation_n": self.mutation_n,
            "turns_mean": round(self.turns_mean, 2),
            "tokens_mean": round(self.tokens_mean, 1),
            "runtime_mean": round(self.runtime_mean, 2),
            "status_counts": self.status_counts,
            "network_attempts": self.network_attempts,
            "eval_errors": self.eval_errors,
        }


def summarize_variant(variant: str, outcomes: Sequence[RunOutcome]) -> VariantSummary:
    summary = VariantSummary(variant=variant, n=len(outcomes))
    if not outcomes:
        return summary

    summary.all_pass_rate = _mean([1.0 if o.final.get("all_pass") else 0.0 for o in outcomes])
    summary.import_ok_rate = _mean([1.0 if o.final.get("import_ok") else 0.0 for o in outcomes])

    coverage = coverage_values(outcomes)
    summary.line_coverage = _mean(coverage)
    summary.line_coverage_sd = _stdev(coverage)

    scores = mutation_scores(outcomes)
    summary.mutation_n = len(scores)
    summary.mutation_mean = _mean(scores)
    summary.mutation_sd = _stdev(scores)

    summary.turns_mean = _mean([float(o.agent.get("turns") or 0) for o in outcomes])
    summary.tokens_mean = _mean([float(o.agent.get("total_tokens") or 0) for o in outcomes])
    summary.runtime_mean = _mean([float(o.duration_sec or 0.0) for o in outcomes])

    counts: Dict[str, int] = {}
    for outcome in outcomes:
        counts[outcome.status] = counts.get(outcome.status, 0) + 1
    summary.status_counts = dict(sorted(counts.items()))
    summary.network_attempts = sum(1 for o in outcomes if o.network_attempt)
    summary.eval_errors = sum(1 for o in outcomes if o.status == "eval_error")
    return summary


def quality_curves(outcomes: Sequence[RunOutcome]) -> Dict[str, List[Dict[str, float]]]:
    """质量–预算曲线：按 checkpoint 给出聚合指标。

    指标是"便宜的两层"（通过率、覆盖率），因为协议 §3 只在最终采集主终点。
    主终点单独在 `mutation_at_endpoint` 里给出。
    """
    by_checkpoint: Dict[str, List[Dict[str, float]]] = {}
    for outcome in outcomes:
        for record in outcome.checkpoints:
            step = int(record.get("checkpoint") or 0)
            by_checkpoint.setdefault(str(step), []).append(record)

    curves: Dict[str, List[Dict[str, float]]] = {}
    for step, records in sorted(by_checkpoint.items(), key=lambda item: int(item[0])):
        curves[step] = [
            {
                "checkpoint": int(step),
                "n": len(records),
                "all_pass_rate": _mean([1.0 if r.get("all_pass") else 0.0 for r in records]),
                "line_coverage": _mean([float(r.get("line_coverage") or 0.0) for r in records]),
                "has_tests_rate": _mean([1.0 if r.get("has_tests") else 0.0 for r in records]),
            }
        ]
    return curves


def failure_cases(outcomes: Sequence[RunOutcome]) -> Dict[str, List[str]]:
    """按状态归类实例 ID。失败分类是"出彩条件 I"的原料。"""
    buckets: Dict[str, List[str]] = {}
    for outcome in outcomes:
        buckets.setdefault(outcome.status, []).append(outcome.instance_id)
    return {key: sorted(value) for key, value in sorted(buckets.items())}


# ----------------------------------------------------------------------
# 渲染
# ----------------------------------------------------------------------
def render_main_table(summaries: Sequence[VariantSummary], official: Optional[VariantSummary] = None) -> str:
    """主表。official 行是官方测试的 baseline，是最强的对照锚点。"""
    lines = [
        "| Variant | All-Pass | Import OK | Line Cov. | Mutation | n(mut) | Turns | Tokens | Runtime |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for summary in list(summaries) + ([official] if official else []):
        label = f"*{summary.variant}*" if official and summary is official else summary.variant
        mutation = (
            f"{summary.mutation_mean:.1%} ± {summary.mutation_sd:.1%}"
            if summary.mutation_n
            else "未采集"
        )
        lines.append(
            f"| {label} | {summary.all_pass_rate:.1%} | {summary.import_ok_rate:.1%} | "
            f"{summary.line_coverage:.1%} ± {summary.line_coverage_sd:.1%} | {mutation} | "
            f"{summary.mutation_n} | {summary.turns_mean:.1f} | {summary.tokens_mean:,.0f} | "
            f"{summary.runtime_mean:.1f}s |"
        )
    return "\n".join(lines)


def render_curve_table(curves: Dict[str, List[Dict[str, float]]]) -> str:
    """质量–预算曲线表：横轴是 checkpoint。"""
    if not curves:
        return "（无 checkpoint 数据）"
    lines = [
        "| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |",
        "|---:|---:|---:|---:|---:|",
    ]
    for step in sorted(curves, key=int):
        record = curves[step][0]
        lines.append(
            f"| {step} turn | {int(record['n'])} | {record['has_tests_rate']:.1%} | "
            f"{record['all_pass_rate']:.1%} | {record['line_coverage']:.1%} |"
        )
    return "\n".join(lines)


def render_status_table(summaries: Sequence[VariantSummary]) -> str:
    """状态分布。ITI 原则下，这些"失败"也计入分母，因此必须可见。"""
    statuses = sorted({status for summary in summaries for status in summary.status_counts})
    if not statuses:
        return "（无数据）"
    header = "| Variant | " + " | ".join(statuses) + " |"
    divider = "|---" * (len(statuses) + 1) + "|"
    lines = [header, divider]
    for summary in summaries:
        cells = [str(summary.status_counts.get(status, 0)) for status in statuses]
        lines.append(f"| {summary.variant} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def write_csv(output_dir: Path, outcomes: Sequence[RunOutcome]) -> Path:
    """逐实例明细 CSV。报告里每个均值都能被它追溯到具体实例。"""
    target = Path(output_dir) / "per_instance.csv"
    columns = [
        "variant",
        "instance_id",
        "status",
        "has_tests",
        "all_pass",
        "import_ok",
        "passed",
        "failed",
        "errors",
        "line_coverage",
        "mutation_score",
        "mutants_total",
        "mutants_killed",
        "turns",
        "llm_calls",
        "tool_calls",
        "total_tokens",
        "duration_sec",
        "network_attempt",
    ]
    with target.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
        writer.writeheader()
        for outcome in outcomes:
            final = outcome.final
            writer.writerow(
                {
                    "variant": outcome.variant,
                    "instance_id": outcome.instance_id,
                    "status": outcome.status,
                    "has_tests": final.get("has_tests"),
                    "all_pass": final.get("all_pass"),
                    "import_ok": final.get("import_ok"),
                    "passed": final.get("passed"),
                    "failed": final.get("failed"),
                    "errors": final.get("errors"),
                    "line_coverage": final.get("line_coverage"),
                    "mutation_score": final.get("mutation_score"),
                    "mutants_total": final.get("mutants_total"),
                    "mutants_killed": final.get("mutants_killed"),
                    "turns": outcome.agent.get("turns"),
                    "llm_calls": outcome.agent.get("llm_calls"),
                    "tool_calls": outcome.agent.get("tool_calls"),
                    "total_tokens": outcome.agent.get("total_tokens"),
                    "duration_sec": round(outcome.duration_sec, 2),
                    "network_attempt": outcome.network_attempt,
                }
            )
    return target


def write_report(
    output_dir: Path,
    outcomes: Sequence[RunOutcome],
    *,
    official: Optional[VariantSummary] = None,
    title: str = "评测结果",
) -> Path:
    """写出 markdown 报告 + 机器可读的汇总 JSON + 逐实例 CSV。"""
    output_dir = Path(output_dir)
    from .mutation import default_operators
    pools = {tuple(sorted(o.environment.get("mutation_operators") or default_operators())) for o in outcomes}
    if len(pools) > 1:
        raise ValueError("Cannot compare results from different scoring pools")
    restricted = bool(pools and next(iter(pools)) != tuple(sorted(default_operators())))
    if restricted and official is not None:
        raise ValueError("Restricted scoring needs a matching official baseline receipt")
    variants = sorted({outcome.variant for outcome in outcomes})
    summaries = [
        summarize_variant(variant, [o for o in outcomes if o.variant == variant])
        for variant in variants
    ]

    curves_by_variant = {
        variant: quality_curves([o for o in outcomes if o.variant == variant])
        for variant in variants
    }
    failures = {
        variant: failure_cases([o for o in outcomes if o.variant == variant])
        for variant in variants
    }

    sections: List[str] = [f"# {title}", ""]
    if restricted:
        sections += ["评分家族：" + ", ".join(next(iter(pools))) + "；不可与历史全家族分数直接比较。", ""]
    sections.append("## 主表")
    sections.append("")
    sections.append(render_main_table(summaries, official))
    sections.append("")
    if official:
        sections.append(
            "> 官方测试（HumanEval+ 自带测试）在同一套测量下的成绩，作为最强对照锚点。"
        )
        sections.append("")

    for variant in variants:
        sections.append(f"## {variant}：质量–预算曲线")
        sections.append("")
        sections.append(render_curve_table(curves_by_variant[variant]))
        sections.append("")
        sections.append("### 状态分布（ITT：全部计入分母）")
        sections.append("")
        sections.append(render_status_table([s for s in summaries if s.variant == variant]))
        sections.append("")
        sections.append("### 失败分类")
        sections.append("")
        for status, instance_ids in failures[variant].items():
            sections.append(f"- `{status}`（{len(instance_ids)}）：{', '.join(instance_ids)}")
        sections.append("")

    empty = [s.variant for s in summaries if s.n == 0]
    if empty:
        sections.append(f"> 注意：以下变体没有任何结果：{', '.join(empty)}")
        sections.append("")

    report_path = output_dir / "report.md"
    report_path.write_text("\n".join(sections), encoding="utf-8")

    (output_dir / "summary.json").write_text(
        json.dumps(
            {
                "variants": [summary.to_dict() for summary in summaries],
                "official_baseline": official.to_dict() if official else None,
                "curves": curves_by_variant,
                "failures": failures,
                "checkpoints": list(CHECKPOINTS),
                "mutation_operators": list(next(iter(pools))) if pools else [],
            },
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )
    write_csv(output_dir, outcomes)
    return report_path
