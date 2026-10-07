"""Frozen supplementary A1/A2/A3 sampling; previously generated A0/A4 stay immutable."""
import argparse
import hashlib
import json
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

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT)]

from code_agent.config import Settings
from code_agent.tools.shell_tools import RunCommandTool
from eval.dataset import load_dataset
from eval.runner import RunOutcome, default_variant, environment_snapshot, run_single, write_result
from scripts.analyze_testgen_supplement import summarize
from scripts.run_testgen_formal import freeze, sha, specification as original_specification

BASELINE = ROOT / "results/testgen_formal_v1"
SEED = 20261006
STATE_LINE = '                bounded_hook.state = getattr(policy_hook, "state", None)\n'


def compatibility(baseline, settings):
    previous = json.loads((baseline / "manifest.json").read_text())
    if settings.model != previous["model"] or settings.base_url != previous["base_url"]:
        raise ValueError("Model/provider differs from reused formal baseline")
    changes = {}
    for name, expected in previous["files_sha256"].items():
        frozen = baseline / "source" / name
        if sha(frozen) != expected:
            raise ValueError("Baseline source snapshot changed: " + name)
        if sha(ROOT / name) != expected:
            current, original = (ROOT / name).read_text(), frozen.read_text()
            if name != "eval/runner.py" or current.count(STATE_LINE) != 1 or current.replace(STATE_LINE, "", 1) != original:
                raise ValueError("Shared baseline engine changed: " + name)
            changes[name] = {"previous_sha256": expected, "current_sha256": sha(ROOT / name),
                             "scope": "One state attribute assignment for output logging only; generation decisions unchanged"}
    expected_env = json.loads((baseline / "environment.json").read_text())
    current_env = environment_snapshot()
    for key in ("python", "platform", "pytest", "coverage"):
        if expected_env[key] != current_env[key]:
            raise ValueError("Environment differs from baseline: " + key)
    return changes


def specification(settings):
    changes = compatibility(BASELINE, settings)
    spec = original_specification(settings)
    files = [Path(__file__), ROOT / "scripts/analyze_testgen_supplement.py", ROOT / "docs/testgen-supplement.md"]
    spec["files_sha256"].update({str(p.relative_to(ROOT)): sha(p) for p in files})
    jobs = [(v, x.instance_id) for v in ("A1", "A2", "A3") for x in load_dataset(ROOT / spec["dataset"])]
    random.Random(SEED).shuffle(jobs)
    assert len(jobs) == len(set(jobs)) == 60
    baseline_files = [p for p in BASELINE.rglob('*') if p.is_file() and 'workspaces' not in p.relative_to(BASELINE).parts and '__pycache__' not in p.parts and p.suffix not in ('.pyc', '.pyo')]
    spec.update({"schema": "testgen-supplement-v1", "jobs": jobs, "protocol": "docs/testgen-supplement.md",
                 "baseline_directory": str(BASELINE.relative_to(ROOT)), "baseline_sha256": {str(p.relative_to(BASELINE)): sha(p) for p in sorted(baseline_files)},
                 "shared_engine_observability_delta": changes,
                 "hook_seconds": {"pytest": 90, "coverage_run": 180, "coverage_json": 120},
                 "variant_caps": {v: {"system_pytest": default_variant(v).system_runs_cap, "coverage_rounds": default_variant(v).coverage_rounds_cap} for v in ("A1", "A2", "A3")},
                 "comparisons": ["A1-A0", "A2-A1", "A3-A2"], "comparison_correction": "Holm, three comparisons",
                 "baseline_reuse_boundary": "A0/A4 run earlier; cross-batch exploratory comparison, not contemporaneous five-condition randomization"})
    return spec


