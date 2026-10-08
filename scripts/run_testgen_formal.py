"""Frozen A0/A4 comparison on all 20 formal instances; no strategy tuning."""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import shlex
import subprocess
import sys
import tempfile
import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import replace
from pathlib import Path
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from code_agent.config import Settings
from code_agent.tools.shell_tools import RunCommandTool
from eval.dataset import load_dataset
from eval.experiment import freeze_sources, sha256_file as sha, write_json
from eval.mutation import generate_mutants
from eval.runner import RunOutcome, default_variant, environment_snapshot, run_single, write_result
from scripts.analyze_ablation import bootstrap_ci
from scipy.stats import wilcoxon

DATASET = ROOT / "benchmarks/humaneval_plus_v2_20.jsonl"
PROTOCOL = ROOT / "docs/testgen-formal.md"
SEED = 20261006


def specification(settings):
    files = sorted({*ROOT.glob("src/**/*.py"), *ROOT.glob("eval/*.py"), Path(__file__),
                    ROOT / "scripts/analyze_ablation.py", DATASET, PROTOCOL,
                    ROOT / "requirements.txt", ROOT / "pyproject.toml"})
    jobs = [(v, x.instance_id) for v in ("A0", "A4") for x in load_dataset(DATASET)]
    random.Random(SEED).shuffle(jobs)
    assert len(jobs) == 40 and len({iid for _, iid in jobs}) == 20
    return {"schema": "testgen-formal-v1", "model": settings.model, "base_url": settings.base_url,
            "temperature": .2, "max_turns": 12, "output_token_limit": 4096,
            "total_token_limit": 30000, "generation_seconds": 300, "command_seconds": 10,
            "max_retries": 1, "concurrency": 2, "jobs": jobs,
            "measurement_seconds": {"pytest": 10, "coverage": 20, "per_mutant": 5},
            "files_sha256": {str(p.relative_to(ROOT)): sha(p) for p in files},
            "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
            "python": sys.version.split()[0], "interpreter": sys.executable,
            "execution_mode": "sandbox", "context_chars": 32000, "request_timeout_seconds": 60,
            "dataset": str(DATASET.relative_to(ROOT)), "protocol": str(PROTOCOL.relative_to(ROOT))}


def freeze(output, spec):
    freeze_sources(ROOT, output, spec)


