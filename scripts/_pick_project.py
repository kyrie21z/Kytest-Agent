#!/usr/bin/env python3
"""挑项目：测每个候选项目的测试套件是否"快、离线、能收集"。

F2P 判定需要反复跑测试套件（每个 bug 至少两次：buggy 一次、fixed 一次）。
所以选项目的首要标准不是 bug 数量，而是**测试套件能不能在几十秒内跑完且不依赖网络**。

youtube-dl 在这条标准上直接出局：它的测试会访问网络，而且数量庞大，
光是收集和运行就超过 15 分钟——43 个 bug × 2 次 = 一天以上，不可行。

用法：
    python3 pick_project.py                # 测全部候选
    python3 pick_project.py thefuck black  # 只测指定项目
"""
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BUGSINPY = Path.home() / "bugs" / "BugsInPy"
WORK = Path.home() / "ws-pick"
BUDGET_SEC = 240


def parse_info(path: Path) -> dict:
    fields = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r'(\w+)\s*=\s*"?([^"]*)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def sh(cmd, cwd=None, env=None, timeout=BUDGET_SEC):
    try:
        return subprocess.run(
            cmd, cwd=str(cwd) if cwd else None, shell=isinstance(cmd, str),
            capture_output=True, text=True, errors="replace", env=env, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None


_COUNT = re.compile(r"(\d+)\s+(passed|failed|error|errors|skipped|deselected|selected)", re.I)
_SUMMARY = re.compile(r"^.*\bin \d+(?:\.\d+)?s.*$", re.MULTILINE)


def measure(venv_bin: Path, repo: Path, env: dict, test_path: str) -> dict:
    started = time.monotonic()
    result = sh([str(venv_bin / "python"), "-m", "pytest", "-q", "--no-header",
                 "-p", "no:cacheprovider", "--continue-on-collection-errors", test_path],
                cwd=repo, env=env)
    elapsed = time.monotonic() - started
    if result is None:
        return {"ok": False, "reason": f"超时（>{BUDGET_SEC}s）", "elapsed": elapsed}
    counts = {"passed": 0, "failed": 0, "errors": 0, "skipped": 0}
    summary = _SUMMARY.findall(result.stdout)
    if summary:
        for value, label in _COUNT.findall(summary[-1]):
            label = label.lower()
            if label == "passed":
                counts["passed"] = int(value)
            elif label == "failed":
                counts["failed"] = int(value)
            elif label.startswith("error"):
                counts["errors"] = int(value)
            elif label == "skipped":
                counts["skipped"] = int(value)
    return {
        "ok": bool(summary),
        "reason": summary[-1].strip() if summary else "没有汇总行（可能收集失败）",
        "elapsed": elapsed,
        "counts": counts,
        "returncode": result.returncode,
    }


def main() -> int:
    wanted = sys.argv[1:]
    project_root = BUGSINPY / "projects"
    candidates = []
    for project in sorted(project_root.iterdir()):
        if not project.is_dir():
            continue
        if wanted and project.name not in wanted:
            continue
        bugs = project / "bugs"
        if not bugs.is_dir():
            continue
        first = sorted([p for p in bugs.iterdir() if p.is_dir() and p.name.isdigit()], key=lambda p: int(p.name))
        if not first:
            continue
        info = parse_info(first[0] / "bug.info")
        candidates.append((project.name, info))

    print(f"候选 {len(candidates)} 个项目，单个项目预算 {BUDGET_SEC}s\n")
    WORK.mkdir(parents=True, exist_ok=True)
    venv = WORK / "venv"
    if not venv.exists():
        sh(["uv", "venv", "--python", "3.9", str(venv)], timeout=300)
    sh(["uv", "pip", "install", "--python", str(venv / "bin" / "python"),
        "pytest<9", "setuptools", "wheel", "pytest-timeout"], timeout=600)
    env = os.environ.copy()
    env["PATH"] = f"{venv / 'bin'}{os.pathsep}" + env.get("PATH", "")
    env["PYTHONDONTWRITEBYTECODE"] = "1"

    report = []
    report_path = WORK / "report.json"

    def record(entry: dict) -> None:
        """每处理完一个项目立刻写盘。上次运行就是死在'最后才写'上——
        中途被杀等于全部白跑。"""
        report.append(entry)
        report_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")

    for name, info in candidates:
        repo_url = parse_info(project_root / name / "project.info").get("github_url", "")
        if not repo_url:
            continue
        print(f"########## {name}  (py {info.get('python_version','?')})", flush=True)
        repo = WORK / name
        if repo.exists():
            shutil.rmtree(repo, ignore_errors=True)
        # 部分克隆：不下载全部历史 blob，checkout 老提交时按需拉取。
        # matplotlib/pandas 这类仓库全量克隆要几百 MB，部分克隆快一个数量级。
        cloned = sh(["git", "clone", "--filter=blob:none", "--quiet", repo_url, str(repo)], timeout=600)
        if cloned is None or not (repo / ".git").exists():
            print("  克隆失败，跳过\n", flush=True)
            record({"project": name, "clone_failed": True})
            continue
        sh(["git", "checkout", "--quiet", info["buggy_commit_id"]], cwd=repo)

        # 装依赖。uv venv 默认不带 pip，所以不能用 `python -m pip`——
        # 必须让 uv 直接对该解释器操作，否则所有项目都会倒在同一步。
        uv_python = str(venv / "bin" / "python")
        install = sh(["uv", "pip", "install", "--python", uv_python,
                      "-e", ".", "--no-build-isolation"],
                     cwd=repo, timeout=600)
        if install is None or install.returncode != 0:
            fallback = sh([str(venv / "bin" / "python"), "setup.py", "develop", "-q"], cwd=repo, timeout=600)
            if fallback is None or fallback.returncode != 0:
                print("  ⚠ 无法安装该包（可能需要编译依赖），跳过\n", flush=True)
                record({"project": name, "installable": False})
                continue

        # 测试目录：优先 test/，其次 tests/
        target = next((p for p in ("test", "tests") if (repo / p).is_dir()), None)
        if target is None:
            print("  没有 test/ 或 tests/ 目录，跳过\n", flush=True)
            record({"project": name, "installable": True, "no_test_dir": True})
            continue

        outcome = measure(venv / "bin", repo, env, target)
        verdict = "✅ 快且可收集" if outcome["ok"] and outcome["elapsed"] < 120 else (
            "⚠ 太慢" if outcome.get("elapsed", 0) >= 120 else "❌ 收集失败")
        print(f"  {verdict}  用时 {outcome['elapsed']:.0f}s  {outcome['reason'][:70]}\n", flush=True)
        record({"project": name, "installable": True, **outcome})

    print("=" * 78)
    print("汇总（按用时排序）")
    print("=" * 78)
    usable = [r for r in report if r.get("ok") and r.get("elapsed", 999) < 120]
    for row in sorted(usable, key=lambda r: r["elapsed"]):
        counts = row.get("counts", {})
        print(f"  {row['project']:<14} {row['elapsed']:>6.1f}s  "
              f"通过 {counts.get('passed',0):<5} 失败 {counts.get('failed',0):<4} 跳过 {counts.get('skipped',0)}")
    if not usable:
        print("  没有项目能在 120s 内跑完测试套件。")
    record_path = report_path
    record_path.write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
