"""代码静态分析工具：语法检查、AST 坏味道扫描、复杂度与规模度量。

这些工具让 Agent 在"审查代码"时先获得客观事实（语法是否通过、哪些行有坏味道、
复杂度多高），再由 LLM 结合上下文给出主观判断，避免纯靠模型"幻觉"。
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

from .base import Tool, ToolResult, resolve_workspace_path

MAX_LINE_LENGTH = 120
MAX_FUNCTION_LINES = 50
MAX_COMPLEXITY = 10
MAX_ARGUMENTS = 5
MAX_NESTING = 4
MAX_ISSUES = 60
MUTABLE_DEFAULT_TYPES = (ast.List, ast.Dict, ast.Set)


@dataclass
class Issue:
    line: int
    level: str  # E: 错误 / W: 警告 / I: 提示
    message: str

    def render(self) -> str:
        return f"  L{self.line}: [{self.level}] {self.message}"


@dataclass
class FunctionMetric:
    name: str
    line: int
    end_line: int
    complexity: int
    arguments: int
    nesting: int

    @property
    def length(self) -> int:
        return max(0, self.end_line - self.line + 1)


def _read_source(target: Path) -> str:
    return target.read_text(encoding="utf-8", errors="replace")


def _used_names(tree: ast.AST) -> Set[str]:
    """收集代码中实际使用到的名字（近似判断未使用导入）。"""
    used: Set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            used.add(node.id)
        elif isinstance(node, ast.Attribute):
            current: Any = node
            while isinstance(current, ast.Attribute):
                current = current.value
            if isinstance(current, ast.Name):
                used.add(current.id)
    return used


def _complexity(node: ast.AST) -> int:
    """近似计算圈复杂度，统计分支节点；不进入嵌套函数/类。"""
    score = 1

    def visit(current: ast.AST) -> None:
        nonlocal score
        for child in ast.iter_child_nodes(current):
            if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                continue
            if isinstance(child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.IfExp)):
                score += 1
            elif isinstance(child, ast.BoolOp):
                score += max(0, len(child.values) - 1)
            elif isinstance(child, ast.comprehension):
                score += len(child.ifs)
            visit(child)

    visit(node)
    return score


def _max_nesting(node: ast.AST, current: int = 0) -> int:
    """计算最大嵌套深度（不进入嵌套函数/类）。"""
    best = current
    for child in ast.iter_child_nodes(node):
        if isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            continue
        bump = isinstance(
            child, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)
        )
        best = max(best, _max_nesting(child, current + (1 if bump else 0)))
    return best


def _iter_functions(tree: ast.AST, prefix: str = ""):
    for node in tree.body if isinstance(tree, ast.Module) else ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield prefix + node.name, node
        elif isinstance(node, ast.ClassDef):
            for name, function in _iter_functions(node, prefix=f"{node.name}."):
                yield name, function


def _scan_issues(tree: ast.AST, source: str) -> List[Issue]:
    """基于 AST 的确定性静态检查，只报告高置信度问题。"""
    issues: List[Issue] = []
    lines = source.splitlines()

    # 1) 未使用的导入
    used = _used_names(tree)
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = (alias.asname or alias.name).split(".")[0]
                if name not in used:
                    issues.append(Issue(node.lineno, "W", f"导入 `{name}` 后未使用，建议删除"))
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                if alias.name == "*":
                    issues.append(Issue(node.lineno, "W", "使用了 `from ... import *`，会污染命名空间，建议改为显式导入"))
                    continue
                name = alias.asname or alias.name
                if name not in used:
                    issues.append(Issue(node.lineno, "W", f"导入 `{name}` 后未使用，建议删除"))

    # 2) 异常处理
    for node in ast.walk(tree):
        if isinstance(node, ast.ExceptHandler):
            if node.type is None:
                issues.append(Issue(node.lineno, "E", "裸 `except:` 会吞掉包括 KeyboardInterrupt 在内的所有异常，建议捕获具体异常类型"))
            elif node.body and all(isinstance(statement, ast.Pass) for statement in node.body):
                issues.append(Issue(node.lineno, "W", "`except ...: pass` 静默忽略异常，建议至少记录日志或返回错误"))
            if isinstance(node.type, ast.Name) and node.type.id == "Exception":
                issues.append(Issue(node.lineno, "I", "捕获过宽的 `Exception`，建议缩小异常类型范围"))

    # 3) 函数级问题
    for name, node in _iter_functions(tree):
        for default in list(node.args.defaults) + [d for d in node.args.kw_defaults if d is not None]:
            if isinstance(default, MUTABLE_DEFAULT_TYPES):
                issues.append(Issue(default.lineno, "E", f"函数 `{name}` 使用可变对象作为默认参数，多次调用会共享状态，建议改为 None 并在函数内初始化"))
                break
            if isinstance(default, ast.Call) and isinstance(default.func, ast.Name) and default.func.id in {"list", "dict", "set"}:
                issues.append(Issue(default.lineno, "E", f"函数 `{name}` 使用 `{default.func.id}()` 作为默认参数，会产生共享可变对象"))
                break
        arg_count = len(node.args.args) + len(node.args.kwonlyargs)
        if arg_count > MAX_ARGUMENTS:
            issues.append(Issue(node.lineno, "W", f"函数 `{name}` 参数过多（{arg_count} 个），建议拆分或使用参数对象"))
        complexity = _complexity(node)
        if complexity > MAX_COMPLEXITY:
            issues.append(Issue(node.lineno, "W", f"函数 `{name}` 圈复杂度过高（约 {complexity}），建议拆分逻辑"))
        nesting = _max_nesting(node)
        if nesting > MAX_NESTING:
            issues.append(Issue(node.lineno, "W", f"函数 `{name}` 嵌套过深（{nesting} 层），建议使用卫语句或提取函数"))

    # 4) 语句级问题
    for node in ast.walk(tree):
        if isinstance(node, ast.Compare):
            if any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops) and any(
                isinstance(comparator, ast.Constant) and comparator.value is None for comparator in node.comparators
            ):
                issues.append(Issue(node.lineno, "W", "与 None 比较建议使用 `is None` / `is not None`，而不是 `==` / `!=`"))
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in {"eval", "exec"}:
            issues.append(Issue(node.lineno, "E", f"使用 `{node.func.id}()` 执行动态代码存在安全风险，请确认输入可信"))
        if isinstance(node, ast.Assert):
            issues.append(Issue(node.lineno, "I", "`assert` 在 `python -O` 下会被移除，不应用于参数校验或业务逻辑"))
        if isinstance(node, ast.FunctionDef) and len(node.body) == 1 and isinstance(node.body[0], ast.Pass):
            issues.append(Issue(node.lineno, "I", f"函数 `{node.name}` 只有 `pass`，可能是未完成的占位实现"))

    # 5) 行级问题
    for number, line in enumerate(lines, start=1):
        if len(line) > MAX_LINE_LENGTH:
            issues.append(Issue(number, "I", f"该行长度 {len(line)} 超过 {MAX_LINE_LENGTH} 字符，建议换行"))
        stripped = line.strip()
        if stripped.startswith("#") and any(tag in stripped.upper() for tag in ("TODO", "FIXME", "XXX", "HACK")):
            issues.append(Issue(number, "I", "代码中存在待办标记，建议尽快处理并建立跟踪"))

    unique: Dict[Tuple[int, str, str], Issue] = {}
    for issue in issues:
        unique.setdefault((issue.line, issue.level, issue.message), issue)
    return sorted(unique.values(), key=lambda item: (item.line, item.level))[:MAX_ISSUES]


class CheckSyntaxTool(Tool):
    name = "check_syntax"
    description = (
        "检查 Python 文件的语法正确性，并进行 AST 静态扫描：未使用导入、裸 except、"
        "可变默认参数、None 比较、过深嵌套、复杂度过高等，返回问题清单（含行号）。"
    )
    parameters = {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "相对工作区的 Python 文件路径"}},
        "required": ["path"],
    }

    def run(self, path: str, **_: Any) -> ToolResult:
        target = resolve_workspace_path(self.workspace, path, must_exist=True)
        if target.is_dir():
            return ToolResult.failure(f"`{path}` 是目录，请指定具体文件")
        try:
            source = _read_source(target)
        except OSError as exc:
            return ToolResult.failure(f"读取文件失败：{exc}")

        relative = target.relative_to(self.workspace) if target.is_relative_to(self.workspace) else target
        total_lines = len(source.splitlines())
        try:
            tree = ast.parse(source, filename=str(target))
        except SyntaxError as exc:
            pointer = (exc.text or "").rstrip()
            return ToolResult.failure(
                f"语法错误：`{relative}` 第 {exc.lineno} 行第 {exc.offset} 列：{exc.msg}\n  {pointer}"
            )

        issues = _scan_issues(tree, source)
        if not issues:
            return ToolResult.success(
                f"语法检查通过：`{relative}`（共 {total_lines} 行）。AST 静态扫描未发现明显问题。"
            )
        errors = sum(1 for issue in issues if issue.level == "E")
        warnings = sum(1 for issue in issues if issue.level == "W")
        preview = "\n".join(issue.render() for issue in issues)
        return ToolResult.success(
            f"语法检查通过：`{relative}`（共 {total_lines} 行）。\n"
            f"AST 静态扫描发现 {len(issues)} 个问题（错误 {errors} / 警告 {warnings}）：\n{preview}"
        )


class AnalyzeCodeTool(Tool):
    name = "analyze_code"
    description = (
        "对 Python 文件做结构与规模统计：文件行数、函数/类数量、每个函数的长度、"
        "参数个数、圈复杂度、嵌套深度，并给出坏味道提示。适合快速了解陌生代码。"
    )
    parameters = {
        "type": "object",
        "properties": {"path": {"type": "string", "description": "相对工作区的 Python 文件路径"}},
        "required": ["path"],
    }

    def run(self, path: str, **_: Any) -> ToolResult:
        target = resolve_workspace_path(self.workspace, path, must_exist=True)
        if target.is_dir():
            return ToolResult.failure(f"`{path}` 是目录，请指定具体文件")
        source = _read_source(target)
        relative = target.relative_to(self.workspace) if target.is_relative_to(self.workspace) else target
        try:
            tree = ast.parse(source, filename=str(target))
        except SyntaxError as exc:
            return ToolResult.failure(f"无法解析 `{relative}`：第 {exc.lineno} 行存在语法错误 {exc.msg}")

        lines = source.splitlines()
        blank = sum(1 for line in lines if not line.strip())
        comment = sum(1 for line in lines if line.strip().startswith("#"))
        code = len(lines) - blank - comment
        classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
        functions: List[FunctionMetric] = []
        for name, node in _iter_functions(tree):
            functions.append(
                FunctionMetric(
                    name=name,
                    line=node.lineno,
                    end_line=getattr(node, "end_lineno", node.lineno),
                    complexity=_complexity(node),
                    arguments=len(node.args.args) + len(node.args.kwonlyargs),
                    nesting=_max_nesting(node),
                )
            )
        functions.sort(key=lambda item: item.line)

        smell: List[str] = []
        for metric in functions:
            if metric.length > MAX_FUNCTION_LINES:
                smell.append(f"  - `{metric.name}`（L{metric.line}）长度 {metric.length} 行，超过 {MAX_FUNCTION_LINES} 行")
            if metric.complexity > MAX_COMPLEXITY:
                smell.append(f"  - `{metric.name}`（L{metric.line}）圈复杂度约 {metric.complexity}，建议拆分")
            if metric.arguments > MAX_ARGUMENTS:
                smell.append(f"  - `{metric.name}`（L{metric.line}）参数 {metric.arguments} 个，建议使用参数对象")
            if metric.nesting > MAX_NESTING:
                smell.append(f"  - `{metric.name}`（L{metric.line}）嵌套 {metric.nesting} 层，建议使用卫语句")

        lines_out = [f"文件：`{relative}`"]
        lines_out.append(
            f"规模：总 {len(lines)} 行（代码 {code} / 注释 {comment} / 空行 {blank}），"
            f"函数 {len(functions)} 个，类 {len(classes)} 个。"
        )
        if functions:
            lines_out.append("函数清单（行号 | 长度 | 参数 | 复杂度 | 嵌套）：")
            for metric in functions:
                lines_out.append(
                    f"  {metric.line:>4} | {metric.length:>4} | {metric.arguments:>4} | "
                    f"{metric.complexity:>4} | {metric.nesting:>4}  {metric.name}"
                )
        lines_out.append("潜在坏味道：" if smell else "潜在坏味道：未发现明显问题。")
        lines_out.extend(smell)
        return ToolResult.success("\n".join(lines_out))