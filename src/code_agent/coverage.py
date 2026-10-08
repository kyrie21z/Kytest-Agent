"""Coverage collection shared by feedback, evaluation and browser adapters."""
from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Callable, Optional, Sequence

from .proc import ProcResult


@dataclass
class CoverageResult:
    execution: ProcResult
    target: Optional[dict] = None
    error: str = ""


def collect_coverage(workspace: Path, target: str, execute: Callable, *,
                     command: Sequence[str], timeout: float,
                     export_timeout: float = 120, export_if: Optional[Callable] = None) -> CoverageResult:
    """Collect one report; callers select commands and whether failed tests may export.

    execute(argv, timeout) returns ProcResult using the adapter's interpreter,
    environment and execution permissions. Metrics and feedback formatting stay
    with the caller.
    """
    workspace = Path(workspace).resolve()
    report_path = workspace / ".coverage.json"
    for path in (workspace / ".coverage", report_path):
        path.unlink(missing_ok=True)
    result = CoverageResult(execute(command, timeout))
    if export_if is not None and not export_if(result.execution):
        result.error = "coverage 执行超时或测试未通过"
        return result
    exported = execute([command[0], "-m", "coverage", "json", "-o", str(report_path),
                        "--pretty-print"], export_timeout)
    if exported.timed_out or exported.exit_code != 0:
        result.error = "coverage JSON 导出失败：" + (exported.error or exported.stderr or exported.stdout)[-300:]
        return result
    if not report_path.is_file() or report_path.is_symlink() or report_path.stat().st_size > 200_000:
        result.error = "coverage 未生成有效报告"
        return result
    try:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        wanted = target.replace("\\", "/")
        result.target = next((value for name, value in payload.get("files", {}).items()
                              if name.replace("\\", "/") == wanted or
                              name.replace("\\", "/").endswith("/" + wanted)), None)
        if result.target is None:
            result.error = f"coverage 报告里没有 {target}"
    except (OSError, ValueError, AttributeError) as exc:
        result.error = f"coverage 报告解析失败：{exc}"
    return result