def preflight(settings):
    with tempfile.TemporaryDirectory(prefix="supplement-preflight-") as tmp, tempfile.TemporaryDirectory(prefix="supplement-private-") as outside:
        tool = RunCommandTool(replace(settings, workspace=Path(tmp), allow_code_execution=True, execution_mode="sandbox", allow_write=True, max_exec_timeout=10))
        pytest = tool.run(command="python -m pytest --version")
        interpreter = tool.run(command='python -c "import sys; print(sys.executable)"')
        if not pytest.ok or not interpreter.ok or sys.executable not in interpreter.content:
            raise ValueError("Common Python/pytest preflight failed")
        canary = Path(outside) / "private.txt"; canary.write_text("preflight canary")
        probe = ("import os,socket\nfrom pathlib import Path\n"
                 f"assert not Path({str(canary)!r}).exists()\n"
                 "assert 'SUPPLEMENT_ADMISSION_SECRET' not in os.environ\n"
                 "assert not {'LLM_API_KEY','OPENAI_API_KEY','ANTHROPIC_API_KEY'} & set(os.environ)\n"
                 "s=socket.socket();s.settimeout(.3)\ntry:\n s.connect(('1.1.1.1',443))\n"
                 "except OSError:\n print('file, credential, network boundaries passed')\nelse:\n raise AssertionError('sandbox network escape')\n")
        saved = os.environ.get("SUPPLEMENT_ADMISSION_SECRET")
        os.environ["SUPPLEMENT_ADMISSION_SECRET"] = "preflight canary"
        try:
            boundary = tool.run(command="python -c " + shlex.quote(probe))
        finally:
            if saved is None: os.environ.pop("SUPPLEMENT_ADMISSION_SECRET", None)
            else: os.environ["SUPPLEMENT_ADMISSION_SECRET"] = saved
        if not boundary.ok:
            raise ValueError("Sandbox boundary preflight failed")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=ROOT / "results/testgen_supplement_v1")
    parser.add_argument("--prepare-only", action="store_true")
    parser.add_argument("--report-only", action="store_true")
    args = parser.parse_args(); output = args.output.resolve()
    if args.report_only:
        s = summarize(output); print(json.dumps({k:s[k] for k in ("complete", "variants", "comparisons")}, ensure_ascii=False)); return
    settings = Settings.from_env(workspace=ROOT); settings.require_llm()
    spec = specification(settings); preflight(settings); freeze(output, spec)
    environment = environment_snapshot()
    environment.update({"preflight_generic_pytest_passed": True, "preflight_interpreter_matches": True, "preflight_file_credential_network_boundaries_passed": True})
    (output / "environment.json").write_text(json.dumps(environment, ensure_ascii=False, indent=2)+"\n")
    if args.prepare_only:
        print(f"Frozen {len(spec['jobs'])} supplementary jobs; no model requests", flush=True); return
    instances = {x.instance_id: x for x in load_dataset(ROOT / spec["dataset"])}
    def factory(workspace):
        return replace(settings, workspace=workspace, temperature=.2, allow_code_execution=True, execution_mode="sandbox", allow_write=True,
                       exec_timeout=10, max_exec_timeout=10, max_retries=1, request_timeout=60, max_context_chars=32000)
    jobs = [j for j in spec["jobs"] if not (output / j[0] / (j[1].replace('/', '__')+'.json')).exists()]
    print(f"Supplement {settings.model}: {len(jobs)} pending / 60, API requests enabled", flush=True)
    def execute(job):
        name, iid = job; variant = default_variant(name); variant.max_total_tokens = 30000
        started = time.time()
        try:
            outcome = run_single(instances[iid], variant, run_root=output / "workspaces", settings_factory=factory,
                                 checkpoints=(), wall_clock_limit=300, defer_measurement=True, measurement_timeouts=(10,20,5))
            outcome.solution_modified |= any(a.get("solution_restored", False) for a in outcome.agent.get("system_actions", []))
        except Exception:
            outcome = RunOutcome(instance_id=iid, variant=name, status="eval_error", started_at=started,
                                 duration_sec=time.time()-started, error=traceback.format_exc(limit=6))
        write_result(output, outcome)
        return outcome
    with ThreadPoolExecutor(max_workers=2) as pool:
        futures = [pool.submit(execute, j) for j in jobs]
        for f in as_completed(futures):
            d = f.result()
            print(f"[{d.variant}/{d.instance_id}] {d.status}, all_pass={d.final.get('all_pass')}, mutation={d.final.get('mutation_score')}, actions={len(d.agent.get('system_actions',[]))}, turns={d.agent.get('turns')}", flush=True)
    s = summarize(output)
    print(json.dumps({k:s[k] for k in ("complete", "variants", "comparisons")}, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
