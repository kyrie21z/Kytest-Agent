#!/usr/bin/env python3
"""F2P 判定扫描 v3：BugsInPy 迁移可行性的决定性实验。

v2 的两个教训，都已修正：
1. 先 checkout 再安装。v2 在仓库 HEAD 上 `pip install -e .`，现代 HEAD 用
   hatchling/新版 Python，必然失败——而筛选脚本先 checkout 到老 commit 才装，
   所以它能装上。editable install 跟随 checkout 切换代码，依赖装一次即可。
2. 测试目标以 run_test.sh 为准（框架的 ground truth）：它跑的是具体测试节点
   （`file::Class::method`），不是整个文件；tqdm 还要求把包 build 进 pythonpath。

分类：F2P（buggy 失败 + fixed 通过，可用）/ P2P（两次都过，测试不暴露 bug）/
N2N（两次都失败，多半环境问题）/ ERR（元数据缺失、收集失败、超时）。

用法：python3 -u _f2p_sweep3.py [项目名 ...]   # 默认 luigi sanic tqdm
"""
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

BUGSINPY = Path.home() / "bugs" / "BugsInPy"
WORK = Path.home() / "ws-f2p2"
PER_PROJECT_BUG_CAP = 12
TEST_TIMEOUT_SEC = 90

PROJECTS = {
    "luigi": 33,
    "sanic": 5,
    "tqdm": 24,
}


def parse_info(path: Path) -> dict:
    fields = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r'(\w+)\s*=\s*"?([^"]*)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def pytest_target(run_test_path: Path) -> str:
    """从 run_test.sh 提取 pytest 目标。格式固定：`pytest <target>` 或
    `python3 -m pytest <target>`。提取不了返回空串。"""
    text = run_test_path.read_text(encoding="utf-8", errors="replace").strip()
    match = re.search(r"(?:python3? -m )?pytest\s+(.+)", text)
    return match.group(1).strip().strip('"\'') if match else ""


