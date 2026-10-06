"""Check stored token accounting and mutation-analysis inputs without changing the submission."""
from __future__ import annotations

import csv
import importlib.util
import json
import math
from pathlib import Path
import statistics
import sys
import warnings

from scipy import stats

ROOT = Path(__file__).resolve().parent
REPO = Path(sys.argv[1]).resolve()
script = REPO / "scripts/analyze_ablation.py"
spec = importlib.util.spec_from_file_location("submitted_analysis", script)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
table = module.load_per_instance(REPO / "results/v2_ablation/derived/v1/per_instance.csv")
summary = json.loads((REPO / "results/v2_ablation/derived/v1/summary.json").read_text())
summary_by_variant = {row["variant"]: row for row in summary["variants"]}
token_totals = {}
for variant in ("A0", "A1", "A2", "A3"):
    records = [json.loads(p.read_text()) for p in (REPO / "results/v2_ablation" / variant).glob("*.json")]
    corrected = statistics.fmean(r["agent"]["input_tokens"] + r["agent"]["output_tokens"] for r in records)
    csv_total = statistics.fmean(row["total_tokens"] for row in table[variant].values())
    token_totals[variant] = {
        "corrected_input_plus_output_mean": corrected,
        "current_derived_csv_mean": csv_total,
        "current_derived_summary_mean": summary_by_variant[variant]["tokens_mean"],
        "csv_uses_corrected_count": abs(corrected - csv_total) < 0.01,
    }

comparisons = {}
for a, b in module.MAIN_COMPARISONS:
    ids = sorted(set(table[a]) & set(table[b]))
    pairs = [(table[a][i]["mutation_score"], table[b][i]["mutation_score"]) for i in ids]
    pairs = [(x, y) for x, y in pairs if x is not None and y is not None]
    va, vb = [x for x, y in pairs], [y for x, y in pairs]
    with warnings.catch_warnings(record=True) as captured:
        warnings.simplefilter("always")
        submitted = module.paired(table, a, b)
    # Reviewer reference calculation preserves the recorded fractions.
    reference = stats.wilcoxon(vb, va, zero_method="wilcox")
    actual_p = float(submitted["wilcoxon_p"])
    comparisons[f"{a}->{b}"] = {
        "nonzero_float_pairs": sum(x != y for x, y in pairs),
        "nonzero_pairs_if_using_old_integer_cast": sum(int(x) != int(y) for x, y in pairs),
        "submitted_p": actual_p if math.isfinite(actual_p) else None,
        "submitted_p_is_nan": math.isnan(actual_p),
        "reference_float_p": float(reference.pvalue),
        "warnings": [str(item.message) for item in captured],
    }

a1 = token_totals["A1"]["corrected_input_plus_output_mean"]
a2 = token_totals["A2"]["corrected_input_plus_output_mean"]
output = {
    "token_counts": token_totals,
    "corrected_A1_to_A2_token_reduction": 1 - a2 / a1,
    "mutation_paired_analysis": comparisons,
    "scope": "Local numeric recalculation of saved records, not model regeneration or verification of historical call authenticity",
}
(ROOT / "analysis_consistency.json").write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(output, ensure_ascii=False, indent=2))
