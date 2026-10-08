#!/usr/bin/env python3
"""验证 BugsInPy 的 F2P 机制：在 buggy 版本上测试必须失败，打完补丁必须通过。

这是整个迁移路线的**决定性实验**。它不写任何评测代码，只回答一个问题：
"这台机器能不能把某个真实 bug 的复现环境搭起来并对它做 F2P 判定？"

流程：
  1. 检出 buggy commit，跑目标测试 → 期望失败
  2. 打上官方补丁，再跑同一个测试 → 期望通过

两步都符合预期，才说明 F2P 判据在这个环境里是可信的。
"""
import re
import shutil
import subprocess
import sys
from pathlib import Path

BUGSINPY = Path.home() / "bugs" / "BugsInPy"
WORK = Path.home() / "ws-f2p"


def run(cmd, cwd=None, check=False, quiet=False, env=None):
    result = subprocess.run(
        cmd, cwd=str(cwd) if cwd else None, shell=isinstance(cmd, str),
        capture_output=True, text=True, errors="replace", env=env,
    )
    if not quiet:
        print(f"$ {' '.join(cmd) if isinstance(cmd, list) else cmd}")
        if result.stdout.strip():
            print(result.stdout[-2500:])
        if result.stderr.strip():
            print("[stderr]", result.stderr[-1200:])
    if check and result.returncode != 0:
        raise SystemExit(f"命令失败（退出码 {result.returncode}）")
    return result


def make_env(venv_bin: Path):
    """把 venv 的 bin 放到 PATH 最前，让脚本里的 `python` 解析到它。

    BugsInPy 的 run_test.sh 直接写 `python`，而这些项目是 py3.7 时代的——
    机器上只有 python3.14/3.9，没有叫 `python` 的命令。不处理的话
    测试会因为"命令找不到"（退出码 127）而失败，看起来像 bug 复现了，其实是假象。
    """
    import os

    env = os.environ.copy()
    env["PATH"] = f"{venv_bin}{os.pathsep}" + env.get("PATH", "")
    return env


