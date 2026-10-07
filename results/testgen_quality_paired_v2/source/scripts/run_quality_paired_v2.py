"""Frozen, repeated A0/A4/A5 comparison; observe generation without scoring feedback."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, replace
import hashlib
import json
import math
import os
from pathlib import Path
import random
import shutil
from statistics import mean, pstdev
import subprocess
import sys
import tempfile
import time
import traceback

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from code_agent.agent import Agent, TurnDecision
from code_agent.config import Settings
from code_agent.fault_feedback import HELDOUT_OPERATORS, independent_pools
from code_agent.testgen import make_testgen_hook
from code_agent.tools.shell_tools import RunCommandTool
from eval.dataset import load_dataset
from eval.metrics import MEASUREMENT_VERSION, run_mutation_tests, run_pytest_on
from eval.runner import (RunOutcome, _build_llm, _tool_trace, default_variant,
                         environment_snapshot, run_single, write_result)
from scripts.analyze_ablation import bootstrap_ci, holm
from scipy.stats import wilcoxon

DATASET = ROOT / "benchmarks/mbpp_quality_v2_20.jsonl"
PROTOCOL = ROOT / "docs/testgen-quality-paired-v2.md"
VARIANTS = ("A0", "A4", "A5")
REPEATS = 3
SEED = 20261007
COMPARISONS = (("A0", "A4"), ("A0", "A5"), ("A4", "A5"))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    os.replace(temporary, path)


def result_path(output, job):
    repeat, variant, iid = job
    return output / f"repeat_{repeat}" / variant / (iid.replace("/", "__") + ".json")


def specification(settings):
    instances = load_dataset(DATASET)
    if len(instances) != 20 or len({x.instance_id for x in instances}) != 20:
        raise ValueError("The paired dataset must have exactly 20 unique tasks")
    rng = random.Random(SEED)
    blocks = [(repeat, x.instance_id) for repeat in range(1, REPEATS + 1) for x in instances]
    rng.shuffle(blocks)
    jobs = []
    for repeat, iid in blocks:
        names = list(VARIANTS)
        rng.shuffle(names)
        jobs.extend((repeat, name, iid) for name in names)
    files = sorted({*ROOT.glob("src/**/*.py"), *ROOT.glob("eval/*.py"),
        Path(__file__), ROOT / "scripts/freeze_mbpp_quality.py", ROOT / "scripts/analyze_ablation.py",
        ROOT / "scripts/verify_quality_paired_v2.py",
        DATASET, PROTOCOL, *ROOT.glob("benchmarks/mbpp_quality_v2/*"),
        ROOT / "requirements.txt", ROOT / "pyproject.toml"})
    return {"schema": "testgen-quality-paired-v2", "measurement_version": MEASUREMENT_VERSION,
        "model": settings.model, "base_url": settings.base_url, "temperature": .2,
        "max_turns": 12, "output_token_limit": 4096, "total_token_limit": 30000,
        "generation_seconds": 300, "budget_enforcement": "soft_between_turns",
        "command_seconds": 10, "request_timeout_seconds": 60, "max_retries": 1,
        "context_chars": 32000, "concurrency": 2, "repeats": REPEATS, "seed": SEED,
        "jobs": jobs, "scoring_operators": list(HELDOUT_OPERATORS), "scoring_limit": 20,
        "measurement_seconds": {"pytest": 10, "coverage": 20, "per_mutant": 5},
        "practical_target_difference": .05, "alpha": .05, "bootstrap_samples": 10000,
        "dataset": str(DATASET.relative_to(ROOT)), "protocol": str(PROTOCOL.relative_to(ROOT)),
        "source_revision": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "python": sys.version.split()[0], "interpreter": sys.executable,
        "files_sha256": {str(p.relative_to(ROOT)): sha(p) for p in files}}


def verify_frozen(output, live=False):
    manifest = json.loads((output / "manifest.json").read_text())
    if manifest["schema"] != "testgen-quality-paired-v2" or manifest["measurement_version"] != MEASUREMENT_VERSION:
        raise ValueError("Unexpected experiment or measurement version")
    for name, expected in manifest["files_sha256"].items():
        if sha(output / "source" / name) != expected:
            raise ValueError("Frozen source mismatch: " + name)
        if live and sha(ROOT / name) != expected:
            raise ValueError("Live source changed: " + name)
    return manifest


def freeze(output, spec):
    output.mkdir(parents=True, exist_ok=True)
    if (output / "manifest.json").exists():
        if json.loads(json.dumps(spec)) != verify_frozen(output, live=True):
            raise ValueError("Experiment inputs changed; use a new output directory")
        return
    if any(output.iterdir()):
        raise ValueError("New experiment output must be empty")
    for name, expected in spec["files_sha256"].items():
        destination = output / "source" / name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, destination)
        if sha(destination) != expected:
            raise ValueError("Source changed during freeze")
    write_json(output / "manifest.json", spec)


def admission(settings, instances):
    reference_rows = []
    with tempfile.TemporaryDirectory(prefix="quality-admission-") as tmp:
        workspace = Path(tmp)
        command = RunCommandTool(replace(settings, workspace=workspace, execution_mode="sandbox"))
        version = command.run(command="python -m pytest --version")
        interpreter = command.run(command='python -c "import sys; print(sys.executable)"')
        if not version.ok or not interpreter.ok or sys.executable not in interpreter.content:
            raise ValueError("Generic baseline does not use the evaluator Python/pytest")
        for instance in instances:
            source = workspace / "solution.py"
            source.write_text(instance.solution_source)
            (workspace / "test_solution.py").write_text(instance.official_test_source)
            reference = run_pytest_on("test_solution.py", workspace, timeout=10)
            development, heldout = independent_pools(instance.solution_source)
            if not reference.all_pass or source.read_text() != instance.solution_source or not development or not heldout:
                raise ValueError("Fixed reference admission failed: " + instance.instance_id + ": " + reference.summary_line)
            reference_rows.append({"instance_id": instance.instance_id, "passed": reference.all_pass,
                "development_total": len(development), "heldout_total": len(heldout), "ast_disjoint": True})
    return {"environment": environment_snapshot(), "interpreter": sys.executable,
            "generic_pytest_admitted": True, "fixed_references": reference_rows}


class ObservedLLM:
    """Record the actual model inputs, responses and faults shown; no policy changes."""
    def __init__(self, delegate, trace, path):
        self.delegate, self.trace, self.path = delegate, trace, path

    def chat(self, messages, tools=None):
        entry = {"started_at": time.time(), "messages": json.loads(json.dumps(messages)),
                 "tool_names": [x.get("function", {}).get("name") for x in tools or []]}
        self.trace["requests"].append(entry)
        write_json(self.path, self.trace)
        try:
            response = self.delegate.chat(messages, tools)
            entry["response"] = asdict(response)
            return response
        except Exception as exc:
            entry["error"] = str(exc)
            raise
        finally:
            entry["finished_at"] = time.time()
            write_json(self.path, self.trace)


def observer_factory(trace, path, events):
    def factory(variant, settings, registry, workspace):
        submitter, inspector = registry.get("submit_tests"), registry.get("inspect_survivors")
        if inspector:
            original_run = inspector.run
            def observed_feedback():
                previous = len(inspector.actions)
                suite = submitter.suite_source()
                response = original_run()
                if len(inspector.actions) > previous:
                    trace["development_stages"].append({"suite_source": suite,
                        "suite_sha256": hashlib.sha256(suite.encode()).hexdigest(),
                        "accepted_names": list(submitter.accepted),
                        "response": response.content, "report": inspector.actions[-1]})
                    write_json(path, trace)
                return response
            inspector.run = observed_feedback
        policy = make_testgen_hook(submitter) if submitter else None
        started = time.monotonic()
        def bounded(agent, outcome):
            decision = policy(agent, outcome) if policy else None
            if time.monotonic() - started >= 300:
                return TurnDecision(end=True, reason="generation_timeout")
            return decision
        def observe_event(event):
            events.append(event)
            trace.setdefault("events", []).append({"timestamp": time.time(), **event.to_dict()})
            if event.type == "run_end":
                trace["generation_finished_at"] = time.time()
        return Agent(llm=ObservedLLM(_build_llm(settings), trace, path), tools=registry,
            system_prompt=variant.resolve_system_prompt(), max_turns=variant.max_turns,
            max_total_tokens=variant.max_total_tokens, max_context_chars=settings.max_context_chars,
            finish_turn=bounded, on_event=observe_event)
    return factory


def confirmed_score(record, expected_total):
    final = record.get("final", {})
    valid = bool(final.get("all_pass")) and not bool(record.get("solution_modified") or final.get("solution_modified"))
    if final and final.get("measurement_version") != MEASUREMENT_VERSION:
        raise ValueError("Mixed measurement semantics")
    if valid:
        if final.get("mutants_total") != expected_total or final.get("mutation_score") is None:
            return 0.0
        killed = final.get("mutants_killed", 0)
        if not 0 <= killed <= expected_total:
            raise ValueError("Invalid confirmed detection count")
        return killed / expected_total
    return 0.0


def summarize(output):
    manifest = verify_frozen(output)
    instances = {x.instance_id: x for x in load_dataset(output / "source" / manifest["dataset"])}
    totals = {iid:len(independent_pools(x.solution_source)[1]) for iid,x in instances.items()}
    expected = {result_path(output, job) for job in manifest["jobs"]}
    actual = set(output.glob("repeat_*/A[045]/*.json"))
    if actual - expected:
        raise ValueError("Unexpected or duplicate experiment records")
    rows, lookup = [], {}
    for job in manifest["jobs"]:
        path = result_path(output, job)
        if not path.exists():
            continue
        repeat, variant, iid = job
        d = json.loads(path.read_text())
        if d.get("variant") != variant or d.get("instance_id") != iid:
            raise ValueError("Record membership mismatch")
        f, a = d.get("final", {}), d.get("agent", {})
        row = {"repeat": repeat, "variant": variant, "instance_id": iid, "status": d["status"],
            "valid_suite": bool(f.get("all_pass")) and not bool(d.get("solution_modified") or f.get("solution_modified")),
            "confirmed_score": confirmed_score(d, totals[iid]), "fixed_mutants_total": totals[iid],
            "mutants_killed": f.get("mutants_killed", 0),
            "upper_bound": f.get("mutation_upper_bound", 0), "completion_rate": f.get("mutation_completion_rate", 0),
            "mutation_status_counts": dict(Counter(x["status"] for x in f.get("mutant_results", []))),
            "tokens": a.get("input_tokens", 0) + a.get("output_tokens", 0),
            "generation_seconds": a.get("generation_seconds", 0), "measurement_seconds": f.get("eval_duration_sec", 0),
            "feedback_rounds": len(a.get("fault_feedback", [])),
            "accepted": len(a.get("testgen", {}).get("accepted", [])),
            "rejected": sum(x["status"] not in {"ACCEPTED", "ALREADY_ACCEPTED"} for x in a.get("testgen", {}).get("attempts", [])),
            "soft_time_overrun": a.get("generation_seconds", 0) > 300,
            "soft_token_overrun": a.get("input_tokens", 0) + a.get("output_tokens", 0) > 30000,
            "stop_reason": a.get("stop_reason"), "record_sha256": sha(path)}
        rows.append(row)
        lookup[(repeat, variant, iid)] = row
    complete = actual == expected
    variants = {}
    for variant in VARIANTS:
        selected = [r for r in rows if r["variant"] == variant]
        variants[variant] = {"runs": len(selected)}
        for key in ("valid_suite", "confirmed_score", "upper_bound", "completion_rate", "tokens",
                    "generation_seconds", "measurement_seconds", "feedback_rounds", "accepted"):
            variants[variant][key + "_mean"] = mean(r[key] for r in selected) if selected else None
        variants[variant]["status_counts"] = dict(Counter(r["status"] for r in selected))
        variants[variant]["mutation_status_counts"] = dict(sum((Counter(r["mutation_status_counts"]) for r in selected), Counter()))
        variants[variant]["soft_time_overruns"] = sum(r["soft_time_overrun"] for r in selected)
        variants[variant]["soft_token_overruns"] = sum(r["soft_token_overrun"] for r in selected)
    paired, comparisons = [], {}
    if complete:
        for iid in sorted(instances):
            entry = {"instance_id": iid}
            for variant in VARIANTS:
                samples = [lookup[(r, variant, iid)]["confirmed_score"] for r in range(1, REPEATS + 1)]
                entry[variant] = {"mean": mean(samples), "sd": pstdev(samples), "samples": samples}
            paired.append(entry)
        raw_p = {}
        for left, right in COMPARISONS:
            key = right + "-" + left
            diffs = [r[right]["mean"] - r[left]["mean"] for r in paired]
            p = float(wilcoxon(diffs, zero_method="wilcox").pvalue) if any(diffs) else 1.0
            if not math.isfinite(p):
                raise ValueError("Nonfinite paired p-value")
            raw_p[key] = p
            comparisons[key] = {"task_n": len(diffs), "mean_difference": mean(diffs),
                "bootstrap_ci95": bootstrap_ci(diffs, n=10000, seed=SEED), "wilcoxon_p": p,
                "improved": sum(x>0 for x in diffs), "tied": sum(x==0 for x in diffs), "worse": sum(x<0 for x in diffs),
                "practical_target_met": mean(diffs) >= .05}
        adjusted = holm(raw_p)
        for key, comparison in comparisons.items():
            right, left = key.split("-")
            comparison["holm_p"] = adjusted[key]
            comparison["quality_acceptance_passed"] = (comparison["practical_target_met"] and
                comparison["bootstrap_ci95"][0] > 0 and adjusted[key] < .05 and
                variants[right]["valid_suite_mean"] >= variants[left]["valid_suite_mean"])
    summary = {"schema":manifest["schema"], "measurement_version":MEASUREMENT_VERSION,
        "complete":complete, "expected_jobs":len(expected), "completed_jobs":len(rows),
        "task_count":len(instances), "repeats":REPEATS, "variants":variants,
        "comparisons":comparisons, "paired_task_means":paired, "per_run":rows,
        "claim_boundary":"Previously unused project MBPP tasks, public benchmark, one configured model, synthetic disjoint faults; no model-training novelty, real-bug generalization or hard-budget equality claim"}
    write_json(output / "summary.json", summary)
    lines = ["# 当前v2：A0/A4/A5重复配对结果", "", f"完成 {len(rows)}/{len(expected)}；20题，每条件每题3次生成。", "",
        "| 条件 | runs | 有效产出率 | 确认独立检出率 | 测量完成率 | token均值 | 生成秒数 |",
        "|---|---:|---:|---:|---:|---:|---:|"]
    for variant, d in variants.items():
        if d["runs"]:
            lines.append(f"| {variant} | {d['runs']} | {d['valid_suite_mean']:.1%} | {d['confirmed_score_mean']:.1%} | {d['completion_rate_mean']:.1%} | {d['tokens_mean']:.0f} | {d['generation_seconds_mean']:.1f} |")
    for key, d in comparisons.items():
        lo, hi = d["bootstrap_ci95"]
        lines += ["", f"{key}：{d['mean_difference']*100:+.2f}个百分点；任务层95%区间 [{lo*100:+.2f}, {hi*100:+.2f}]；",
                  f"Holm p={d['holm_p']:.6g}；改善/持平/退步={d['improved']}/{d['tied']}/{d['worse']}；质量验收通过={d['quality_acceptance_passed']}。"]
    lines += ["", "所有失败样本计0；先对每题3次生成取均值，再对20个任务等权分析。",
        "评分仅ROR/LCR/BCR，开发仅AOR/CRP；未知与可能等价项保留分母，不计检出。",
        "300秒和30000token均为轮间软上限；超界数量、成本及停止原因见summary.json。",
        "公开MBPP是否进入模型训练未知；结果不外推为真实仓库缺陷或总体质量等价。",
        "协议与源文件见source/docs/testgen-quality-paired-v2.md。"]
    (output / "report.md").write_text("\n".join(lines)+"\n")
    return summary


def execute(output, job, instances, settings):
    repeat, name, iid = job
    path = result_path(output, job)
    if path.exists():
        raise ValueError("Completed run is immutable")
    generation_path = output / "generation" / f"repeat_{repeat}" / name / (iid.replace("/", "__") + ".json")
    partial = []
    if generation_path.exists():
        preserved = generation_path.with_suffix(f".partial-{time.time_ns()}.json")
        generation_path.rename(preserved)
        partial.append(str(preserved.relative_to(output)))
    trace = {"job":job, "started_at":time.time(), "requests":[], "development_stages":[], "previous_partial_traces":partial}
    events = []
    def settings_factory(workspace):
        return replace(settings, workspace=workspace, temperature=.2, execution_mode="sandbox",
            allow_write=True, allow_code_execution=True, exec_timeout=10, max_exec_timeout=10,
            request_timeout=60, max_retries=1, max_context_chars=32000)
    variant = default_variant(name)
    variant.max_total_tokens = 30000
    try:
        outcome = run_single(instances[iid], variant, run_root=output / f"repeat_{repeat}" / "workspaces",
            settings_factory=settings_factory, agent_factory=observer_factory(trace, generation_path, events),
            checkpoints=(), defer_measurement=True, wall_clock_limit=300,
            mutation_operators=HELDOUT_OPERATORS, measurement_timeouts=(10,20,5))
    except Exception:
        outcome = RunOutcome(instance_id=iid, variant=name, status="eval_error", started_at=trace["started_at"],
            duration_sec=time.time()-trace["started_at"], error=traceback.format_exc(limit=6),
            environment={"measurement_version":MEASUREMENT_VERSION,
                "reference_mutants_total":len(independent_pools(instances[iid].solution_source)[1])})
    outcome.agent["tool_trace"] = _tool_trace(events)
    outcome.agent["generation_trace_file"] = str(generation_path.relative_to(output))
    trace["finished_at"] = time.time()
    trace["status"] = outcome.status
    write_json(generation_path, trace)
    write_result(output / f"repeat_{repeat}", outcome)
    return outcome


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results/testgen_quality_paired_v2")
    parser.add_argument("--freeze-only", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args()
    output = args.output.resolve()
    if args.report_only:
        summary = summarize(output)
        print(json.dumps({k:summary[k] for k in ("complete","completed_jobs","variants","comparisons")},ensure_ascii=False),flush=True)
        return
    settings = Settings.from_env(workspace=ROOT)
    settings.require_llm()
    if settings.model != "qwen3.7-flash":
        raise ValueError("Protocol model differs from configured model; revise protocol before freezing")
    settings = replace(settings, temperature=.2, llm_max_tokens=4096, request_timeout=60, max_retries=1)
    spec = specification(settings)
    freeze(output, spec)
    instances = {x.instance_id:x for x in load_dataset(DATASET)}
    if not (output / "admission.json").exists():
        write_json(output / "admission.json", admission(settings, instances.values()))
    if args.freeze_only:
        print(f"Frozen {len(spec['jobs'])} jobs, source_files={len(spec['files_sha256'])}; no model requests",flush=True)
        return
    if not (output / "api-admission.json").exists():
        response = _build_llm(replace(settings, llm_max_tokens=32)).chat([
            {"role":"user","content":"Reply with API_OK only."}])
        if "API_OK" not in response.content:
            raise ValueError("Live provider admission response was unexpected")
        write_json(output / "api-admission.json", {"model":settings.model,"timestamp":time.time(),
            "usage":response.usage,"response":response.content,"study_run":False})
    jobs = [job for job in spec["jobs"] if not result_path(output,job).exists()]
    print(f"Paired v2 {settings.model}: {len(jobs)} pending / 180, real model enabled",flush=True)
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(execute,output,job,instances,settings) for job in jobs]
        completed = len(spec["jobs"]) - len(jobs)
        for future in as_completed(futures):
            outcome = future.result()
            completed += 1
            print(f"[{completed}/180] {outcome.variant}/{outcome.instance_id}: {outcome.status}, confirmed={outcome.final.get('mutation_score')}, tokens={outcome.agent.get('total_tokens')}",flush=True)
    summary = summarize(output)
    print(json.dumps({k:summary[k] for k in ("complete","variants","comparisons")},ensure_ascii=False),flush=True)


if __name__ == "__main__":
    main()
