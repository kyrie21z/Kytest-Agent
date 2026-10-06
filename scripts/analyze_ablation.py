#!/usr/bin/env python3
"""消融配对分析：协议 §6 预注册的统计程序。

- 主终点：变异杀伤率，配对差值（同一实例上 variant B − variant A）
- 主比较：A0→A1、A1→A2、A2→A3（Holm 校正，familywise α=0.05）
- 效应量：均值差 + 95% bootstrap 置信区间（10000 次重采样，固定 seed=20261006）
- 显著性：Wilcoxon signed-rank（scipy，精确/正态近似由 scipy 自动选择）
- 次要分析：ΔQuality/ΔCost（杀伤率增量 / token 增量）与 all-pass 配对差
- ITT：所有实例进分母；timeout 按协议 §5 计分（测试已产出则按实际，否则 0）

用法：python scripts/analyze_ablation.py [--dir results/v2_ablation]
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import random
import re
import statistics
import sys
from pathlib import Path

from scipy import stats

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(REPO_ROOT / "src"), str(REPO_ROOT)]
from eval.report import summarize_variant, write_report
from eval.runner import RunOutcome

SEED = 20261006
BOOTSTRAP_N = 10000
MAIN_COMPARISONS = [("A0", "A1"), ("A1", "A2"), ("A2", "A3")]
DERIVATION_VERSION = "input-output-v1"


def derive_results(source: Path) -> Path:
    """从保存的 JSON 重算；原始 JSON/CSV/summary 全部保留，不作为当前总 token 来源。"""
    output = source / "derived" / "v1"
    outcomes = []
    hashes = {}
    historical = {}
    for variant in ("A0", "A1", "A2", "A3"):
        paths = sorted((source / variant).glob("*.json"))
        if not paths:
            raise ValueError(f"缺少 {variant} 的原始运行记录")
        seen = set()
        for path in paths:
            raw = path.read_bytes()
            record = json.loads(raw)
            if record["variant"] != variant or record["instance_id"] in seen:
                raise ValueError(f"变体或实例标识不一致：{path}")
            seen.add(record["instance_id"])
            hashes[str(path.relative_to(source))] = hashlib.sha256(raw).hexdigest()
            agent = dict(record["agent"])
            for key in ("input_tokens", "output_tokens"):
                if type(agent[key]) is not int or agent[key] < 0:
                    raise ValueError(f"非法 {key}：{path}")
            historical[f"{variant}/{record['instance_id']}"] = agent["total_tokens"]
            agent["total_tokens"] = agent["input_tokens"] + agent["output_tokens"]
            outcomes.append(RunOutcome(
                instance_id=record["instance_id"], variant=variant, status=record["status"],
                agent=agent, final=record["final"], checkpoints=record.get("checkpoints", []),
                duration_sec=float(record["duration_sec"]),
                network_attempt=bool(record.get("network_attempt", False)),
            ))
    ids = [{o.instance_id for o in outcomes if o.variant == v} for v in ("A0", "A1", "A2", "A3")]
    if any(group != ids[0] for group in ids[1:]):
        raise ValueError("四个变体的实例集合不一致，不能静默丢弃未配对记录")
    official = None
    baseline = source / "official_baseline.json"
    if baseline.exists():
        raw = baseline.read_bytes()
        hashes[baseline.name] = hashlib.sha256(raw).hexdigest()
        official = summarize_variant("官方测试锚点", [
            RunOutcome(instance_id=r["instance_id"], variant="official", final=r)
            for r in json.loads(raw)["per_instance"]
        ])
    output.mkdir(parents=True, exist_ok=True)
    write_report(output, outcomes, official=official, title="历史运行派生结果（input-output-v1）")
    # 派生摘要保留精确 token 均值；表格才进行显示舍入。
    summary_path = output / "summary.json"
    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    for row in summary["variants"]:
        row["tokens_mean"] = statistics.fmean(o.agent["total_tokens"] for o in outcomes
                                             if o.variant == row["variant"])
    summary["derivation_version"] = DERIVATION_VERSION
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    metadata = {
        "version": DERIVATION_VERSION,
        "token_formula": "agent.input_tokens + agent.output_tokens; cache hits are not added again",
        "scope": "Reanalysis of historical records; no new model generation or fee calculation",
        "source_sha256": hashes,
        "historical_total_tokens": historical,
        "token_means": {v: statistics.fmean(o.agent["total_tokens"] for o in outcomes if o.variant == v)
                        for v in ("A0", "A1", "A2", "A3")},
    }
    (output / "manifest.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return output


def load_per_instance(csv_path: Path) -> dict[str, dict[str, dict]]:
    """按 variant → instance_id 组织逐实例结果。"""
    table: dict[str, dict[str, dict]] = {}
    with csv_path.open("r", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            variant = row["variant"]
            score = row["mutation_score"].strip()
            table.setdefault(variant, {})[row["instance_id"]] = {
                "status": row["status"],
                "all_pass": row["all_pass"].strip().lower() == "true",
                "mutation_score": float(score) if score else None,
                "line_coverage": float(row["line_coverage"] or 0.0),
                "turns": int(row["turns"] or 0),
                "total_tokens": int(row["total_tokens"] or 0),
                "duration_sec": float(row["duration_sec"] or 0.0),
            }
    return table


def bootstrap_ci(diffs: list[float], *, n: int = BOOTSTRAP_N, seed: int = SEED) -> tuple[float, float]:
    rng = random.Random(seed)
    means = []
    for _ in range(n):
        sample = [diffs[rng.randrange(len(diffs))] for _ in range(len(diffs))]
        means.append(sum(sample) / len(sample))
    means.sort()
    return means[int(0.025 * n)], means[int(0.975 * n)]


def holm(pvalues: dict[str, float]) -> dict[str, float]:
    """Holm 逐步下降校正，返回校正后的 p 值。"""
    if any(not math.isfinite(p) or not 0 <= p <= 1 for p in pvalues.values()):
        raise ValueError("Holm 校正输入必须是有限的 [0, 1] p 值")
    ordered = sorted(pvalues.items(), key=lambda kv: kv[1])
    m = len(ordered)
    adjusted: dict[str, float] = {}
    running = 0.0
    for i, (name, p) in enumerate(ordered):
        value = min(1.0, (m - i) * p)
        running = max(running, value)
        adjusted[name] = running
    return adjusted


def paired(table: dict[str, dict[str, dict]], a: str, b: str, field: str = "mutation_score") -> dict:
    if set(table[a]) != set(table[b]):
        raise ValueError(f"{a}/{b} 实例集合不一致")
    ids = sorted(table[a])
    va = [table[a][i][field] for i in ids]
    vb = [table[b][i][field] for i in ids]
    if field == "mutation_score":
        # 协议 §2.1：无变异体实例杀伤率为 None，不进分母；两变体必须同时可测才配对
        pairs = [(x, y) for x, y in zip(va, vb) if x is not None and y is not None]
        va = [p[0] for p in pairs]
        vb = [p[1] for p in pairs]
    if field == "all_pass":
        va, vb = [int(x) for x in va], [int(y) for y in vb]
    if not va or any(not math.isfinite(x) for x in va + vb):
        raise ValueError(f"{a}→{b} 的 {field} 没有有效的有限配对数据")
    diffs = [y - x for x, y in zip(va, vb)]
    mean_diff = sum(diffs) / len(diffs)
    lo, hi = bootstrap_ci(diffs)
    non_zero = [d for d in diffs if d != 0]
    if non_zero:
        stat, p = stats.wilcoxon(vb, va, zero_method="wilcox")
        if not math.isfinite(float(stat)) or not math.isfinite(float(p)):
            raise ValueError(f"{a}→{b} 的 {field} 检验产生非有限统计量")
        test_status = "computed"
    else:
        # 所有配对完全相同：无可检验的秩差，显式标记，不调用会产生 nan 的路径。
        stat, p, test_status = None, 1.0, "all_pairs_tied"
    return {
        "n": len(diffs),
        "mean_a": sum(va) / len(va),
        "mean_b": sum(vb) / len(vb),
        "mean_diff": mean_diff,
        "ci": (lo, hi),
        "wilcoxon_p": p,
        "wilcoxon_statistic": stat,
        "test_status": test_status,
        "nonzero_pairs": len(non_zero),
        "improved": sum(1 for d in diffs if d > 0),
        "tied": sum(1 for d in diffs if d == 0),
        "worse": sum(1 for d in diffs if d < 0),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", default=str(REPO_ROOT / "results" / "v2_ablation"))
    parser.add_argument("--write-docs", action="store_true", help="同步仓库中标记的当前实验表格")
    args = parser.parse_args(argv)
    source = Path(args.dir).resolve()
    out_dir = derive_results(source)
    table = load_per_instance(out_dir / "per_instance.csv")
    print(f"数据口径：{DERIVATION_VERSION}；历史原始记录未修改；派生目录：{out_dir}\n")

    print("== 主比较（预注册：Holm 校正，Wilcoxon signed-rank，bootstrap 95% CI）==\n")
    results = {}
    for a, b in MAIN_COMPARISONS:
        results[f"{a}→{b}"] = paired(table, a, b)
    adjusted = holm({name: r["wilcoxon_p"] for name, r in results.items()})
    for name, r in results.items():
        lo, hi = r["ci"]
        print(
            f"{name:<8} n={r['n']:>2}  Δmutation = {r['mean_diff']:+.1%} "
            f"[{lo:+.1%}, {hi:+.1%}]  p(Wilcoxon)={r['wilcoxon_p']:.3f}  "
            f"p(Holm)={adjusted[name]:.3f}  改善/持平/变差 = {r['improved']}/{r['tied']}/{r['worse']}"
        )

    print("\n== 次要比较（链外对照，探索性）==\n")
    for a, b in [("A0", "A2"), ("A0", "A3"), ("A1", "A3"), ("A2", "A3")]:
        key = f"{a}→{b} (探索)"
        if key in results:
            continue
        r = paired(table, a, b)
        lo, hi = r["ci"]
        print(
            f"{key:<12} n={r['n']:>2}  Δmutation = {r['mean_diff']:+.1%} "
            f"[{lo:+.1%}, {hi:+.1%}]  p={r['wilcoxon_p']:.3f}"
        )

    print("\n== ΔQuality/ΔCost（预注册次要分析：每 10 万 token 的杀伤率增量）==\n")
    for a, b in MAIN_COMPARISONS:
        ids = sorted(table[a])
        ids = [i for i in ids if table[a][i]["mutation_score"] is not None
               and table[b][i]["mutation_score"] is not None]
        dq = [table[b][i]["mutation_score"] - table[a][i]["mutation_score"] for i in ids]
        dc = [(table[b][i]["total_tokens"] - table[a][i]["total_tokens"]) / 100000 for i in ids]
        # 只在 token 增量非零的实例上有定义
        ratios = [q / c for q, c in zip(dq, dc) if abs(c) > 1e-9]
        if ratios:
            print(f"{a}→{b}: 中位 ΔQ/ΔC = {sorted(ratios)[len(ratios)//2]:+.3f} / 10 万 token"
                  f"（均值 {sum(ratios)/len(ratios):+.3f}，n={len(ratios)}）")
        else:
            print(f"{a}→{b}: 所有实例 token 增量为 0，比值无定义")

    print("\n== 状态分布与成本 ==\n")
    variants = ["A0", "A1", "A2", "A3"]
    for v in variants:
        rows = table[v]
        statuses: dict[str, int] = {}
        for r in rows.values():
            statuses[r["status"]] = statuses.get(r["status"], 0) + 1
        n = len(rows)
        turns = sum(r["turns"] for r in rows.values()) / n
        tok = sum(r["total_tokens"] for r in rows.values()) / n
        print(f"{v}: {statuses}  turns={turns:.1f}  tokens={tok:,.0f}")

    print("\n== all-pass 配对差（门槛指标）==\n")
    for a, b in MAIN_COMPARISONS:
        r = paired(table, a, b, field="all_pass")
        print(f"{a}→{b}: all-pass {r['mean_a']:.0%} → {r['mean_b']:.0%}（Δ={r['mean_diff']:+.0%}，n={r['n']}）")

    (out_dir / "paired.json").write_text(json.dumps(
        {"version": DERIVATION_VERSION, "main": results, "holm": adjusted},
        ensure_ascii=False, indent=2, allow_nan=False,
    ) + "\n", encoding="utf-8")
    tables = render_tables(out_dir, table, results, adjusted)
    (out_dir / "tables.md").write_text("\n\n".join(tables.values()) + "\n", encoding="utf-8")
    if args.write_docs:
        if source != (REPO_ROOT / "results" / "v2_ablation").resolve():
            raise ValueError("--write-docs 只允许使用仓库的 v2_ablation 原始记录")
        sync_document_tables(tables)

    return 0


def render_tables(out_dir: Path, table: dict, results: dict, adjusted: dict) -> dict[str, str]:
    summary = json.loads((out_dir / "summary.json").read_text(encoding="utf-8"))
    main = ["| Variant | All-Pass | Line Cov. | Mutation（主终点） | Turns | Tokens | Runtime |",
            "|---|---:|---:|---:|---:|---:|---:|"]
    for row in summary["variants"]:
        v = row["variant"]
        tokens = statistics.fmean(r["total_tokens"] for r in table[v].values())
        main.append(f"| {v} | {row['all_pass_rate']:.1%} | {row['line_coverage']:.1%} | "
                    f"{row['mutation_mean']:.1%} ± {row['mutation_sd']:.1%} | "
                    f"{row['turns_mean']:.1f} | {tokens:,.0f} | {row['runtime_mean']:.0f}s |")
    row = summary.get("official_baseline")
    if row:
        main.append(f"| 官方测试锚点 | {row['all_pass_rate']:.1%} | {row['line_coverage']:.1%} | "
                    f"{row['mutation_mean']:.1%} ± {row['mutation_sd']:.1%} | — | — | — |")
    paired_lines = ["| 比较 | n | Δmutation | 95% CI | p(Wilcoxon) | p(Holm) | 改善/持平/变差 |",
                    "|---|---:|---:|---|---:|---:|---|"]
    costs = ["| 比较 | Δ杀伤率 | Δtokens（均值/实例） | Δturns |",
             "|---|---:|---:|---:|"]
    for a, b in MAIN_COMPARISONS:
        name = f"{a}→{b}"
        r = results[name]
        lo, hi = r["ci"]
        paired_lines.append(f"| {name} | {r['n']} | {r['mean_diff']:+.1%} | [{lo:+.1%}, {hi:+.1%}] | "
                            f"{r['wilcoxon_p']:.3f} | {adjusted[name]:.3f} | "
                            f"{r['improved']}/{r['tied']}/{r['worse']} |")
        ma, mb = [statistics.fmean(x["total_tokens"] for x in table[v].values()) for v in (a, b)]
        ta, tb = [statistics.fmean(x["turns"] for x in table[v].values()) for v in (a, b)]
        pct = f"{(mb / ma - 1):+.2%}" if ma else "不可计算"
        costs.append(f"| {name} | {r['mean_diff']:+.1%} | {mb-ma:+,.0f}（{pct}） | {tb-ta:+.1f} |")
    curves = ["| turn | A0 产出/通过 | A1 产出/通过 | A2 产出/通过 | A3 产出/通过 |",
              "|---:|---|---|---|---|"]
    for step in ("1", "2", "4", "8"):
        cells = []
        for v in ("A0", "A1", "A2", "A3"):
            records = summary["curves"][v].get(step)
            if not records:
                cells.append("未采集")
            else:
                r = records[0]
                cells.append(f"{r['has_tests_rate']:.0%} / {r['all_pass_rate']:.0%}（n={r['n']}）")
        curves.append(f"| {step} | " + " | ".join(cells) + " |")
    return {"main": "\n".join(main), "paired": "\n".join(paired_lines),
            "cost": "\n".join(costs), "curves": "\n".join(curves)}


def sync_document_tables(tables: dict[str, str]) -> None:
    updated = {}
    for path, names in (
        (REPO_ROOT / "README.md", ("main",)),
        (REPO_ROOT / "Design.md", ("main", "paired", "cost")),
        (REPO_ROOT / "results/v2_ablation/ANALYSIS.md", ("main", "paired", "cost", "curves")),
    ):
        text = path.read_text(encoding="utf-8")
        for name in names:
            pattern = rf"(<!-- ablation:{name}:start -->)\n.*?\n(<!-- ablation:{name}:end -->)"
            text, count = re.subn(pattern, lambda m: m[1] + "\n" + tables[name] + "\n" + m[2], text, flags=re.S)
            if count != 1:
                raise ValueError(f"文档表格标记缺失或重复：{path.name}/{name}")
        updated[path] = text
    for path, text in updated.items():
        path.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    sys.exit(main())
