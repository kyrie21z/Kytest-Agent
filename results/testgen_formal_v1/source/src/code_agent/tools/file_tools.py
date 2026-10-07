"""文件类工具：列目录、读文件、正则搜索、写文件。全部受工作区沙箱约束。"""
from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path
from typing import Any, Iterator, List

from .base import Tool, ToolResult, resolve_workspace_path

#: 扫描/搜索时跳过的目录
SKIP_DIRS = {
    ".git", ".hg", ".svn", "__pycache__", ".pytest_cache", ".mypy_cache",
    ".venv", "venv", "node_modules", ".idea", ".vscode", ".sessions",
    ".agent_tmp", ".tox", "dist", "build", ".next", ".cache", "coverage",
}

#: 已知的文本文件后缀
TEXT_SUFFIXES = {
    ".py", ".pyi", ".js", ".jsx", ".ts", ".tsx", ".java", ".go", ".rs", ".c", ".h",
    ".cpp", ".hpp", ".cs", ".rb", ".php", ".swift", ".kt", ".scala", ".sh", ".ps1",
    ".sql", ".html", ".css", ".scss", ".json", ".yaml", ".yml", ".toml", ".ini",
    ".cfg", ".md", ".txt", ".xml", ".gradle", ".m", ".r", ".lua", ".vue", ".env",
}


def _is_probably_text(path: Path) -> bool:
    if path.suffix.lower() in TEXT_SUFFIXES:
        return True
    try:
        with path.open("rb") as handle:
            chunk = handle.read(4096)
    except OSError:
        return False
    return b"\x00" not in chunk


def iter_files(root: Path, recursive: bool = True) -> Iterator[Path]:
    """遍历工作区内的文件，跳过常见依赖/缓存目录。"""
    if root.is_file():
        yield root
        return
    if recursive:
        for current, dirnames, filenames in os.walk(root):
            dirnames[:] = sorted(
                name for name in dirnames if name not in SKIP_DIRS and not name.startswith(".")
            )
            for filename in sorted(filenames):
                yield Path(current) / filename
    else:
        for entry in sorted(root.iterdir()):
            if entry.is_file():
                yield entry


def _relative(path: Path, workspace: Path) -> str:
    try:
        return str(path.relative_to(workspace)).replace("\\", "/")
    except ValueError:
        return str(path)


class ListFilesTool(Tool):
    name = "list_files"
    description = "列出工作区目录下的文件与子目录（自动跳过 .git、node_modules 等目录）。"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "相对工作区的目录路径，默认为当前目录 '.'"},
            "recursive": {"type": "boolean", "description": "是否递归列出子目录，默认 false"},
            "max_entries": {"type": "integer", "description": "最多返回多少条，默认 200"},
        },
        "required": [],
    }

    def __init__(self, settings: Any) -> None:
        super().__init__(settings.workspace)

    def run(self, path: str = ".", recursive: bool = False, max_entries: int = 200, **_: Any) -> ToolResult:
        target = resolve_workspace_path(self.workspace, path, must_exist=True)
        if target.is_file():
            return ToolResult.success(f"{_relative(target, self.workspace)}（这是一个文件，共 1 个）")
        try:
            limit = max(1, min(int(max_entries or 200), 1000))
        except (TypeError, ValueError):
            limit = 200

        entries: List[str] = []
        if recursive:
            for file_path in iter_files(target, recursive=True):
                entries.append(_relative(file_path, self.workspace))
                if len(entries) >= limit:
                    break
        else:
            for entry in sorted(target.iterdir(), key=lambda item: (item.is_file(), item.name.lower())):
                if entry.name.startswith(".") or entry.name in SKIP_DIRS:
                    continue
                suffix = "/" if entry.is_dir() else ""
                entries.append(_relative(entry, self.workspace) + suffix)
                if len(entries) >= limit:
                    break
        if not entries:
            return ToolResult.success(f"目录 `{_relative(target, self.workspace)}` 为空（或只包含被忽略的目录）。")
        lines = "\n".join(f"  {item}" for item in entries)
        note = f"\n（已达到 {limit} 条上限，结果被截断）" if len(entries) >= limit else ""
        return ToolResult.success(f"目录 `{_relative(target, self.workspace)}` 共列出 {len(entries)} 项：\n{lines}{note}")