def sh(cmd, cwd=None, timeout=300):
    try:
        return subprocess.run(
            cmd, cwd=str(cwd) if cwd else None, shell=isinstance(cmd, str),
            capture_output=True, text=True, errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None


def run_test(venv_bin: Path, repo: Path, target: str):
    """跑 run_test.sh 指定的测试目标，返回 (结果分类, 汇总片段)。"""
    result = sh(
        f'"{venv_bin / "python"}" -m pytest -q --no-header -p no:cacheprovider {target}',
        cwd=repo, timeout=TEST_TIMEOUT_SEC,
    )
    if result is None:
        return "TIMEOUT", ""
    out = (result.stdout or "") + (result.stderr or "")
    summary = re.search(r"^\s*(?:=+.*)?\b(\d+)\s+(?:passed|failed)", out, re.M)
    counts = {}
    for value, label in re.findall(r"(\d+)\s+(passed|failed|error|errors|no tests ran)", out):
        key = "none" if label == "no tests ran" else label.rstrip("s")
        counts[key] = counts.get(key, 0) + int(value)
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    if counts.get("none"):
        return "NO_TESTS", tail
    if counts.get("failed") or counts.get("error"):
        return "FAIL", tail
    if counts.get("passed"):
        return "PASS", tail
    return "NO_TESTS", tail


def main() -> int:
    wanted = [a for a in sys.argv[1:] if a in PROJECTS] or list(PROJECTS)
    WORK.mkdir(parents=True, exist_ok=True)
    results = {}

    for project in wanted:
        bugs_root = BUGSINPY / "projects" / project / "bugs"
        bug_ids = sorted(
            (p for p in bugs_root.iterdir() if p.is_dir() and p.name.isdigit()),
            key=lambda p: int(p.name),
        )[:PER_PROJECT_BUG_CAP]
        if not bug_ids:
            print(f"### {project}: 没有 bug 目录\n")
            continue

        repo_url = parse_info(BUGSINPY / "projects" / project / "project.info").get("github_url", "")
        repo = WORK / project
        if repo.exists():
            shutil.rmtree(repo, ignore_errors=True)
        print(f"### {project}: 克隆 {repo_url}", flush=True)
        cloned = sh(["git", "clone", "--filter=blob:none", "--quiet", repo_url, str(repo)], timeout=600)
        if cloned is None or not (repo / ".git").exists():
            print(f"### {project}: 克隆失败\n")
            continue

        # 第一个 bug 的 buggy commit 是安装点：老 commit 是当年这套依赖能装的时代
        first_info = parse_info(bug_ids[0] / "bug.info")
        sh(["git", "checkout", "-f", "--quiet", first_info["buggy_commit_id"]], cwd=repo, timeout=300)

        venv = WORK / f"{project}-venv"
        if venv.exists():
            shutil.rmtree(venv, ignore_errors=True)
        sh(["uv", "venv", "--python", "3.9", str(venv)], timeout=300)
        venv_bin = venv / "bin"
        sh(["uv", "pip", "install", "--python", str(venv_bin / "python"),
            "pytest<9", "setuptools", "wheel"], timeout=300)
        print(f"    在 {first_info['buggy_commit_id'][:8]} 上安装 {project} …", flush=True)
        install = sh(["uv", "pip", "install", "--python", str(venv_bin / "python"),
                      "-e", ".", "--no-build-isolation"], cwd=repo, timeout=600)
        if install is None or install.returncode != 0:
            tail = (install.stderr or install.stdout or "").strip().splitlines()[-3:] if install else ["超时"]
            print(f"### {project}: 装不上，跳过 | {' / '.join(tail)}\n")
            continue

        env = os.environ.copy()
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        if (bug_ids[0] / "bug.info").exists():
            pythonpath = parse_info(bug_ids[0] / "bug.info").get("pythonpath", "")
            if pythonpath:
                env["PYTHONPATH"] = str(repo / pythonpath)

        bins = {"F2P": 0, "P2P": 0, "N2N": 0, "ERR": 0}
        details = []
        for bug_dir in bug_ids:
            info = parse_info(bug_dir / "bug.info")
            bug_id = int(bug_dir.name)
            target = pytest_target(bug_dir / "run_test.sh")
            row = {"bug": bug_id, "target": target}
            if not (target and info.get("buggy_commit_id") and info.get("fixed_commit_id")):
                bins["ERR"] += 1
                details.append({**row, "cls": "ERR", "why": "目标或 commit 缺失"})
                print(f"    bug {bug_id:>3}  ERR（目标或 commit 缺失）", flush=True)
                continue

            outcome = {}
            for label, commit in (("buggy", info["buggy_commit_id"]), ("fixed", info["fixed_commit_id"])):
                sh(["git", "checkout", "-f", "--quiet", commit], cwd=repo, timeout=300)
                sh(["git", "clean", "-fdq"], cwd=repo, timeout=120)
                outcome[label], tail = run_test(venv_bin, repo, target)
                row[f"{label}_tail"] = tail[:80]

            pair = (outcome["buggy"], outcome["fixed"])
            if pair == ("FAIL", "PASS"):
                bins["F2P"] += 1
                row["cls"] = "F2P"
            elif pair == ("PASS", "PASS"):
                bins["P2P"] += 1
                row["cls"] = "P2P"
            elif pair == ("FAIL", "FAIL"):
                bins["N2N"] += 1
                row["cls"] = "N2N"
            else:
                bins["ERR"] += 1
                row["cls"] = "ERR"
            details.append(row)
            print(f"    bug {bug_id:>3}  {pair[0]}→{pair[1]:<8} {row['cls']}", flush=True)

        results[project] = {"bins": bins, "details": details}
        (WORK / f"result-{project}.json").write_text(
            json.dumps(details, indent=2, ensure_ascii=False), encoding="utf-8")
        total = sum(bins.values())
        print(f"### {project}: {bins}  F2P 占比 {bins['F2P'] / total:.0%}（{total} 个 bug）\n", flush=True)

    print("=" * 70)
    grand_f2p = sum(r["bins"]["F2P"] for r in results.values())
    grand_total = sum(sum(r["bins"].values()) for r in results.values())
    print(f"总计：F2P {grand_f2p}/{grand_total} = {grand_f2p / max(1, grand_total):.0%}")
    for project, r in results.items():
        print(f"  {project:<8} {r['bins']}")
    (WORK / "result-all.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
