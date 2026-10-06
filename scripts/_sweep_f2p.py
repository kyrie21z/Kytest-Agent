#!/usr/bin/env python3
"""用"整套测试对比"来判定 F2P，并在多个 bug 上统计命中率。

为什么不能只跑 `run_test.sh` 里那一条测试：它的断言可能根本没有覆盖补丁修复的行为。
youtube-dl bug 1 就是这种情况——补丁改的是布尔值处理，而目标测试用的全是字符串与整数，
于是 buggy 版本上测试照样通过，看起来像"bug 不存在"。

可靠的做法是把两个版本上的**整套测试结果都记下来**，取差集：
    在 buggy 上失败、在 fixed 上通过  =  这才是该 bug 的真实复现测试
如果差集为空，说明这个 bug 在当前环境下无法用测试区分，应当排除。

用法：
    python3 sweep_f2p.py youtube-dl --max-bugs 10
"""
import argparse
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

BUGSINPY = Path.home() / "bugs" / "BugsInPy"
WORK = Path.home() / "ws-sweep"


def parse_info(path: Path) -> dict:
    fields = {}
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        match = re.match(r'(\w+)\s*=\s*"?([^"]*)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def sh(cmd, cwd=None, env=None, timeout=900):
    return subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, shell=isinstance(cmd, str),
        capture_output=True, text=True, errors="replace", env=env, timeout=timeout,
    )


# pytest 汇总行里的失败用例名，例如 "FAILED test/test_utils.py::TestUtil::test_x"
_FAILED = re.compile(r"^(?:FAILED|ERROR)\s+(\S+)", re.MULTILINE)


def failing_tests(venv_bin: Path, repo: Path, env: dict) -> set:
    """跑整套 pytest，返回失败用例集合。"""
    result = sh([str(venv_bin / "python"), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider",
                 "--continue-on-collection-errors", "-x", "--co", "-q"], cwd=repo, env=env, timeout=300)
    # 先看能否收集；收集失败说明环境没搭好，直接返回空并标记
    result = sh([str(venv_bin / "python"), "-m", "pytest", "-q", "--no-header", "-p", "no:cacheprovider",
                 "--continue-on-collection-errors", "test/"], cwd=repo, env=env, timeout=900)
    return set(_FAILED.findall(result.stdout + result.stderr))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("project", nargs="?", default="youtube-dl")
    parser.add_argument("--max-bugs", type=int, default=10)
    args = parser.parse_args()

    project = args.project
    project_dir = BUGSINPY / "projects" / project
    repo_url = parse_info(project_dir / "project.info").get("github_url", "")
    if not repo_url:
        raise SystemExit(f"没找到 {project} 的仓库地址")

    bug_ids = sorted(
        [p.name for p in (project_dir / "bugs").iterdir() if p.is_dir() and p.name.isdigit()],
        key=int,
    )[: args.max_bugs]

    print(f"项目 {project}　仓库 {repo_url}")
    print(f"检查 {len(bug_ids)} 个 bug：{bug_ids}\n")

    WORK.mkdir(parents=True, exist_ok=True)
    venv = WORK / "venv"
    if not venv.exists():
        sh(["uv", "venv", "--python", "3.9", str(venv)], timeout=300)
    sh(["uv", "pip", "install", "--python", str(venv / "bin" / "python"),
        "pytest<9", "setuptools", "wheel"], timeout=600)
    env = os.environ.copy()
    env["PATH"] = f"{venv / 'bin'}{os.pathsep}" + env.get("PATH", "")

    repo = WORK / project
    if repo.exists():
        shutil.rmtree(repo, ignore_errors=True)
    sh(["git", "clone", "--quiet", repo_url, str(repo)], timeout=900)

    results = []
    for bug_id in bug_ids:
        bug_dir = project_dir / "bugs" / bug_id
        info = parse_info(bug_dir / "bug.info")
        patch = (bug_dir / "bug_patch.txt")
        if not patch.is_file():
            continue

        started = time.monotonic()
        sh(["git", "reset", "--hard", "--quiet"], cwd=repo)
        sh(["git", "clean", "-fdq"], cwd=repo)
        sh(["git", "checkout", "--quiet", info["buggy_commit_id"]], cwd=repo)

        # 用数据库记录的测试覆盖（若有）
        recorded = bug_dir / "tests"
        if recorded.is_dir():
            for source in recorded.rglob("*"):
                if source.is_file():
                    target = repo / source.relative_to(recorded)
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copyfile(source, target)

        buggy_failures = failing_tests(venv / "bin", repo, env)

        applied = sh(["git", "apply", str(patch)], cwd=repo)
        if applied.returncode != 0:
            sh(["patch", "-p1", "--forward", "-i", str(patch)], cwd=repo)
        fixed_failures = failing_tests(venv / "bin", repo, env)

        exposed = buggy_failures - fixed_failures
        elapsed = time.monotonic() - started
        results.append((bug_id, len(buggy_failures), len(fixed_failures), exposed, elapsed))
        mark = "✅" if exposed else "❌"
        print(f"{mark} bug {bug_id:<4} buggy 失败 {len(buggy_failures):<4} fixed 失败 {len(fixed_failures):<4} "
              f"差集 {len(exposed):<3} 用时 {elapsed:.0f}s")
        if exposed:
            for name in sorted(exposed)[:3]:
                print(f"        {name}")

    ok = sum(1 for r in results if r[3])
    print(f"\n{'='*78}\n汇总\n{'='*78}")
    print(f"  可用 bug（差集非空）：{ok} / {len(results)}")
    print(f"  平均每 bug 用时：{sum(r[4] for r in results)/max(1,len(results)):.0f}s")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
