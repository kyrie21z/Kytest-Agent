#!/usr/bin/env python3
"""F2P 判定扫描：BugsInPy 迁移可行性的决定性实验（第二轮）。

上一轮在 youtube-dl 上得到两个教训：
1. 目标测试可能根本不覆盖补丁修复的行为（bug 1：补丁改布尔处理，测试全用字符串）；
2. 工作区必须是干净的——上一轮打过补丁的仓库被复用，"buggy 版本"里跑的其实是已修复代码。

本脚本对每个 bug 直接 checkout buggy/fixed 两个 commit（不 apply 补丁，杜绝残留），
只跑 bug.info 里登记的目标测试文件，按四类分箱：

    F2P  buggy 失败 + fixed 通过   —— 可用（有区分度）
    P2P  两次都通过                —— 测试不暴露该 bug
    N2N  两次都失败                —— 多半是环境问题而非 bug
    ERR  测试文件缺失/收集失败等

判据（来自上次的约定）：第 2 步"挑出快且离线的项目"已通过（luigi/sanic/tqdm）；
本步回答"这些项目的 bug 有多少真正可复现"。若 F2P 占比可观（≥40%），
迁移路线可行；否则回退 HumanEval+ 并写明局限。

用法：
    python3 -u _f2p_sweep2.py                # 全部项目
    python3 -u _f2p_sweep2.py luigi sanic    # 指定项目
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


def sh(cmd, cwd=None, timeout=300):
    try:
        return subprocess.run(
            cmd, cwd=str(cwd) if cwd else None,
            capture_output=True, text=True, errors="replace", timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return None


def run_test(venv_bin: Path, repo: Path, test_file: str):
    """跑目标测试，返回 (分类用的简况, 是否有测试真正执行)。

    只认 pytest 的汇总行；收集失败/文件缺失都会反映在这里。
    """
    result = sh(
        [str(venv_bin / "python"), "-m", "pytest", "-q", "--no-header",
         "-p", "no:cacheprovider", "--no-summary", test_file],
        cwd=repo, timeout=TEST_TIMEOUT_SEC,
    )
    if result is None:
        return "TIMEOUT", None
    out = result.stdout or ""
    counts = {}
    for value, label in re.findall(
        r"(\d+)\s+(passed|failed|error(?:s)?|skipped)", out
    ):
        counts[label.rstrip("s")] = counts.get(label.rstrip("s"), 0) + int(value)
    if not counts and "error" in out.lower():
        return "COLLECT_ERROR", 0
    if not counts:
        return "NO_OUTPUT", None
    executed = counts.get("passed", 0) + counts.get("failed", 0)
    return counts, executed


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

        venv = WORK / f"{project}-venv"
        if not venv.exists():
            sh(["uv", "venv", "--python", "3.9", str(venv)], timeout=300)
        venv_bin = venv / "bin"
        sh(["uv", "pip", "install", "--python", str(venv_bin / "python"),
            "pytest<9", "setuptools", "wheel"], timeout=300)
        print(f"    安装 {project}（可编辑模式）…", flush=True)
        install = sh(["uv", "pip", "install", "--python", str(venv_bin / "python"),
                      "-e", ".", "--no-build-isolation"], cwd=repo, timeout=600)
        if install is None or install.returncode != 0:
            print(f"### {project}: 装不上，跳过\n")
            continue

        env = os.environ.copy()
        env["PATH"] = f"{venv_bin}{os.pathsep}" + env.get("PATH", "")
        env["PYTHONDONTWRITEBYTECODE"] = "1"

        bins = {"F2P": 0, "P2P": 0, "N2N": 0, "ERR": 0}
        details = []
        for bug_dir in bug_ids:
            info = parse_info(bug_dir / "bug.info")
            bug_id = int(bug_dir.name)
            test_file = info.get("test_file", "")
            buggy = info.get("buggy_commit_id", "")
            fixed = info.get("fixed_commit_id", "")
            if not (test_file and buggy and fixed):
                bins["ERR"] += 1
                details.append({"bug": bug_id, "cls": "ERR", "why": "元数据不全"})
                continue

            row = {"bug": bug_id, "test_file": test_file}
            outcome = {}
            for label, commit in (("buggy", buggy), ("fixed", fixed)):
                sh(["git", "checkout", "-f", "--quiet", commit], cwd=repo, timeout=300)
                sh(["git", "clean", "-fdq"], cwd=repo, timeout=120)
                counts, executed = run_test(venv_bin, repo, test_file)
                if isinstance(counts, str):
                    outcome[label] = counts
                elif counts.get("failed", 0) or counts.get("error", 0):
                    outcome[label] = "FAIL"
                elif counts.get("passed", 0):
                    outcome[label] = "PASS"
                else:
                    outcome[label] = "EMPTY"

            pair = (outcome["buggy"], outcome["fixed"])
            if pair == ("FAIL", "PASS"):
                bins["F2P"] += 1
                row["cls"] = "F2P"
            elif pair == ("PASS", "PASS"):
                bins["P2P"] += 1
                row["cls"] = "P2P"
            elif pair[0] == "FAIL" and pair[1] == "FAIL":
                bins["N2N"] += 1
                row["cls"] = "N2N"
            else:
                bins["ERR"] += 1
                row["cls"] = "ERR"
            row["outcome"] = f"{outcome['buggy']}→{outcome['fixed']}"
            details.append(row)
            print(f"    bug {bug_id:>3}  {row['outcome']:<18} {row['cls']}", flush=True)

        results[project] = {"bins": bins, "details": details}
        (WORK / f"result-{project}.json").write_text(
            json.dumps(details, indent=2, ensure_ascii=False), encoding="utf-8")
        total = sum(bins.values())
        print(f"### {project}: {bins}  F2P 占比 {bins['F2P']/total:.0%} ({total} 个 bug)\n", flush=True)

    print("=" * 70)
    grand_f2p = sum(r["bins"]["F2P"] for r in results.values())
    grand_total = sum(sum(r["bins"].values()) for r in results.values())
    print(f"总计：F2P {grand_f2p}/{grand_total} = {grand_f2p/max(1,grand_total):.0%}")
    for project, r in results.items():
        print(f"  {project:<8} {r['bins']}")
    (WORK / "result-all.json").write_text(
        json.dumps(results, indent=2, ensure_ascii=False), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
