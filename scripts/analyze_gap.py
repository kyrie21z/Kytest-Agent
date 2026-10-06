"""差异分析：A0 与官方测试逐实例对比，判断基准是否已经饱和。

为什么需要它：主表只给均值，而均值会掩盖关键结构。判断"这个基准对这个模型是不是太简单了"
需要看三件事：

1. **逐实例差值的分布**，而不是均值——均值 95% 可能由 28 个 100% 和 2 个 20% 组成；
2. **A0 在主终点上低于官方测试的实例**——这些才是"还有提升空间"的位置；
3. **A0 相对模型自身能力的位置**——如果它在主终点上处处打满，A1~A3 就没有可改善的余地，
   实验会退化成"证明不了任何差异"。

用法：
    python scripts/analyze_gap.py                 # A0 与官方 baseline 对比
    python scripts/analyze_gap.py --variant A1     # 指定变体
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "src"))
sys.path.insert(0, str(REPO_ROOT))


def _mean(values: List[float]) -> float:
    return statistics.fmean(values) if values else 0.0


def load_official(output_dir: Path) -> Dict[str, dict]:
    path = output_dir / "official_baseline.json"
    if not path.exists():
        return {}
    try:
        records = json.loads(path.read_text(encoding="utf-8"))["per_instance"]
    except (OSError, json.JSONDecodeError, KeyError):
        return {}
    return {record["instance_id"]: record for record in records}


def load_variant(output_dir: Path, variant: str) -> Dict[str, dict]:
    directory = output_dir / variant
    if not directory.is_dir():
        return {}
    results: Dict[str, dict] = {}
    for path in sorted(directory.glob("*.json")):
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        merged = dict(payload.get("final") or {})
        merged["_status"] = payload.get("status")
        merged["_agent"] = payload.get("agent") or {}
        results[payload.get("instance_id", path.stem)] = merged
    return results


def _fmt(value: Optional[float], scale: float = 100.0, suffix: str = "%") -> str:
    if value is None:
        return "n/a"
    return f"{value * scale:.0f}{suffix}"


def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="逐实例差异分析")
    parser.add_argument("--variant", default="A0")
    parser.add_argument("--output", default=str(REPO_ROOT / "results"))
    args = parser.parse_args(argv)

    output_dir = Path(args.output)
    official = load_official(output_dir)
    variant = load_variant(output_dir, args.variant)

    if not variant:
        print(f"没有找到 {args.variant} 的结果。先跑 scripts/run_eval.py run --variant {args.variant}")
        return 1

    ids = sorted(variant)
    print(f"变体 {args.variant}：{len(ids)} 个实例")
    print(f"官方 baseline：{len(official)} 个实例\n")

    # ---------- 逐实例表 ----------
    header = (
        f"{'instance':<16} {'status':<13} {'pass':>5} {'cov':>5} "
        f"{'mut':>6} {'官方mut':>8} {'差值':>6} {'turns':>5} {'tokens':>8}"
    )
    print(header)
    print("-" * len(header))

    deltas: List[float] = []
    rows: List[Tuple[str, Optional[float], Optional[float], float]] = []

    for instance_id in ids:
        record = variant[instance_id]
        base = official.get(instance_id, {})
        mut = record.get("mutation_score")
        base_mut = base.get("mutation_score")
        delta = (mut - base_mut) if (mut is not None and base_mut is not None) else None
        if delta is not None:
            deltas.append(delta)
            rows.append((instance_id, mut, base_mut, delta))
        print(
            f"{instance_id:<16} {str(record.get('_status')):<13} "
            f"{'Y' if record.get('all_pass') else 'n':>5} "
            f"{_fmt(record.get('line_coverage')):>5} "
            f"{_fmt(mut):>6} {_fmt(base_mut):>8} "
            f"{(f'{delta:+.0%}' if delta is not None else 'n/a'):>6} "
            f"{record['_agent'].get('turns', 0):>5} "
            f"{record['_agent'].get('total_tokens', 0):>8,}"
        )

    # ---------- 分布与判据 ----------
    print("\n" + "=" * 78)
    print("主终点分布")
    print("=" * 78)
    scores = [record["mutation_score"] for record in variant.values() if record.get("mutation_score") is not None]
    if scores:
        perfect = sum(1 for score in scores if score >= 0.999)
        print(f"  可测实例       {len(scores)}")
        print(f"  均值           {_mean(scores):.1%}")
        print(f"  中位数         {statistics.median(scores):.1%}")
        print(f"  打满 100% 的   {perfect} / {len(scores)}（{perfect / len(scores):.0%}）")
        buckets = {"100%": 0, "80-99%": 0, "50-79%": 0, "<50%": 0}
        for score in scores:
            if score >= 0.999:
                buckets["100%"] += 1
            elif score >= 0.8:
                buckets["80-99%"] += 1
            elif score >= 0.5:
                buckets["50-79%"] += 1
            else:
                buckets["<50%"] += 1
        print(f"  分档           {buckets}")

    if deltas:
        print(f"\n  与官方测试的差值：均值 {_mean(deltas):+.1%}，"
              f"中位数 {statistics.median(deltas):+.1%}")
        worse = [row for row in rows if row[3] < -0.001]
        better = [row for row in rows if row[3] > 0.001]
        same = [row for row in rows if abs(row[3]) <= 0.001]
        print(f"  不如官方测试   {len(worse)} 个：{[r[0] for r in worse]}")
        print(f"  与官方相同     {len(same)} 个")
        print(f"  好于官方测试   {len(better)} 个：{[r[0] for r in better]}")

    # ---------- 饱和判据 ----------
    print("\n" + "=" * 78)
    print("饱和判据")
    print("=" * 78)
    if not scores:
        print("  主终点未采集，无法判断。")
    else:
        perfect_ratio = sum(1 for score in scores if score >= 0.999) / len(scores)
        if perfect_ratio >= 0.8:
            print(f"  ⚠ 饱和：{perfect_ratio:.0%} 的实例在主终点上打满。")
            print("     A1~A3 没有可改善的余地——在这个基准 × 这个模型的组合下，")
            print("     消融实验无法产生有信息量的差异。建议换更难的基准或更弱的模型。")
        elif perfect_ratio >= 0.5:
            print(f"  ⚠ 接近饱和：{perfect_ratio:.0%} 的实例打满，提升空间有限。")
            print("     仍可做实验，但结论会是'小幅提升'，需要更多实例才能检出。")
        else:
            print(f"  ✓ 未饱和：仅 {perfect_ratio:.0%} 的实例打满，存在可测量的提升空间。")
            print("     可以做消融实验。")

    # ---------- 状态分布 ----------
    print("\n状态分布")
    status_counts: Dict[str, int] = {}
    for record in variant.values():
        status = str(record.get("_status"))
        status_counts[status] = status_counts.get(status, 0) + 1
    for status, count in sorted(status_counts.items(), key=lambda item: -item[1]):
        print(f"  {status:<14} {count}")

    unknowns = [i for i in ids if i not in official]
    if unknowns:
        print(f"\n注意：官方 baseline 里没有这些实例，未参与差值比较：{unknowns}")

    print(f"\n提示：报告里的失败分类见 {output_dir / 'report.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