class ReadFileTool(Tool):
    name = "read_file"
    description = (
        "读取工作区内文本文件的内容，返回带行号的代码，便于按行引用。"
        "可使用 start_line/end_line 只读取部分内容；"
        "超过大小上限的文件必须显式给出 start_line/end_line 做按行部分读取。"
    )
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "相对工作区的文件路径"},
            "start_line": {"type": "integer", "description": "起始行号（从 1 开始），默认 1"},
            "end_line": {"type": "integer", "description": "结束行号（含），默认 0 表示读到文件末尾"},
            "max_lines": {"type": "integer", "description": "最多返回行数，默认 400"},
        },
        "required": ["path"],
    }

    # 超限文件单次部分读取的字符预算（与总大小上限分开定义）。
    # 有界读取，内存占用受该预算、单次读取长度与 max_lines 约束。
    PARTIAL_READ_CHAR_BUDGET = 200_000
    # 单行截断阈值：防止单行超大文件（如压缩的 JSON）撑爆预算。
    _MAX_LINE_CHARS = 2_000

    def __init__(self, settings: Any) -> None:
        super().__init__(settings.workspace)
        self.max_file_bytes = int(settings.max_file_bytes)

    def run(
        self,
        path: str,
        start_line: int = 1,
        end_line: int = 0,
        max_lines: int = 400,
        **_: Any,
    ) -> ToolResult:
        target = resolve_workspace_path(self.workspace, path, must_exist=True)
        if target.is_dir():
            return ToolResult.failure(f"`{path}` 是一个目录，请改用 list_files 工具")
        size = target.stat().st_size
        try:
            start = max(1, int(start_line or 1))
        except (TypeError, ValueError):
            start = 1
        try:
            end = int(end_line or 0)
        except (TypeError, ValueError):
            end = 0

        if size > self.max_file_bytes:
            # 超限文件：整文件读取被拒绝；显式给出行区间或行数上限时做
            # **流式部分读取**，内存受单次读取预算与行数上限双重约束。
            # 两条上限分开定义：max_file_bytes 管"整文件读取"，
            # PARTIAL_READ_CHAR_BUDGET 管"单次部分读取"。
            try:
                requested_lines = int(max_lines)
            except (TypeError, ValueError):
                requested_lines = 400
            explicit_partial = start > 1 or end > 0 or requested_lines != 400
            if not explicit_partial:
                return ToolResult.failure(
                    f"文件过大（{size} 字节，上限 {self.max_file_bytes} 字节），无法整文件读取。"
                    "请显式传入 start_line/end_line 按行读取部分内容"
                    "（例如 start_line=1，end_line=100），或调整 MAX_FILE_BYTES 配置。"
                )
            return self._read_partial(target, start, end, requested_lines)

        if not _is_probably_text(target):
            return ToolResult.failure(f"`{path}` 看起来是二进制文件，无法作为文本读取")
        raw = target.read_text(encoding="utf-8", errors="replace")
        lines = raw.splitlines()
        total = len(lines)
        if end <= 0 or end > total:
            end = total
        if start > total:
            return ToolResult.failure(f"起始行 {start} 超出文件总行数 {total}")
        end = max(start, end)
        limit = max(1, min(int(max_lines or 400), 2000))
        shown_end = min(end, start + limit - 1)
        body = "\n".join(f"{number:>5}| {lines[number - 1]}" for number in range(start, shown_end + 1))
        notes = [f"文件 `{_relative(target, self.workspace)}` 共 {total} 行，显示第 {start}-{shown_end} 行："]
        if shown_end < end or shown_end < total:
            notes.append(f"提示：仍有未显示内容（可用 start_line/end_line 继续读取，例如 start_line={shown_end + 1}）。")
        return ToolResult.success("\n".join(notes) + "\n" + body)

    def _read_partial(self, target: Path, start: int, end: int, max_lines: int) -> ToolResult:
        """有界行读取；长行只保留前缀，余下部分按 64K 块排空。"""
        if end > 0 and end < start:
            return ToolResult.failure(f"end_line（{end}）不能小于 start_line（{start}）")
        limit = max(1, min(int(max_lines or 400), 2000))
        kept: List[str] = []
        used_chars = 0
        line_no = 0
        truncated_file = False
        try:
            with target.open("r", encoding="utf-8", errors="replace") as handle:
                while True:
                    piece = handle.readline(self._MAX_LINE_CHARS + 1)
                    if not piece:
                        break
                    line_no += 1
                    line = piece.rstrip("\r\n")
                    clipped = len(line) > self._MAX_LINE_CHARS
                    line = line[:self._MAX_LINE_CHARS]
                    # 不积累 pending；每个排空块都有长度上限。
                    while not piece.endswith("\n"):
                        piece = handle.readline(65_536)
                        if not piece:
                            break
                        clipped = True
                    if line_no < start:
                        continue
                    if clipped:
                        line += "…（本行过长已截断）"
                    remaining = self.PARTIAL_READ_CHAR_BUDGET - used_chars
                    rendered = f"{line_no:>5}| {line}"
                    if len(rendered) > remaining:
                        rendered = rendered[:remaining]
                        truncated_file = True
                    kept.append(rendered)
                    used_chars += len(rendered)
                    if end > 0 and line_no >= end:
                        break
                    if len(kept) >= limit or used_chars >= self.PARTIAL_READ_CHAR_BUDGET:
                        truncated_file = True
                        break
        except OSError as exc:
            return ToolResult.failure(f"读取失败：{exc}")

        if not kept:
            return ToolResult.failure(
                f"未读到内容：文件从第 {start} 行起已无更多行（或区间为空）。"
            )
        notes = [
            f"文件 `{_relative(target, self.workspace)}` 超过大小上限，已按行部分读取，"
            f"显示第 {start}-{start + len(kept) - 1} 行："
        ]
        if truncated_file:
            notes.append(
                "提示：本次读取达到行数或字符预算上限，后面可能还有内容"
                f"（可用 start_line={start + len(kept)} 继续读取）。"
            )
        return ToolResult.success("\n".join(notes) + "\n" + "\n".join(kept))


