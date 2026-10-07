"""Export minimal coursework evidence without changing any research originals."""
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]
from eval.dataset import load_dataset

ARCHIVE = "e34bb5c8770f85815612e5669a50a02a0c5f5532"
OUT = ROOT / "submission/evidence"
FIELDS = ["instance_id", "variant", "repeat", "batch", "status", "valid_suite",
          "score", "killed", "total", "tokens", "generation_seconds",
          "measurement_seconds", "record_path", "record_sha256"]

def read(name):
    return json.loads((ROOT / name).read_text())

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def export(study, rows):
    text = io.StringIO(newline="")
    writer = csv.DictWriter(text, fieldnames=FIELDS, lineterminator="\n")
    writer.writeheader()
    for row in rows:
        source = ROOT / row["record_path"]
        assert digest(source) == row["record_sha256"]
        assert abs(row["score"] - (row["killed"] / row["total"] if row["valid_suite"] else 0)) < 1e-12
        writer.writerow({**row, "valid_suite": int(row["valid_suite"])})
    (OUT / (study + ".csv")).write_text(text.getvalue())

def main():
    OUT.mkdir(parents=True, exist_ok=True)
    old = read("results/testgen_supplement_v1/supplement_summary.json")
    formal = read("results/testgen_formal_v1/formal_summary.json")
    new = read("results/testgen_quality_paired_v2/summary.json")
    rows = []
    for row in old["per_run"]:
        folder = "testgen_formal_v1" if row["variant"] in {"A0", "A4"} else "testgen_supplement_v1"
        rows.append({"instance_id":row["instance_id"], "variant":row["variant"], "repeat":1,
            "batch":row["batch"], "status":row["status"], "valid_suite":row["valid_suite"],
            "score":row["valid_mutation"], "killed":row["mutants_killed"], "total":row["mutants_total"],
            "tokens":row["tokens"], "generation_seconds":row["generation_seconds"],
            "measurement_seconds":row["measurement_seconds"],
            "record_path":f"results/{folder}/{row['variant']}/{row['instance_id'].replace('/', '__')}.json",
            "record_sha256":row["record_sha256"]})
    export("formal_v1", rows)
    rows = [{"instance_id":r["instance_id"], "variant":r["variant"], "repeat":r["repeat"],
        "batch":"interleaved", "status":r["status"], "valid_suite":r["valid_suite"],
        "score":r["confirmed_score"], "killed":r["mutants_killed"], "total":r["fixed_mutants_total"],
        "tokens":r["tokens"], "generation_seconds":r["generation_seconds"],
        "measurement_seconds":r["measurement_seconds"],
        "record_path":f"results/testgen_quality_paired_v2/repeat_{r['repeat']}/{r['variant']}/{r['instance_id'].replace('/', '__')}.json",
        "record_sha256":r["record_sha256"]} for r in new["per_run"]]
    export("paired_v2", rows)
    studies = {}
    for name, summary, repeats, seed in [("formal_v1",old,1,20261006),("paired_v2",new,3,20261007)]:
        variants = {}
        for variant, value in summary["variants"].items():
            variants[variant] = {"runs":value["runs"],
                "valid_suite_rate":value["valid_suite_rate"] if repeats==1 else value["valid_suite_mean"],
                "score":value["valid_mutation"] if repeats==1 else value["confirmed_score_mean"],
                "tokens":value["tokens"] if repeats==1 else value["tokens_mean"],
                "generation_seconds":value["generation_seconds"] if repeats==1 else value["generation_seconds_mean"],
                "measurement_seconds":value["measurement_seconds"] if repeats==1 else value["measurement_seconds_mean"]}
        studies[name] = {"tasks":20,"task_ids":sorted({row["instance_id"] for row in summary["per_run"]}),
                         "repeats":repeats,"seed":seed,"variants":variants,
                         "comparisons":summary["comparisons"]}
    studies["formal_v1"]["separate_comparison"] = {"A4-A0":formal["comparison"]}
    sources = ["results/testgen_formal_v1/formal_summary.json",
        "results/testgen_supplement_v1/supplement_summary.json",
        "results/testgen_quality_paired_v2/summary.json",
        "verification/testgen-quality-paired-v2/independent-replay.json",
        "verification/testgen-quality-paired-v2/stochastic-reference-diagnostic.json"]
    expected = {"scope":"Derived coursework rows; reconstruct statistics, not generation or complete mutation replay",
        "archive_commit":ARCHIVE,"archive_url":"https://github.com/kyrie21z/Kytest-Agent/tree/"+ARCHIVE,
        "source_sha256":{name:digest(ROOT/name) for name in sources},"studies":studies,
        "csv_sha256":{name:digest(OUT/name) for name in ["formal_v1.csv","paired_v2.csv"]}}
    (OUT/"expected.json").write_text(json.dumps(expected,ensure_ascii=False,indent=2)+"\n")
    sample = OUT / "real_run"
    sample.mkdir(exist_ok=True)
    for source, dest in [("results/testgen_quality_paired_v2/repeat_2/A5/MBPP__127.json","record.json"),
        ("results/testgen_quality_paired_v2/generation/repeat_2/A5/MBPP__127.json","generation.json"),
        ("results/testgen_quality_paired_v2/repeat_2/A5/MBPP__127.tests.py","test_solution.py")]:
        shutil.copyfile(ROOT/source,sample/dest)
    instance = next(x for x in load_dataset(ROOT/"benchmarks/mbpp_quality_v2_20.jsonl") if x.instance_id=="MBPP/127")
    (sample/"solution.py").write_text(instance.solution_source)
    (OUT/"README.md").write_text("""# 提交证据\n\nformal_v1.csv含100行，paired_v2.csv含180行；这些是从冻结原件导出的最小派生行，\n不是原始模型响应。每行带原件路径和SHA-256；expected.json带源报告和CSV哈希。\npython scripts/reproduce_submission.py重新核对成员、固定分母、均值和配对统计。\n\nreal_run/保留MBPP/127 repeat_2 A5的完整请求/响应、工具事件、原始结果及最终套件。\n它是专门用于展示反馈闭环的案例：独立检出2/3到3/3；不是随机代表样本，不替代\n全部180次的总体比较。公开MBPP的预训练接触未知。solution.py来自冻结数据。\n\n最新完整重放主分数180/180一致，参考和变异状态179/180一致；严格回执未通过。\n唯一差异是A0/MBPP/71 repeat_1的随机大列表揭示上游参考排序缺陷，原始0分保留。\n完整原件、严格失败回执和固定种子诊断见精简前Git版本，不能把派生统计重现\n称为全部程序重放成功。\n""")
    print("Exported 100 + 180 rows and one explicitly selected demonstration trace; originals unchanged.")

if __name__ == "__main__":
    main()
