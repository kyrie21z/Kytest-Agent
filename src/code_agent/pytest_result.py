"""Shared pytest observations from captured process output, before display truncation.

Summary and node recognition are text heuristics, not authenticated pytest events.
Invocation settings, contract guards and mutation scoring belong to the callers.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field

from .proc import ProcResult

_COUNT = r"(\d+)\s+(passed|failed|errors?|skipped|xfailed|xpassed|warnings?|deselected|reruns?)\b"
_SUMMARY = re.compile(
    rf"(?:{_COUNT}(?:,\s*{_COUNT})*|no tests ran)\s+in\s+\d+(?:\.\d+)?s(?:\s+\([\d:]+\))?",
    re.I,
)
_ANSI = re.compile(r"\x1b\[[0-9;]*m")
_NODE = re.compile(r"^(PASSED|FAILED|ERROR)\s+(\S+)")


@dataclass
class PytestResult:
    process: ProcResult = field(default_factory=ProcResult)
    passed: int = 0
    failed: int = 0
    errors: int = 0
    skipped: int = 0
    summary_line: str = ""
    passed_nodes: list[str] = field(default_factory=list)
    failure_nodes: list[str] = field(default_factory=list)
    failure_lines: list[str] = field(default_factory=list)
    failure_in_solution: bool = False

    @property
    def counts(self) -> dict[str, int]:
        return {"passed": self.passed, "failed": self.failed,
                "errors": self.errors, "skipped": self.skipped}

    @property
    def complete(self) -> bool:
        """A normal exit and a recognized summary from untruncated capture."""
        p = self.process
        return (p.exit_code is not None and p.error is None and not p.timed_out
                and not p.output_truncated and bool(self.summary_line))

    @property
    def all_pass(self) -> bool:
        return (self.complete and self.process.exit_code == 0 and self.passed > 0
                and self.failed == 0 and self.errors == 0)

    @property
    def import_ok(self) -> bool:
        return self.complete and self.errors == 0 and self.passed + self.failed + self.skipped > 0

    def to_dict(self) -> dict:
        """Measurement record; raw output remains available on process."""
        p = self.process
        return {**self.counts, "ran": p.exit_code is not None or p.timed_out,
                "returncode": p.exit_code, "timed_out": p.timed_out,
                "duration_sec": p.duration_sec, "summary_line": self.summary_line,
                "passed_nodes": self.passed_nodes, "failure_nodes": self.failure_nodes,
                "failure_in_solution": self.failure_in_solution,
                "output_truncated": p.output_truncated, "execution_error": p.error,
                "all_pass": self.all_pass, "import_ok": self.import_ok}


def parse_pytest_result(process: ProcResult | None) -> PytestResult:
    """Recognize the final whole summary line; never accumulate earlier summaries.

    No summary means unknown counts, not proof that zero tests executed. A rejected
    tool call has no process; a timeout or truncated capture cannot establish a pass.
    Node evidence is returned only when the command actually emitted it (e.g. -rA).
    """
    result = PytestResult(process=process if process is not None else ProcResult())
    text = _ANSI.sub("", result.process.stdout + "\n" + result.process.stderr)
    for line in text.splitlines():
        line = line.strip()
        summary = line.strip("= ").strip()
        if _SUMMARY.fullmatch(summary):
            result.summary_line = summary
            counts = dict.fromkeys(result.counts, 0)
            for number, name in re.findall(_COUNT, summary, re.I):
                name = name.lower()
                if name in ("error", "errors"):
                    name = "errors"
                if name in counts:
                    counts[name] = int(number)
            result.passed, result.failed, result.errors, result.skipped = counts.values()
        node = _NODE.match(line)
        if node:
            tag, name = node.groups()
            if tag == "PASSED":
                result.passed_nodes.append(name)
            else:
                result.failure_nodes.append(name)
                result.failure_lines.append(line)
    result.failure_in_solution = bool(re.search(
        r'(?:^|[/\\\s"])solution\.py(?::\d+|"?, line \d+)', text, re.M))
    return result
