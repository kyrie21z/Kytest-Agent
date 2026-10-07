"""Validate the frozen v2 evidence on its corresponding release checkout."""
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify():
    manifest = read(HERE / "manifest.json")
    for name, expected in manifest["files_sha256"].items():
        assert sha(ROOT / name) == sha(HERE / "source" / name) == expected, name
    for name, expected in manifest["artifacts_sha256"].items():
        assert sha(HERE / name) == expected, name
    protected = read(HERE / "protected-files.json")
    for name, expected in protected["files_sha256"].items():
        assert sha(ROOT / name) == expected, name
    demo = read(HERE / "demo-receipt.json")
    replay = read(HERE / "independent-replay.json")
    assert replay["demo_receipt_sha256"] == sha(HERE / "demo-receipt.json")
    assert demo["quality_protocol_sha256"] == sha(ROOT / "docs/testgen-quality-v2.md")
    assert demo["protocol_sha256"] == sha(ROOT / "docs/fault-feedback.md")
    assert not set(demo["feedback_fingerprints"]) & set(demo["heldout_fingerprints"])
    for stage in ("before", "after"):
        assert replay["stages"][stage]["suite_sha256"] == sha(HERE / (stage + ".tests.py"))
        assert replay["stages"][stage]["baseline"]["all_pass"]
        assert replay["stages"][stage]["killed"] == demo["measurements"][stage]["detected"]
    assert replay["stages"]["before"]["killed"] == 0 and replay["stages"]["after"]["killed"] == 2
    assert replay["pools_disjoint"] and replay["all_stages_match"]
    reports = demo["development_feedback"]
    assert [r["detected"] for r in reports] == [1, 3]
    assert len(reports[1]["newly_detected_faults"]) == 2 and not reports[1]["lost_detections"]
    assert demo["reference_unchanged"] and demo["accepted"] == 5
    assert all(a["current_suite_checked"] for a in demo["quality_actions"])
    counts = re.search(r"(\d+) passed, (\d+) skipped", (HERE / "pytest.log").read_text())
    assert counts and tuple(map(int, counts.groups())) == (294, 4)
    return {"status": "PASS", "measurement_version": replay["measurement_version"],
            "base_revision": manifest["base_revision"], "source_files_verified": len(manifest["files_sha256"]),
            "historical_files_unchanged": len(protected["files_sha256"]), "project_tests_passed": 294, "windows_tests_skipped": 4,
            "development_detection_before_after": [1, 3], "development_faults_total": 3,
            "heldout_detection_before_after": [0, 2], "heldout_faults_total": 2,
            "independent_replay_matches": True, "feedback_and_scoring_pools_disjoint": True,
            "real_model_requests": 0,
            "scope": "Controlled mechanism acceptance, no real-model average-quality claim",
            "limitations": "Recognized constraints and executed paths only; complex oracles remain unproved. No transactional suite replacement; 300s generation limit remains soft between turns."}


if __name__ == "__main__":
    result = verify()
    previous = HERE / "acceptance.json"
    if previous.exists():
        assert result == read(previous), "Acceptance changed"
    print(json.dumps(result, ensure_ascii=False, indent=2))