def parse_info(path: Path) -> dict:
    fields = {}
    for line in (path.read_text(encoding="utf-8", errors="replace")).splitlines():
        match = re.match(r'(\w+)\s*=\s*"?([^"]*)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def main() -> int:
    project = sys.argv[1] if len(sys.argv) > 1 else "youtube-dl"
    bug_id = sys.argv[2] if len(sys.argv) > 2 else "1"

    bug_dir = BUGSINPY / "projects" / project / "bugs" / bug_id
    info = parse_info(bug_dir / "bug.info")
    # github_url 记在 project.info 里，不在 bug.info
    project_info = parse_info(BUGSINPY / "projects" / project / "project.info")
    repo_url = info.get("github_url") or project_info.get("github_url", "")
    if not repo_url:
        raise SystemExit(f"没找到 {project} 的 github_url")
    test_cmd = (bug_dir / "run_test.sh").read_text(encoding="utf-8").strip()
    patch = (bug_dir / "bug_patch.txt").read_text(encoding="utf-8")

    print("=" * 78)
    print(f"项目 {project} / bug {bug_id}")
    print("=" * 78)
    print(f"  仓库               {repo_url}")
    for key in ("python_version", "buggy_commit_id", "fixed_commit_id", "test_file"):
        print(f"  {key:<18} {info.get(key, '?')}")
    print(f"  run_test.sh        {test_cmd}")
    print(f"  补丁长度           {len(patch)} 字符")
    print()

    # ---------- 准备仓库（每次都从零开始，保证 buggy 版本是干净的）----------
    WORK.mkdir(parents=True, exist_ok=True)
    repo = WORK / project
    if repo.exists():
        run(["git", "reset", "--hard", "--quiet"], cwd=repo, quiet=True)
        run(["git", "clean", "-fdq"], cwd=repo, quiet=True)
        shutil.rmtree(repo, ignore_errors=True)
    if repo.exists():
        raise SystemExit(f"无法清理旧工作区：{repo}")
    cloned = run(["git", "clone", "--quiet", repo_url, str(repo)], quiet=True)
    if not (repo / ".git").exists():
        raise SystemExit(f"克隆失败：{repo_url}\n{cloned.stderr}")

    print(f"[1/4] 检出 buggy commit {info['buggy_commit_id'][:8]}")
    run(["git", "checkout", "--quiet", info["buggy_commit_id"]], cwd=repo, check=True)
    # 硬重置：克隆目录若被复用，上一轮 application 的补丁会残留，
    # 导致"buggy 版本"里跑的其实是修复后的代码——这一坑真实踩过。
    run(["git", "reset", "--hard", "--quiet", "HEAD"], cwd=repo, check=True)
    run(["git", "clean", "-fdq"], cwd=repo, quiet=True)
    dirty = run(["git", "status", "--short"], cwd=repo, quiet=True).stdout.strip()
    print(f"  工作区状态：{'干净' if not dirty else '⚠ 仍有改动：' + dirty}")

    # 关键一步：用数据库里记录的测试文件覆盖仓库里的版本。
    # BugsInPy 的 checkout 命令会做这件事，我早先漏了它，结果目标测试在 buggy 版本上
    # 也照常通过——看起来像"bug 修好了"，实际是测的根本不是暴露该 bug 的那份测试。
    recorded_tests = bug_dir / "tests"
    overwritten = []
    if recorded_tests.is_dir():
        for source in recorded_tests.rglob("*"):
            if not source.is_file():
                continue
            relative = source.relative_to(recorded_tests)
            target = repo / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            overwritten.append(str(relative))
    print(f"  用数据库记录的测试覆盖仓库版本：{overwritten or '（该 bug 未记录测试文件）'}")

    print(f"\n[1.5/4] 准备 Python 环境（{info.get('python_version', '?')} → 用 3.9 兼容）")
    venv = WORK / "venv"
    if not venv.exists():
        run(["uv", "venv", "--python", "3.9", str(venv)], check=True)
    run(["uv", "pip", "install", "--python", str(venv / "bin" / "python"), "pytest<9", "setuptools", "wheel"],
        quiet=True)
    # 被测包自身（这些项目多为纯 Python，可开发模式安装）
    install = run([str(venv / "bin" / "python"), "-m", "pip", "install", "-e", ".", "--no-build-isolation"],
                  cwd=repo, quiet=True)
    if install.returncode != 0:
        print("  pip install -e . 失败，尝试 setup.py develop")
        run([str(venv / "bin" / "python"), "setup.py", "develop", "-q"], cwd=repo, quiet=True)
    env = make_env(venv / "bin")
    print(f"  venv: {venv}")
    print(f"  python: {run([str(venv/'bin'/'python'), '--version'], quiet=True).stdout.strip()}")

    print(f"\n[2/4] 在 buggy 版本上运行目标测试（期望：失败，且不是命令找不到）")
    first = run(test_cmd, cwd=repo, env=env)
    buggy_failed = first.returncode not in (0, 127)
    print(f"  → 退出码 {first.returncode}　"
          f"{'符合预期（失败）' if buggy_failed else '⚠ 无效：命令没跑起来或未复现'}")

    print(f"\n[3/4] 应用官方补丁")
    patch_file = WORK / "bug_patch.txt"
    patch_file.write_text(patch, encoding="utf-8")
    applied = run(["git", "apply", "--verbose", str(patch_file)], cwd=repo)
    if applied.returncode != 0:
        print("  git apply 失败，改用 patch 命令重试")
        applied = run(["patch", "-p1", "--forward", "-i", str(patch_file)], cwd=repo)
    print(f"  → {'补丁已应用' if applied.returncode == 0 else '⚠ 补丁应用失败'}")

    print(f"\n[4/4] 在修复版本上运行同一测试（期望：通过）")
    second = run(test_cmd, cwd=repo, env=env)
    fixed_passed = second.returncode == 0
    print(f"  → 退出码 {second.returncode}　{'符合预期（通过）' if fixed_passed else '⚠ 未通过'}")

    print("\n" + "=" * 78)
    print("结论")
    print("=" * 78)
    if buggy_failed and fixed_passed:
        print("  ✅ F2P 机制可用：buggy 失败、fixed 通过。")
        print("     说明这台机器能搭建该项目的复现环境并对它做 F2P 判定。")
        print(f"     工作区留存在 {repo}")
        return 0
    print(f"  ❌ F2P 不可用：buggy_failed={buggy_failed}  fixed_passed={fixed_passed}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