class SearchCodeTool(Tool):
    name = "search_code"
    description = "在工作区代码中按正则表达式搜索内容，返回 文件:行号: 内容，适合定位函数、变量或调用点。"
    parameters = {
        "type": "object",
        "properties": {
            "pattern": {"type": "string", "description": "要搜索的正则表达式或普通文本"},
            "path": {"type": "string", "description": "搜索范围（文件或目录），默认 '.'"},
            "file_glob": {"type": "string", "description": "文件名通配符过滤，例如 '*.py'，默认 '*'"},
            "ignore_case": {"type": "boolean", "description": "是否忽略大小写，默认 false"},
            "max_results": {"type": "integer", "description": "最多返回多少条匹配，默认 50"},
        },
        "required": ["pattern"],
    }

    def __init__(self, settings: Any) -> None:
        super().__init__(settings.workspace)
        self.max_file_bytes = int(settings.max_file_bytes)

    def run(
        self,
        pattern: str,
        path: str = ".",
        file_glob: str = "*",
        ignore_case: bool = False,
        max_results: int = 50,
        **_: Any,
    ) -> ToolResult:
        target = resolve_workspace_path(self.workspace, path, must_exist=True)
        flags = re.IGNORECASE if ignore_case else 0
        try:
            regex = re.compile(pattern, flags)
        except re.error:
            regex = re.compile(re.escape(pattern), flags)  # 非法正则时退化为字面量搜索
        try:
            limit = max(1, min(int(max_results or 50), 500))
        except (TypeError, ValueError):
            limit = 50

        matches: List[str] = []
        files = [target] if target.is_file() else list(iter_files(target, recursive=True))
        for file_path in files:
            if not fnmatch.fnmatch(file_path.name, file_glob or "*"):
                continue
            try:
                if file_path.stat().st_size > self.max_file_bytes or not _is_probably_text(file_path):
                    continue
                content = file_path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            for number, line in enumerate(content.splitlines(), start=1):
                if regex.search(line):
                    matches.append(f"{_relative(file_path, self.workspace)}:{number}: {line.strip()[:200]}")
                    if len(matches) >= limit:
                        break
            if len(matches) >= limit:
                break
        if not matches:
            return ToolResult.success(f"未找到与 `{pattern}` 匹配的内容（范围：{_relative(target, self.workspace)}）。")
        note = f"\n（已达到 {limit} 条上限，结果被截断）" if len(matches) >= limit else ""
        return ToolResult.success(f"找到 {len(matches)} 条匹配：\n" + "\n".join(f"  {item}" for item in matches) + note)


class WriteFileTool(Tool):
    name = "write_file"
    description = "把文本内容写入工作区内的文件（可用于生成代码、测试文件或修复补丁），默认不覆盖已存在文件。"
    parameters = {
        "type": "object",
        "properties": {
            "path": {"type": "string", "description": "相对工作区的目标文件路径"},
            "content": {"type": "string", "description": "要写入的完整文本内容"},
            "overwrite": {"type": "boolean", "description": "目标已存在时是否覆盖，默认 false"},
        },
        "required": ["path", "content"],
    }

    def __init__(self, settings: Any) -> None:
        super().__init__(settings.workspace)
        self.allow_write = bool(settings.allow_write)

    def run(self, path: str, content: str, overwrite: bool = False, **_: Any) -> ToolResult:
        if not self.allow_write:
            return ToolResult.failure("写入功能已被配置禁用（ALLOW_WRITE=false）")
        target = resolve_workspace_path(self.workspace, path)
        if target.exists() and not overwrite:
            return ToolResult.failure(
                f"文件 `{path}` 已存在。如确认覆盖，请显式传入 overwrite=true；或改用其他路径。"
            )
        if target.exists() and target.is_dir():
            return ToolResult.failure(f"`{path}` 是目录，不能作为文件写入")

        try:
            target.parent.mkdir(parents=True, exist_ok=True)
            text = content if isinstance(content, str) else str(content)
            target.write_text(text, encoding="utf-8")
        except OSError as exc:
            return ToolResult.failure(f"写入失败：{exc}")
        return ToolResult.success(
            f"已写入 `{_relative(target, self.workspace)}`（{len(text)} 字符，{len(text.splitlines())} 行）。"
            "建议随后用运行命令的方式验证该文件（例如执行 pytest）。"
        )