def summarize(output):
    manifest = json.loads((output / "manifest.json").read_text())
    dataset = output / "source" / manifest["dataset"]
    totals = {x.instance_id: len(generate_mutants(x.solution_source)) for x in load_dataset(dataset)}
    expected = {(v, iid) for v, iid in manifest["jobs"]}
    rows, seen = [], set()
    for path in sorted(output.glob("A[04]/*.json")):
        d = json.loads(path.read_text()); key = (d["variant"], d["instance_id"])
        if key not in expected or key in seen:
            raise ValueError("Unexpected or duplicate formal job")
        seen.add(key)
        f, a = d.get("final", {}), d.get("agent", {})
        total = totals[d["instance_id"]]
        valid = bool(f.get("all_pass")) and not bool(d.get("solution_modified") or f.get("solution_modified"))
        measured = f.get("mutants_total") == total and f.get("mutation_score") is not None
        effective = (f["mutants_killed"] / total if valid and measured else 0) if total else None
        rows.append({"variant": d["variant"], "instance_id": d["instance_id"], "status": d["status"],
                     "all_pass": bool(f.get("all_pass")), "valid_suite": valid, "valid_mutation": effective,
                     "raw_mutation": f.get("mutation_score"), "expected_mutants": total,
                     "mutants_total": f.get("mutants_total", 0), "mutants_killed": f.get("mutants_killed", 0),
                     "mutants_errors": f.get("mutants_errors", 0), "line_coverage": f.get("line_coverage"),
                     "tokens": a.get("input_tokens", 0) + a.get("output_tokens", 0),
                     "generation_seconds": a.get("generation_seconds", 0),
                     "measurement_seconds": f.get("eval_duration_sec", 0),
                     "accepted": len(a.get("testgen", {}).get("accepted", [])),
                     "rejected": sum(x["status"] not in ("ACCEPTED", "ALREADY_ACCEPTED") for x in a.get("testgen", {}).get("attempts", [])),
                     "network_attempt": bool(d.get("network_attempt")), "solution_modified": not valid and bool(d.get("solution_modified") or f.get("solution_modified")),
                     "record_sha256": sha(path)})
    variants = {}
    for v in ("A0", "A4"):
        selected = [r for r in rows if r["variant"] == v]
        def average(field, exclude_none=False):
            values = [r[field] for r in selected if not exclude_none or r[field] is not None]
            return mean(values) if values else None
        counts = {s: sum(r["status"] == s for r in selected) for s in sorted({r["status"] for r in selected})}
        variants[v] = {"runs": len(selected), "all_pass_rate": average("all_pass"),
                       "valid_suite_rate": average("valid_suite"), "valid_mutation": average("valid_mutation", True),
                       "raw_mutation": average("raw_mutation", True), "tokens": average("tokens"),
                       "generation_seconds": average("generation_seconds"), "measurement_seconds": average("measurement_seconds"),
                       "line_coverage": average("line_coverage", True), "mutants_errors": sum(r["mutants_errors"] for r in selected),
                       "status_counts": counts, "accepted_mean": average("accepted"), "rejected_total": sum(r["rejected"] for r in selected)}
    paired = []
    lookup = {(r["variant"], r["instance_id"]): r for r in rows}
    for iid in sorted(totals):
        if all((v, iid) in lookup for v in ("A0", "A4")):
            a, b = lookup[("A0", iid)], lookup[("A4", iid)]
            paired.append({"instance_id": iid, "A0": a["valid_mutation"], "A4": b["valid_mutation"],
                           "delta": b["valid_mutation"] - a["valid_mutation"] if totals[iid] else None})
    complete = seen == expected
    diffs = [p["delta"] for p in paired if p["delta"] is not None]
    comparison = None
    if complete and diffs:
        pvalue = float(wilcoxon(diffs, zero_method="wilcox").pvalue) if any(d != 0 for d in diffs) else 1.0
        if not math.isfinite(pvalue):
            raise ValueError("Nonfinite formal Wilcoxon result")
        comparison = {"n": len(diffs), "mean_difference": mean(diffs), "bootstrap_ci95": bootstrap_ci(diffs),
                      "wilcoxon_p": pvalue, "all_pairs_tied": all(d == 0 for d in diffs),
                      "improved": sum(d > 0 for d in diffs), "tied": sum(d == 0 for d in diffs), "worse": sum(d < 0 for d in diffs)}
    summary = {"complete": complete, "expected_jobs": len(expected), "completed_jobs": len(rows),
               "variants": variants, "comparison": comparison, "paired": paired,
               "excluded_zero_mutant_instances": [iid for iid, n in totals.items() if not n],
               "claim_boundary": "One sample per condition on the previously evaluated formal 20-case set. Current-version paired comparison, not a new unseen holdout or a comparison with historical A0. Scores may include equivalent faults.",
               "per_run": rows}
    write_json(output / "formal_summary.json", summary)
    lines = ["# A4正式20例对照结果", "", f"完成：{len(rows)}/{len(expected)}；每条件每例一次；所有启动run计入。", "",
             "| 条件 | runs | all-pass | 有效杀伤率 | 原始杀伤率 | token均值 | 生成秒数 | 变异超时/错误数 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|"]
    for v, s in variants.items():
        if s["runs"]:
            def pct(field): return f"{s[field]:.1%}" if s[field] is not None else "未测"
            lines.append(f"| {v} | {s['runs']} | {pct('all_pass_rate')} | {pct('valid_mutation')} | {pct('raw_mutation')} | {s['tokens']:.0f} | {s['generation_seconds']:.1f} | {s['mutants_errors']} |")
    if comparison:
        ci = comparison["bootstrap_ci95"]
        lines += ["", f"A4−A0平均有效杀伤率差：{comparison['mean_difference']*100:+.2f}个百分点；",
                  f"95%配对bootstrap区间：[{ci[0]*100:+.2f}, {ci[1]*100:+.2f}]个百分点；Wilcoxon双侧p={comparison['wilcoxon_p']:.6g}。",
                  f"改善/持平/退步：{comparison['improved']}/{comparison['tied']}/{comparison['worse']}；全持平：{comparison['all_pairs_tied']}。"]
    lines += ["", "单次采样、曾评测过的20例、单一模型；不代表全新保留集或总体能力。",
              "疑似等价变异体未按本轮结果排除；超时变异体不计检出。旧版A0不混入配对。",
              "", "协议见source/docs/testgen-formal.md；逐实例差值、状态和成本见formal_summary.json。"]
    (output / "report.md").write_text("\n".join(lines)+"\n")
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results/testgen_formal_v1")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args(); output = args.output.resolve()
    if args.report_only:
        summary = summarize(output); print(json.dumps({k: summary[k] for k in ("complete", "variants", "comparison")}, ensure_ascii=False)); return
    settings = Settings.from_env(workspace=ROOT); settings.require_llm()
    with tempfile.TemporaryDirectory(prefix="formal-preflight-") as tmp, tempfile.TemporaryDirectory(prefix="formal-outside-") as outside:
        tool = RunCommandTool(replace(settings, workspace=Path(tmp), allow_code_execution=True,
                                      execution_mode="sandbox", allow_write=True, max_exec_timeout=10))
        result = tool.run(command="python -m pytest --version")
        interpreter = tool.run(command='python -c "import sys; print(sys.executable)"')
        if not result.ok or not interpreter.ok or sys.executable not in interpreter.content:
            raise SystemExit("Common Python/pytest sandbox preflight failed")
        canary = Path(outside) / "private.txt"
        canary.write_text("formal admission canary")
        probe = ("import os,socket\nfrom pathlib import Path\n"
                 f"assert not Path({str(canary)!r}).exists()\n"
                 "assert 'FORMAL_ADMISSION_SECRET' not in os.environ\n"
                 "assert not {'LLM_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY'} & set(os.environ)\n"
                 "s=socket.socket();s.settimeout(.3)\n"
                 "try:\n s.connect(('1.1.1.1',443))\n"
                 "except OSError:\n print('file, credential, network boundaries passed')\n"
                 "else:\n raise AssertionError('network escaped sandbox')\n")
        saved_secret = os.environ.get("FORMAL_ADMISSION_SECRET")
        os.environ["FORMAL_ADMISSION_SECRET"] = "formal-admission-canary"
        try:
            boundary = tool.run(command="python -c " + shlex.quote(probe))
        finally:
            if saved_secret is None:
                os.environ.pop("FORMAL_ADMISSION_SECRET", None)
            else:
                os.environ["FORMAL_ADMISSION_SECRET"] = saved_secret
        if not boundary.ok:
            raise SystemExit("Sandbox file/credential/network boundary preflight failed")
    spec = specification(settings); freeze(output, spec)
    environment = environment_snapshot()
    environment.update({"preflight_generic_pytest_passed": True, "preflight_interpreter_matches": True,
                        "preflight_file_credential_network_boundaries_passed": True})
    (output / "environment.json").write_text(json.dumps(environment, ensure_ascii=False, indent=2))
    instances = {x.instance_id: x for x in load_dataset(DATASET)}
    def factory(workspace):
        return replace(settings, workspace=workspace, temperature=.2, allow_code_execution=True,
                       execution_mode="sandbox", allow_write=True, exec_timeout=10, max_exec_timeout=10,
                       max_retries=1, request_timeout=60, max_context_chars=32000)
    jobs = [job for job in spec["jobs"] if not (output / job[0] / (job[1].replace('/', '__')+'.json')).exists()]
    print(f"Formal {settings.model}: {len(jobs)} pending / 40, API requests enabled", flush=True)
    def execute(job):
        name, iid = job; variant = default_variant(name); variant.max_total_tokens = 30000
        started = time.time()
        try:
            outcome = run_single(instances[iid], variant, run_root=output / "workspaces", settings_factory=factory,
                                 checkpoints=(), wall_clock_limit=300, defer_measurement=True,
                                 measurement_timeouts=(10,20,5))
        except Exception:
            outcome = RunOutcome(instance_id=iid, variant=name, status="eval_error", started_at=started,
                                 duration_sec=time.time()-started, error=traceback.format_exc(limit=6))
        write_result(output, outcome)
        return outcome
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(execute, job) for job in jobs]
        for f in as_completed(futures):
            d = f.result()
            print(f"[{d.variant}/{d.instance_id}] {d.status}, all_pass={d.final.get('all_pass')}, mutation={d.final.get('mutation_score')}, errors={d.final.get('mutants_errors')}, turns={d.agent.get('turns')}", flush=True)
    summary = summarize(output)
    print(json.dumps({k: summary[k] for k in ("complete", "variants", "comparison")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
