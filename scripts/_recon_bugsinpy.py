#!/usr/bin/env python3
"""侦察 BugsInPy：找出依赖最干净、最适合先跑通的项目。

不修改任何数据，只读 bug.info / requirements.txt / setup.sh / run_test.sh。
"""
import re
from pathlib import Path

ROOT = Path.home() / "bugs" / "BugsInPy" / "projects"


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace").strip()
    except OSError:
        return ""


def parse_info(path: Path) -> dict:
    fields = {}
    for line in read(path).splitlines():
        match = re.match(r'(\w+)\s*=\s*"?(.*?)"?\s*$', line)
        if match:
            fields[match.group(1)] = match.group(2)
    return fields


def main() -> int:
    rows = []
    for project in sorted(ROOT.iterdir()):
        if not project.is_dir():
            continue
        bugs_dir = project / "bugs"
        if not bugs_dir.is_dir():
            continue
        bug_ids = sorted(bugs_dir.iterdir(), key=lambda p: int(p.name) if p.name.isdigit() else 0)
        if not bug_ids:
            continue

        first = bug_ids[0]
        info = parse_info(first / "bug.info")
        requirements = [
            line.strip()
            for line in read(first / "requirements.txt").splitlines()
            if line.strip() and not line.strip().startswith("#")
        ]
        rows.append(
            {
                "project": project.name,
                "bugs": len(bug_ids),
                "python": info.get("python_version", "?"),
                "deps": requirements,
                "setup": read(first / "setup.sh").replace("\n", " ; "),
                "test": read(first / "run_test.sh").replace("\n", " ; "),
            }
        )

    rows.sort(key=lambda r: (len(r["deps"]), r["bugs"]))
    print(f"共 {len(rows)} 个项目\n")
    for row in rows:
        print(f"{row['project']:<14} bugs={row['bugs']:<3} py={row['python']:<8} deps={len(row['deps'])}")
        if row["deps"]:
            for dep in row["deps"][:6]:
                print(f"                 - {dep}")
        else:
            print("                 (requirements.txt 为空)")
        print(f"                 setup: {row['setup'][:90]}")
        print(f"                 test : {row['test'][:90]}")

    print("\n=== 依赖最少的三个项目的完整信息 ===")
    for row in rows[:3]:
        print(f"\n########## {row['project']}（{row['bugs']} 个 bug，python {row['python']}）")
        print(f"  依赖: {row['deps'] or '无'}")
        print(f"  setup: {row['setup']}")
        print(f"  test : {row['test']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
