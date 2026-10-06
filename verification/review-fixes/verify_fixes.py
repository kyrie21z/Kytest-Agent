"""验收保存的行为证据、派生统计和历史文件完整性；不会请求真实模型。"""
from pathlib import Path
import hashlib
import json
import math
import re
import sys

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()

def read(name):
    return json.loads((ROOT / name).read_text(encoding="utf-8"))

independent = read("independent_checks.json")
extra = read("additional_checks.json")
signal = read("interactive_abort_probe.json")
numeric = read("analysis_consistency.json")
artifacts = read("artifact_replay.json")
adapter = read("adapter_probe.json")
checks = {}
checks["F3_cancel_then_new_task"] = (
    signal["returncode"] == 0 and signal["http_requests"] == 2
    and signal["stderr"].count("[aborted]") == 1 and "[completed] turns=1" in signal["stderr"]
    and extra["task_and_checkpoint_budgets"]["same_task_total_turns"] == 3
    and extra["task_and_checkpoint_budgets"]["next_task_turns"] == 3
)
checks["A4_credentials_redacted"] = (
    not independent["session_redaction"]["dummy_credential_logged_in_plaintext"]
    and not extra["structured_credentials_redaction"]["plaintext_fields_in_log"]
    and extra["known_values_redaction"]["all_values_redacted"]
)
checks["Q3_command_boundary_and_read_budget"] = (
    not independent["workspace_boundary"]["command_tool_read_outside"]
    and not independent["allow_write_false"]["command_write_succeeded"]
    and extra["unterminated_output_peak_allocation"]["exit_code"] == 0
    and extra["unterminated_output_peak_allocation"]["stored_chars"] <= 1000
    and extra["unterminated_output_peak_allocation"]["reviewer_process_python_peak_bytes"] < 4 * 1024 * 1024
)
checks["D2_current_statistics_match_reference"] = (
    all(r["csv_uses_corrected_count"] and r["current_derived_summary_mean"] == r["corrected_input_plus_output_mean"]
        for r in numeric["token_counts"].values())
    and all(not r["submitted_p_is_nan"] and math.isclose(r["submitted_p"], r["reference_float_p"], abs_tol=1e-12)
            for r in numeric["mutation_paired_analysis"].values())
)
hashes = read("historical-results-sha256.json")
checks["historical_files_unchanged"] = all(
    hashlib.sha256((REPO / name).read_bytes()).hexdigest() == digest for name, digest in hashes.items()
)
table_blocks = {}
for filename, names in {"README.md": ["main"], "Design.md": ["main", "paired", "cost"],
                        "results/v2_ablation/ANALYSIS.md": ["main", "paired", "cost", "curves"]}.items():
    text = (REPO / filename).read_text(encoding="utf-8")
    for name in names:
        matched = re.search(rf"<!-- ablation:{name}:start -->\n(.*?)\n<!-- ablation:{name}:end -->", text, re.S)
        assert matched, (filename, name)
        assert name not in table_blocks or table_blocks[name] == matched[1], (filename, name)
        table_blocks[name] = matched[1]
checks["documentation_tables_consistent"] = (
    (REPO / "results/v2_ablation/derived/v1/tables.md").read_text(encoding="utf-8")
    == "\n\n".join(table_blocks[n] for n in ["main", "paired", "cost", "curves"]) + "\n"
)
checks["saved_tests_detect_faults_and_recover"] = len(artifacts["core_cases"]) == 5 and all(
    r["correct_original_all_runs"] and r["detects_independent_mutant"] for r in artifacts["core_cases"]
) and not artifacts["consistency_issues"]
checks["adapter_tool_roundtrip"] = adapter["function_call_roundtrip"]["tool_result_sent_in_next_request"]
log = (ROOT / "pytest.log").read_text(encoding="utf-8")
counts = re.search(r"(\d+) passed, (\d+) skipped", log)
assert counts and " failed" not in log
checks["full_regression"] = True
result = {"all_passed": all(checks.values()), "checks": checks,
          "pytest": {"passed": int(counts[1]), "skipped": int(counts[2]), "failed": 0},
          "historical_files_verified": len(hashes), "external_model_requests": 0,
          "scope": "Current local behavior and saved artifacts; no new model sampling or self-assigned grade"}
(ROOT / "acceptance.json").write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
assert result["all_passed"], checks
