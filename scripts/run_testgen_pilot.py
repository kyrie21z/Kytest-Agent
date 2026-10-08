"""Run and summarize the frozen 5-case, 3-repeat A0/A4 development pilot."""
from __future__ import annotations

import argparse
import json
import random
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
from statistics import mean, pstdev

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from code_agent.config import Settings
from eval.dataset import load_dataset
from eval.experiment import freeze_sources, sha256_file as file_hash, write_json
from eval.mutation import generate_mutants
from eval.runner import default_variant, run_single, write_result


def specification(settings):
    files = sorted([*ROOT.glob("src/**/*.py"), *ROOT.glob("eval/*.py"),
                    Path(__file__), ROOT / "benchmarks/smoke_pool_5.jsonl", ROOT / "docs/testgen-pilot.md"])
    jobs = [(r, v, x.instance_id) for r in range(1, 4) for v in ("A0", "A4")
            for x in load_dataset(ROOT / "benchmarks/smoke_pool_5.jsonl")]
    random.Random(20261006).shuffle(jobs)
    return {"schema": "testgen-pilot-v2", "model": settings.model, "base_url": settings.base_url,
            "temperature": .2, "max_turns": 12, "output_token_limit": 4096,
            "total_token_limit": 30000, "generation_seconds": 300, "command_seconds": 10,
            "max_retries": 1, "concurrency": 2, "jobs": jobs,
            "measurement_seconds": {"pytest": 3, "coverage": 10, "per_mutant": 3},
            "files_sha256": {str(p.relative_to(ROOT)): file_hash(p) for p in files},
            "python": sys.version.split()[0], "execution_mode": "sandbox",
            "interpreter": sys.executable, "max_context_chars": settings.max_context_chars,
            "request_timeout_seconds": settings.request_timeout}


