"""Independent post-generation replay and task-level aggregation; originals immutable."""
from __future__ import annotations

import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
import math
from pathlib import Path
import random
from statistics import mean
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from code_agent.fault_feedback import HELDOUT_OPERATORS, independent_pools
from eval.dataset import load_dataset
from eval.metrics import run_mutation_tests, run_pytest_on


def checksum(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replay_suite(instance, suite):
    with tempfile.TemporaryDirectory(prefix="quality-paired-replay-") as tmp:
        workspace = Path(tmp)
        source = workspace / "solution.py"
        source.write_text(instance.solution_source)
        (workspace / "test_solution.py").write_text(suite)
        reference = run_pytest_on("test_solution.py", workspace, timeout=10)
        changed = source.read_text() != instance.solution_source
        source.write_text(instance.solution_source)
        mutation = run_mutation_tests(workspace, instance.solution_source, "test_solution.py",
            baseline=reference, blocked_reason="solution_modified" if changed else "",
            operators=HELDOUT_OPERATORS, max_mutants=20, timeout=5)
        return {"reference_passed":reference.all_pass, "solution_modified":changed,
            "score":mutation["score"], "total":mutation["total"], "killed":mutation["killed"],
            "detected_ids":[x["mutant_id"] for x in mutation["mutant_results"] if x["status"]=="KILLED"],
            "statuses":{x["mutant_id"]:x["status"] for x in mutation["mutant_results"]},
            "reference_restored":source.read_text()==instance.solution_source}


def verify(output, receipt_path):
    manifest = json.loads((output / "manifest.json").read_text())
    if manifest["measurement_version"] != "valid-mutation-v2" or manifest["scoring_operators"] != list(HELDOUT_OPERATORS):
        raise ValueError("Unexpected scoring protocol")
    for name, digest in manifest["files_sha256"].items():
        if checksum(output / "source" / name) != digest or checksum(ROOT / name) != digest:
            raise ValueError("Frozen/live engine differs: " + name)
    instances = {x.instance_id:x for x in load_dataset(output / "source" / manifest["dataset"])}
    jobs = manifest["jobs"]
    expected = {output/f"repeat_{r}"/v/(iid.replace("/","__")+".json") for r,v,iid in jobs}
    if set(output.glob("repeat_*/A[045]/*.json")) != expected or len(expected)!=180:
        raise ValueError("Independent replay requires exactly 180 completed runs")
    original_hashes = {str(p.relative_to(output)):checksum(p) for p in expected}
    rows = []
    def one(job):
        repeat, variant, iid = job
        path = output/f"repeat_{repeat}"/variant/(iid.replace("/","__")+".json")
        d = json.loads(path.read_text()); f=d.get("final",{})
        suite_path = path.with_suffix(".tests.py")
        suite = suite_path.read_text() if suite_path.exists() else ""
        if len(suite)!=d["tests_chars"]:
            raise ValueError("Saved final suite changed")
        instance = instances[iid]
        total = len(independent_pools(instance.solution_source)[1])
        valid = f.get("all_pass",False) and not (d.get("solution_modified",False) or f.get("solution_modified",False))
        original_score = f.get("mutants_killed",0)/total if valid and f.get("mutants_total")==total else 0
        if suite:
            replay = replay_suite(instance,suite)
        else:
            replay = {"reference_passed":False,"score":0,"total":total,"killed":0,
                      "detected_ids":[],"statuses":{},"reference_restored":True,"solution_modified":False}
        # A restored test file cannot erase an observed generation-time SUT violation.
        replay_score = replay["score"] if valid else 0
        raw_match = (replay["killed"]==f.get("mutants_killed",0) and
                     (not f or replay["total"]==f.get("mutants_total")))
        original_statuses = {x["mutant_id"]:x["status"] for x in f.get("mutant_results",[])}
        row = {"repeat":repeat,"variant":variant,"instance_id":iid,"record_sha256":checksum(path),
            "tokens":d.get("agent",{}).get("input_tokens",0)+d.get("agent",{}).get("output_tokens",0),
            "original_score":original_score,"replay_score":replay_score,
            "reference_matches":replay["reference_passed"]==bool(f.get("all_pass")),
            "score_matches":math.isclose(original_score,replay_score,abs_tol=1e-12),
            "raw_counts_match":raw_match,"statuses_match":not suite or replay["statuses"]==original_statuses,
            "replay":replay}
        if variant=="A5":
            trace = json.loads((output/d["agent"]["generation_trace_file"]).read_text())
            stages = []
            for stage in trace["development_stages"]:
                stage_suite = stage["suite_source"]
                if hashlib.sha256(stage_suite.encode()).hexdigest()!=stage["suite_sha256"] or stage["report"]["suite_sha256"]!=stage["suite_sha256"]:
                    raise ValueError("Development stage suite identity mismatch")
                measured = replay_suite(instance,stage_suite)
                seen_by_model = any(stage["response"] in str(message.get("content", ""))
                    for request in trace["requests"] for message in request["messages"]
                    if message.get("role") in {"user","tool"})
                stages.append({"suite_sha256":stage["suite_sha256"],"accepted_names":stage["accepted_names"],
                    "seen_by_model":seen_by_model,"development_detected":stage["report"]["detected"],
                    "development_new_ids":stage["report"]["newly_detected_faults"],"heldout":measured})
            row["development_stages"]=stages
            if stages:
                before=set(stages[0]["heldout"]["detected_ids"])
                after=set(replay["detected_ids"])
                row["heldout_new_after_feedback"]=sorted(after-before)
                row["heldout_lost_after_feedback"]=sorted(before-after)
        return row
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(one,job) for job in jobs]
        for future in as_completed(futures):
            row=future.result(); rows.append(row)
            print(f"[replay {len(rows)}/180] {row['variant']}/{row['instance_id']}: reference={row['reference_matches']} score={row['score_matches']} raw={row['raw_counts_match']}",flush=True)
    independent={}
    for variant in ("A0","A4","A5"):
        selected=[r for r in rows if r["variant"]==variant]
        task_values=[]
        for iid in sorted(instances):
            task_values.append(mean(r["original_score"] for r in selected if r["instance_id"]==iid))
        independent[variant]={"runs":len(selected),"confirmed_score_mean":mean(task_values),
                              "tokens_mean":mean(r["tokens"] for r in selected)}
    summary=json.loads((output/"summary.json").read_text())
    summary_matches=all(math.isclose(value,summary["variants"][variant][key],abs_tol=1e-12)
        for variant,values in independent.items() for key,value in values.items())
    # Recalculate bootstrap independently of the reporting helper.
    from scipy.stats import wilcoxon
    comparison_audit={}; pvalues={}
    for left,right in (("A0","A4"),("A0","A5"),("A4","A5")):
        key=right+"-"+left
        differences=[]
        for iid in sorted(instances):
            differences.append(mean(r["original_score"] for r in rows if r["instance_id"]==iid and r["variant"]==right)-
                               mean(r["original_score"] for r in rows if r["instance_id"]==iid and r["variant"]==left))
        rng=random.Random(20261007)
        resampled=sorted(mean(differences[rng.randrange(len(differences))] for _ in differences) for _ in range(10000))
        fields={"mean_difference":mean(differences),"bootstrap_ci95":[resampled[250],resampled[9750]],
            "wilcoxon_p":float(wilcoxon(differences,zero_method="wilcox").pvalue) if any(differences) else 1.0}
        submitted=summary["comparisons"][key]
        matches=all(math.isclose(fields[k],submitted[k],abs_tol=1e-12) for k in ("mean_difference","wilcoxon_p"))
        matches &= all(math.isclose(a,b,abs_tol=1e-12) for a,b in zip(fields["bootstrap_ci95"],submitted["bootstrap_ci95"]))
        comparison_audit[key]={**fields,"matches":matches}; pvalues[key]=fields["wilcoxon_p"]
    maximum=0
    for rank,(key,pvalue) in enumerate(sorted(pvalues.items(),key=lambda x:x[1])):
        maximum=max(maximum,min(1,(3-rank)*pvalue))
        comparison_audit[key]["holm_p"]=maximum
        comparison_audit[key]["matches"] &= math.isclose(maximum,summary["comparisons"][key]["holm_p"],abs_tol=1e-12)
    historical=json.loads((output/"protected-files.json").read_text())
    historical_matches=all((ROOT/name).stat().st_size==entry["bytes"] and checksum(ROOT/name)==entry["sha256"]
                           for name,entry in historical["files"].items())
    originals_preserved=all(checksum(output/name)==digest for name,digest in original_hashes.items())
    feedback_rows=[r for r in rows if r["variant"]=="A5"]
    receipt={"scope":"Independent post-generation replay and frozen-record audit; no new model calls or score replacement",
        "jobs":len(rows),"frozen_source_files":len(manifest["files_sha256"]),
        "reference_matches":sum(r["reference_matches"] for r in rows),
        "score_matches":sum(r["score_matches"] for r in rows),
        "raw_counts_matches":sum(r["raw_counts_match"] for r in rows),
        "statuses_matches":sum(r["statuses_match"] for r in rows),
        "original_records_preserved":originals_preserved,"historical_files_checked":len(historical["files"]),
        "historical_files_preserved":historical_matches,"summary_matches":summary_matches,
        "independent_aggregation":independent,"comparison_audit":comparison_audit,
        "a5_feedback_runs":sum(bool(r.get("development_stages")) for r in feedback_rows),
        "a5_independent_gain_runs":sum(bool(r.get("heldout_new_after_feedback")) for r in feedback_rows),
        "a5_independent_loss_runs":sum(bool(r.get("heldout_lost_after_feedback")) for r in feedback_rows),
        "a5_feedback_stages_seen_by_model":sum(s["seen_by_model"] for r in feedback_rows for s in r.get("development_stages",[])),
        "rows":rows}
    receipt["primary_all_match"]=(all(r["reference_matches"] and r["score_matches"] and r["replay"]["reference_restored"] for r in rows)
        and summary_matches and originals_preserved and historical_matches and all(x["matches"] for x in comparison_audit.values()))
    receipt_path.parent.mkdir(parents=True,exist_ok=True)
    receipt_path.write_text(json.dumps(receipt,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in receipt.items() if k!="rows"},ensure_ascii=False),flush=True)
    if not receipt["primary_all_match"]:
        raise SystemExit("Independent primary verification differs; inspect preserved records")


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--results",type=Path,default=ROOT/"results/testgen_quality_paired_v2")
    parser.add_argument("--receipt",type=Path,required=True)
    args=parser.parse_args()
    verify(args.results.resolve(),args.receipt.resolve())


if __name__=="__main__":
    main()
