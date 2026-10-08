"""Recalculate saved evaluation statistics; no model calls or original-result writes."""
import argparse
import csv
import hashlib
import json
import math
from pathlib import Path
import random
from statistics import mean

ROOT = Path(__file__).resolve().parents[1]

def close(actual, expected):
    if not math.isfinite(actual) or not math.isclose(actual, expected, abs_tol=1e-10, rel_tol=1e-10):
        raise ValueError(f"Reported statistic differs: {actual} vs {expected}")

def comparisons(means, specification, seed, adjusted=True):
    from scipy.stats import wilcoxon
    result = {}
    for name, expected in specification.items():
        right,left = name.split("-")
        diffs = [means[right][iid]-means[left][iid] for iid in sorted(means[left])]
        rng = random.Random(seed)
        samples = sorted(mean(diffs[rng.randrange(len(diffs))] for _ in diffs) for _ in range(10000))
        p = float(wilcoxon(diffs,zero_method="wilcox").pvalue) if any(diffs) else 1.0
        value = {"mean_difference":mean(diffs),"bootstrap_ci95":[samples[250],samples[9750]],"wilcoxon_p":p}
        for key in ["mean_difference","wilcoxon_p"]:
            close(value[key],expected[key])
        for actual,target in zip(value["bootstrap_ci95"],expected["bootstrap_ci95"]):
            close(actual,target)
        result[name] = value
    if adjusted:
        maximum = 0
        for rank,(name,value) in enumerate(sorted(result.items(),key=lambda x:x[1]["wilcoxon_p"])):
            maximum = max(maximum,min(1,(len(result)-rank)*value["wilcoxon_p"]))
            value["holm_p"] = maximum
            close(maximum,specification[name]["holm_p"])
    return result

def verify(evidence):
    expected = json.loads((evidence/"expected.json").read_text())
    for filename,digest in expected["csv_sha256"].items():
        if hashlib.sha256((evidence/filename).read_bytes()).hexdigest()!=digest:
            raise ValueError("Evidence bytes changed: "+filename)
    report = {}
    for name, spec in expected["studies"].items():
        with (evidence/(name+".csv")).open(newline="") as file:
            rows = list(csv.DictReader(file))
        groups = {}
        seen = set()
        for row in rows:
            key = (row["variant"],row["instance_id"],int(row["repeat"]))
            if key in seen or key[0] not in spec["variants"] or not 1<=key[2]<=spec["repeats"]:
                raise ValueError("Unexpected or duplicate generation member")
            seen.add(key)
            valid = int(row["valid_suite"])
            killed,total = int(row["killed"]),int(row["total"])
            if valid not in (0,1) or total<=0 or not 0<=killed<=total:
                raise ValueError("Invalid fixed-pool denominator")
            score = float(row["score"])
            close(score,killed/total if valid else 0)
            if len(row["record_sha256"])!=64:
                raise ValueError("Missing original-record identity")
            groups.setdefault((key[0],key[1]),[]).append((score,row))
        tasks = {iid for variant,iid in groups}
        if tasks!=set(spec["task_ids"]) or len(tasks)!=spec["tasks"] or len(rows)!=len(spec["variants"])*spec["tasks"]*spec["repeats"]:
            raise ValueError("Incomplete task matrix")
        means = {}
        aggregate = {}
        for variant,target in spec["variants"].items():
            means[variant] = {}
            for iid in tasks:
                values = groups.get((variant,iid),[])
                if len(values)!=spec["repeats"]:
                    raise ValueError("Incomplete generation repeats")
                means[variant][iid] = mean(score for score,row in values)
            selected = [row for row in rows if row["variant"]==variant]
            value = {"runs":len(selected),"score":mean(means[variant].values()),
                "valid_suite_rate":mean(int(x["valid_suite"]) for x in selected),
                **{field:mean(float(x[field]) for x in selected)
                   for field in ["tokens","generation_seconds","measurement_seconds"]}}
            for field in value:
                close(value[field],target[field])
            aggregate[variant] = value
        report[name] = {"rows":len(rows),"variants":aggregate,
            "comparisons":comparisons(means,spec["comparisons"],spec["seed"])}
        if "separate_comparison" in spec:
            report[name]["separate_comparison"] = comparisons(means,spec["separate_comparison"],spec["seed"],False)
    return {"scope":"Derived statistical reconstruction only, not model generation or full program replay",
            "all_matches":True,"studies":report}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence",type=Path,default=ROOT/"docs/evidence")
    parser.add_argument("--output",type=Path)
    args = parser.parse_args()
    report = verify(args.evidence)
    text = json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if args.output:
        args.output.write_text(text)
    print(text,end="")

if __name__ == "__main__":
    main()