def summarize(output):
    rows = []
    reference_totals = {x.instance_id: len(generate_mutants(x.solution_source))
                        for x in load_dataset(ROOT / "benchmarks/smoke_pool_5.jsonl")}
    for path in sorted(output.glob("repeat_*/*/*.json")):
        d = json.loads(path.read_text())
        f, a = d["final"], d["agent"]
        score = f.get("mutation_score")
        rows.append({"repeat": path.parents[1].name, "variant": d["variant"], "instance_id": d["instance_id"],
                     "status": d["status"], "all_pass": bool(f.get("all_pass")),
                     "raw_mutation": score, "valid_mutation": (score if f.get("all_pass") and score is not None else 0)
                     if reference_totals.get(d["instance_id"], 0) else None,
                     "tokens": a.get("input_tokens", 0) + a.get("output_tokens", 0),
                     "generation_seconds": a.get("generation_seconds"), "measurement_seconds": f.get("eval_duration_sec"),
                     "accepted": len(a.get("testgen", {}).get("accepted", [])),
                     "rejected": sum(x["status"] not in ("ACCEPTED", "ALREADY_ACCEPTED") for x in a.get("testgen", {}).get("attempts", []))})
    variants = {}
    for v in ("A0", "A4"):
        selected = [r for r in rows if r["variant"] == v]
        scored = [r["valid_mutation"] for r in selected if r["valid_mutation"] is not None]
        variants[v] = {"runs": len(selected), "all_pass_rate": mean([r["all_pass"] for r in selected]) if selected else None,
                       "valid_mutation": mean(scored) if scored else None,
                       "tokens": mean([r["tokens"] for r in selected]) if selected else None,
                       "generation_seconds": mean([r["generation_seconds"] or 0 for r in selected]) if selected else None}
    paired = []
    for iid in sorted({r["instance_id"] for r in rows}):
        entry = {"instance_id": iid}
        for v in ("A0", "A4"):
            scores = [r["valid_mutation"] for r in rows if r["variant"] == v and r["instance_id"] == iid and r["valid_mutation"] is not None]
            entry[v] = {"n": len(scores), "mean": mean(scores) if scores else None, "sd": pstdev(scores) if scores else None}
        entry["delta"] = entry["A4"]["mean"] - entry["A0"]["mean"] if all(entry[v]["n"] == 3 for v in ("A0", "A4")) else None
        paired.append(entry)
    complete = len(rows) == 30 and all(e[v]["n"] == 3 for e in paired for v in ("A0", "A4"))
    delta = mean([p["delta"] for p in paired]) if complete else None
    go = complete and variants["A4"]["all_pass_rate"] >= variants["A0"]["all_pass_rate"] and delta > 0
    validity_path = output / "validity.json"
    validity = json.loads(validity_path.read_text()) if validity_path.exists() else {"comparable": True}
    go = go and validity["comparable"]
    summary = {"complete": complete, "variants": variants, "paired_instance_means": paired,
               "validity": validity,
               "delta_valid_mutation": delta, "candidate_for_independent_evaluation": go,
               "claim_boundary": "Development-only, five previously used smoke cases, three samples each. No population significance or final benchmark improvement proven.", "per_run": rows}
    write_json(output / "pilot_summary.json", summary)
    lines = ["# A4 开发试验结果", "", "开发池五例，每条件每例3次。所有run计入；无效套件的有效杀伤率为0。", "",
             "| 条件 | runs | all-pass | 有效杀伤率 | token均值 | 生成秒数 |", "|---|---:|---:|---:|---:|---:|"]
    if not validity["comparable"]:
        lines[:0] = ["# 环境诊断：不可用于机制比较", "", str(validity.get("reason", "Environmental mismatch")), "",
                     "本轮全部记录保留；不得用于质量优势结论或进入独立评测的决定。", ""]
    for v, s in variants.items():
        if s["runs"]:
            mutation = f"{s['valid_mutation']:.1%}" if s['valid_mutation'] is not None else "未测"
            lines.append(f"| {v} | {s['runs']} | {s['all_pass_rate']:.1%} | {mutation} | {s['tokens']:.0f} | {s['generation_seconds']:.1f} |")
    lines += ["", f"完整：{complete}；A4−A0平均有效杀伤率：{delta}；进入独立评测候选：{go}。", "",
              "仅支持开发池上的观察；不能证明总体质量收益。等价变异体未自动排除。", "",
              "逐实例重复均值、波动、拒绝数量及原始记录见 pilot_summary.json 和 repeat_*。"]
    (output / "report.md").write_text("\n".join(lines) + "\n")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results/testgen_pilot_v2")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    if args.report_only:
        print(json.dumps(summarize(args.output)["variants"], ensure_ascii=False)); return
    settings = Settings.from_env(workspace=ROOT)
    settings.require_llm()
    # Admission checks happen before any model request: both specialized execution
    # and the baseline's generic command must reach the exact same pytest runtime.
    import tempfile
    from code_agent.tools.shell_tools import RunCommandTool
    with tempfile.TemporaryDirectory(prefix="pilot-preflight-") as tmp:
        preflight = RunCommandTool(replace(settings, workspace=Path(tmp), allow_code_execution=True,
                                          execution_mode="sandbox", allow_write=True))
        result = preflight.run(command="python -m pytest --version")
        if not result.ok:
            raise SystemExit("Baseline pytest preflight failed: " + result.content)
        interpreter = preflight.run(command="python -c \"import sys; print(sys.executable)\"")
        if not interpreter.ok or sys.executable not in interpreter.content:
            raise SystemExit("Baseline interpreter differs from evaluator: " + interpreter.content)
    spec = specification(settings)
    output = args.output.resolve()
    freeze_sources(ROOT, output, spec)
    instances = {x.instance_id: x for x in load_dataset(ROOT / "benchmarks/smoke_pool_5.jsonl")}
    def factory(workspace):
        return replace(settings, workspace=workspace, temperature=.2, allow_code_execution=True,
                       execution_mode="sandbox", allow_write=True, exec_timeout=10, max_exec_timeout=10, max_retries=1)
    jobs = [job for job in spec["jobs"] if not (output / f"repeat_{job[0]}" / job[1] / (job[2].replace('/', '__') + '.json')).exists()]
    print(f"Pilot {settings.model}: {len(jobs)} pending / 30, API requests enabled", flush=True)
    def execute(job):
        repeat, name, iid = job
        variant = default_variant(name); variant.max_total_tokens = 30000
        outcome = run_single(instances[iid], variant, run_root=output / f"repeat_{repeat}/workspaces",
                             settings_factory=factory, checkpoints=(), wall_clock_limit=300,
                             defer_measurement=True, measurement_timeouts=(3, 10, 3))
        write_result(output / f"repeat_{repeat}", outcome)
        return repeat, name, iid, outcome
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(execute, job) for job in jobs]
        for f in as_completed(futures):
            repeat, name, iid, outcome = f.result()
            print(f"[{repeat}/{name}/{iid}] {outcome.status}, all_pass={outcome.final.get('all_pass')}, mutation={outcome.final.get('mutation_score')}, turns={outcome.agent.get('turns')}", flush=True)
    summary = summarize(output)
    print(json.dumps(summary["variants"], ensure_ascii=False), flush=True)
    print(f"Complete={summary['complete']}; candidate={summary['candidate_for_independent_evaluation']}", flush=True)


if __name__ == "__main__":
    main()
