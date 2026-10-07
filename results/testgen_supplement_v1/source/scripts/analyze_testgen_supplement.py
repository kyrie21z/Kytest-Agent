"""Current-version descriptive A0-A4 comparison with explicit batch provenance."""
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from statistics import mean

from eval.dataset import load_dataset
from eval.mutation import generate_mutants
from scripts.analyze_ablation import bootstrap_ci, holm
from scipy.stats import wilcoxon

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("A0", "A1", "A2", "A3", "A4")
COMPARISONS = (("A0", "A1"), ("A1", "A2"), ("A2", "A3"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def summarize(output):
    manifest = json.loads((output / "manifest.json").read_text())
    baseline = ROOT / manifest["baseline_directory"]
    for name, expected_hash in manifest["baseline_sha256"].items():
        if sha(baseline / name) != expected_hash:
            raise ValueError("Reused baseline changed: " + name)
    instances = load_dataset(output / "source" / manifest["dataset"])
    totals = {x.instance_id: len(generate_mutants(x.solution_source)) for x in instances}
    if set(map(tuple, manifest["jobs"])) != {(v, iid) for v in ("A1", "A2", "A3") for iid in totals} or len(manifest["jobs"]) != 3*len(totals):
        raise ValueError("Supplement manifest job membership is invalid")
    rows, seen = [], set()
    for folder, allowed in ((baseline, ("A0", "A4")), (output, ("A1", "A2", "A3"))):
        expected = {(v, iid) for v in allowed for iid in totals}
        for path in sorted(folder.glob("A*/*.json")):
            d = json.loads(path.read_text()); key = (d["variant"], d["instance_id"])
            if key not in expected or key in seen or path.parent.name != key[0] or path.stem != key[1].replace("/", "__"):
                raise ValueError("Unexpected or duplicate supplement job: " + str(path))
            seen.add(key)
            f, a = d.get("final", {}), d.get("agent", {})
            actions = a.get("system_actions", [])
            modified = bool(d.get("solution_modified") or f.get("solution_modified") or any(x.get("solution_restored") for x in actions))
            valid = bool(f.get("all_pass")) and not modified
            total = totals[key[1]]
            measured = f.get("mutants_total") == total and f.get("mutation_score") is not None
            score = (f["mutants_killed"] / total if valid and measured else 0) if total else None
            tokens = a.get("input_tokens", 0) + a.get("output_tokens", 0)
            rows.append({"variant": key[0], "instance_id": key[1], "batch": "reused" if folder == baseline else "supplement",
                         "status": d["status"], "all_pass": bool(f.get("all_pass")), "valid_suite": valid,
                         "valid_mutation": score, "raw_mutation": f.get("mutation_score"),
                         "mutants_total": f.get("mutants_total", 0), "mutants_killed": f.get("mutants_killed", 0),
                         "mutants_errors": f.get("mutants_errors", 0), "line_coverage": f.get("line_coverage"),
                         "tokens": tokens, "over_soft_token_limit": tokens > manifest["total_token_limit"],
                         "generation_seconds": a.get("generation_seconds", 0), "measurement_seconds": f.get("eval_duration_sec", 0),
                         "network_attempt": bool(d.get("network_attempt")), "solution_modified": modified,
                         "system_actions": actions, "record_sha256": sha(path)})
    variants = {}
    for v in VARIANTS:
        selected = [r for r in rows if r["variant"] == v]
        def average(field):
            values = [r[field] for r in selected if r[field] is not None]
            return mean(values) if values else None
        actions = [a for r in selected for a in r["system_actions"]]
        variants[v] = {"runs": len(selected), "all_pass_rate": average("all_pass"), "valid_suite_rate": average("valid_suite"),
                       "valid_mutation": average("valid_mutation"), "raw_mutation": average("raw_mutation"),
                       "tokens": average("tokens"), "generation_seconds": average("generation_seconds"),
                       "measurement_seconds": average("measurement_seconds"), "line_coverage": average("line_coverage"),
                       "mutants_errors": sum(r["mutants_errors"] for r in selected), "status_counts": dict(Counter(r["status"] for r in selected)),
                       "network_attempts": sum(r["network_attempt"] for r in selected), "solution_modifications": sum(r["solution_modified"] for r in selected),
                       "over_soft_token_limit": sum(r["over_soft_token_limit"] for r in selected),
                       "system_pytest_runs": len(actions), "action_statuses": dict(Counter(a["status"] for a in actions)),
                       "decisions": dict(Counter(a["decision"] for a in actions)),
                       "coverage_rounds": sum(max([a.get("coverage_rounds", 0) for a in r["system_actions"]], default=0) for r in selected),
                       "coverage_incomplete_instances": sum(any(a.get("decision") == "coverage_incomplete" for a in r["system_actions"]) for r in selected),
                       "sut_restore_actions": sum(bool(a.get("solution_restored")) for a in actions)}
    expected_all = {(v, iid) for v in VARIANTS for iid in totals}
    complete = seen == expected_all
    comparisons = {}
    lookup = {(r["variant"], r["instance_id"]): r for r in rows}
    if complete:
        for left, right in COMPARISONS:
            diffs = [lookup[(right, iid)]["valid_mutation"] - lookup[(left, iid)]["valid_mutation"] for iid in sorted(totals) if totals[iid]]
            if not diffs:
                continue
            p = float(wilcoxon(diffs, zero_method="wilcox").pvalue) if any(diffs) else 1.0
            if not math.isfinite(p):
                raise ValueError("Nonfinite supplementary comparison")
            comparisons[right+"-"+left] = {"n": len(diffs), "mean_difference": mean(diffs), "bootstrap_ci95": bootstrap_ci(diffs),
                "wilcoxon_p": p, "all_pairs_tied": not any(diffs), "improved": sum(d > 0 for d in diffs),
                "tied": sum(d == 0 for d in diffs), "worse": sum(d < 0 for d in diffs), "cross_batch": left == "A0"}
        adjusted = holm({name: row["wilcoxon_p"] for name, row in comparisons.items()})
        for name, row in comparisons.items():
            row["holm_p"] = adjusted[name]
    summary = {"complete": complete, "expected_jobs": len(expected_all), "completed_jobs": len(rows),
               "new_jobs": sum(r["batch"] == "supplement" for r in rows), "reused_jobs": sum(r["batch"] == "reused" for r in rows),
               "variants": variants, "comparisons": comparisons, "per_run": rows,
               "excluded_zero_mutant_instances": [iid for iid, total in totals.items() if not total],
               "claim_boundary": "One sample per condition; A0/A4 reused from an earlier batch, A1-A3 generated later. Cross-batch exploratory comparison, not five-condition contemporaneous randomization or an unseen holdout. Equivalent mutants and sampling noise limit interpretation."}
    (output / "supplement_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2)+"\n")
    lines = ["# A1–A3正式20例补测", "", f"完成{len(rows)}/{len(expected_all)}：新增{summary['new_jobs']}，重用{summary['reused_jobs']}。", "",
             "| 条件 | runs | 全部通过 | 有效杀伤率 | 原始杀伤率 | token均值 | 生成秒 | 评分秒 | 变异超时 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for v, s in variants.items():
        if s["runs"]:
            valid = f"{s['valid_mutation']:.2%}" if s['valid_mutation'] is not None else "未测"
            raw = f"{s['raw_mutation']:.2%}" if s['raw_mutation'] is not None else "未测"
            lines.append(f"| {v} | {s['runs']} | {s['all_pass_rate']:.1%} | {valid} | {raw} | {s['tokens']:.0f} | {s['generation_seconds']:.1f} | {s['measurement_seconds']:.1f} | {s['mutants_errors']} |")
    lines += ["", "| 配对 | 差值(百分点) | 95%区间 | Wilcoxon p | Holm p | 改善/持平/退步 |", "|---|---:|---|---:|---:|---|"]
    for name, c in comparisons.items():
        lo, hi = c["bootstrap_ci95"]
        lines.append(f"| {name} | {100*c['mean_difference']:+.2f} | [{100*lo:+.2f}, {100*hi:+.2f}] | {c['wilcoxon_p']:.4g} | {c['holm_p']:.4g} | {c['improved']}/{c['tied']}/{c['worse']} |")
    lines += ["", "| 机制 | 系统pytest | PASS/FAIL/TIMEOUT | 覆盖率轮数 | 激活未覆盖补测的实例 |", "|---|---:|---|---:|---:|"]
    for v in ("A2", "A3"):
        s = variants[v]; counts = s["action_statuses"]
        lines.append(f"| {v} | {s['system_pytest_runs']} | {counts.get('PASS',0)}/{counts.get('FAIL',0)}/{counts.get('TIMEOUT',0)} | {s['coverage_rounds']} | {s['coverage_incomplete_instances']} |")
    lines += ["", "A0/A4来自先前批次，A1–A3是后续补测；跨批次A1−A0为探索性比较。",
              "每条件每例仅一次采样；正式集曾评测过，非新未见集。未显著不证明等价。",
              "失败套件计0；变异超时不计检出，疑似等价变异体未按结果排除。",
              "A4−A0原报告保留，未加入本轮三项Holm比较族。",
              "", "冻结协议见source/docs/testgen-supplement.md；配置、重用记录哈希与源码差异见manifest.json。",
              "详细分数、系统动作、成本与预算超额见supplement_summary.json。"]
    (output / "report.md").write_text("\n".join(lines)+"\n")
    return summary
