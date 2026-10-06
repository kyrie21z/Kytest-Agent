"""轻量 AST 变异引擎：评测层的主终点测量仪。

它回答的问题只有一个：**我们生成的测试，有没有能力区分"正确的程序"与"被改坏的
程序"？** 不需要知道所有输入的正确答案，因此绕开了 Oracle 问题。

为什么不直接用 `mutmut` / `cosmic-ray`：

- 它们面向"整个项目 + 完整 pytest 配置"，每杀一个变异体都要跑一遍项目初始化。
  我们需要的是**单个函数、每次几十个变异体、无配置**的快速测量。
- 评测要对 30 个实例 × 2 个变体做变异分析，工具本身的开销必须可忽略。
- 自研版本约 200 行，行为完全可预期，也便于在报告里逐算子解释。

变异算子（协议 §2.1 冻结）：

| 算子 | 变换 |
|---|---|
| AOR | `+`↔`-`，`*`↔`/`%` |
| ROR | `<`↔`<=`、`>`↔`>=`（翻转边界），`==`↔`!=` |
| LCR | `and`↔`or` |
| CRP | 常量 `0`↔`1` |
| BCR | 布尔字面量 `True`↔`False` |
| RVR | 函数体里的 `return <expr>` 换成 `return <expr 的替代常量>` |

选择规则是确定性的：按 (行号, 列号, 算子名) 字典序排序后取前 N 个。
不用随机数——否则同一份测试在两次评测里会得到不同的杀伤率。
"""
from __future__ import annotations

import ast
from dataclasses import dataclass
from typing import List, Optional, Sequence, Tuple

# 每个实例的变异体上限。协议 §2.1 冻结为 20：
# 它直接决定评测墙钟（每个变异体一次 pytest），也是"分辨率 vs 成本"的取舍点。
DEFAULT_MAX_MUTANTS = 20

_AOR = {
    ast.Add: ast.Sub,
    ast.Sub: ast.Add,
    ast.Mult: ast.Div,
    ast.Div: ast.Mult,
    ast.Mod: ast.Mult,
}
_ROR = {
    ast.Lt: ast.LtE,
    ast.LtE: ast.Lt,
    ast.Gt: ast.GtE,
    ast.GtE: ast.Gt,
    ast.Eq: ast.NotEq,
    ast.NotEq: ast.Eq,
}
_LCR = {ast.And: ast.Or, ast.Or: ast.And}


@dataclass(frozen=True)
class Mutant:
    """一个变异体。`source` 是完整的可导入模块源码，可直接写进 solution.py。"""

    mutant_id: str
    operator: str
    line: int
    column: int
    description: str
    source: str

    def to_dict(self) -> dict:
        return {
            "mutant_id": self.mutant_id,
            "operator": self.operator,
            "line": self.line,
            "column": self.column,
            "description": self.description,
        }


# ----------------------------------------------------------------------
# 候选收集
# ----------------------------------------------------------------------
def _kind_of(node: ast.AST) -> Optional[Tuple[str, str]]:
    """判断节点是否是变异目标，返回 (算子, 描述)。"""
    if isinstance(node, ast.BinOp) and type(node.op) in _AOR:
        return "AOR", f"{type(node.op).__name__} -> {_AOR[type(node.op)].__name__}"
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in _ROR:
        return "ROR", f"{type(node.ops[0]).__name__} -> {_ROR[type(node.ops[0])].__name__}"
    if isinstance(node, ast.BoolOp) and type(node.op) in _LCR:
        return "LCR", f"{type(node.op).__name__} -> {_LCR[type(node.op)].__name__}"
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        return "BCR", f"{node.value} -> {not node.value}"
    if isinstance(node, ast.Constant) and not isinstance(node.value, bool) and node.value in (0, 1):
        return "CRP", f"constant {node.value} -> {1 - int(node.value)}"
    if isinstance(node, ast.Return) and node.value is not None:
        replacement = _return_replacement(node.value)
        if replacement is not None:
            return "RVR", f"return <expr> -> return {replacement!r}"
    return None


def _walk_in_order(tree: ast.AST):
    """按 AST 广度优先顺序遍历。候选收集与变异定位必须用**同一个**顺序。"""
    for node in ast.walk(tree):
        yield node


def _candidates(tree: ast.AST) -> List[Tuple[int, int, int, str, str]]:
    """列出全部可变异点：(**遍历索引**, 行, 列, 算子, 描述)。

    遍历索引是定位用的唯一标识，必须与 `_walk_in_order` 完全同源。把它显式放进
    返回值，而不是让调用方自己 `enumerate`——后者得到的是"候选列表内的序号"，
    与遍历索引不是一回事，用它去变异必然改错节点或什么都改不到。
    这个混淆实际发生过：代价是每个实例只剩一个变异体，杀伤率失去分辨率。

    行号只用于报告与确定性排序，不参与定位。
    """
    found: List[Tuple[int, int, int, str, str]] = []
    for index, node in enumerate(_walk_in_order(tree)):
        kind = _kind_of(node)
        if kind is None:
            continue
        operator, description = kind
        found.append(
            (
                index,
                int(getattr(node, "lineno", 0) or 0),
                int(getattr(node, "col_offset", 0) or 0),
                operator,
                description,
            )
        )
    return found


def _return_replacement(value: ast.expr) -> Optional[object]:
    """给 return 表达式挑一个"看起来合理但可能错"的替代返回值。

    只有当 AST 能直接告诉我们该返回什么类型时才产生候选——盲目返回 None
    会让大量变异体因为类型错误而崩溃，失去区分意义。
    """
    if isinstance(value, ast.Constant):
        if isinstance(value.value, bool):
            return not value.value
        if isinstance(value.value, (int, float)):
            return value.value + 1
        return None
    if isinstance(value, ast.Compare):
        return True
    if isinstance(value, ast.BoolOp):
        return not isinstance(value.op, ast.And)
    return None


# ----------------------------------------------------------------------
# 变异体生成
# ----------------------------------------------------------------------
def _apply_mutation(node: ast.AST) -> bool:
    """就地修改该节点，成功返回 True。"""
    if isinstance(node, ast.BinOp) and type(node.op) in _AOR:
        node.op = _AOR[type(node.op)]()
        return True
    if isinstance(node, ast.Compare) and len(node.ops) == 1 and type(node.ops[0]) in _ROR:
        node.ops[0] = _ROR[type(node.ops[0])]()
        return True
    if isinstance(node, ast.BoolOp) and type(node.op) in _LCR:
        node.op = _LCR[type(node.op)]()
        return True
    if isinstance(node, ast.Constant) and isinstance(node.value, bool):
        node.value = not node.value
        return True
    if isinstance(node, ast.Constant) and not isinstance(node.value, bool) and node.value in (0, 1):
        node.value = 1 - int(node.value)
        return True
    if isinstance(node, ast.Return) and node.value is not None:
        replacement = _return_replacement(node.value)
        if replacement is not None:
            node.value = ast.Constant(value=replacement)
            return True
    return False


def _mutate_at(tree: ast.AST, index: int) -> bool:
    """变异第 `index` 个候选（按 `_candidates` 的同一顺序计数）。

    必须按索引精确定位，不能"改第一个能改的"：那样每次都会改同一个节点，
    生成的变异体全部重复，去重之后每个实例只剩一个变异体——杀伤率失去分辨率。
    这是实际发生过的缺陷。
    """
    for position, node in enumerate(_walk_in_order(tree)):
        if position != index:
            continue
        return _apply_mutation(node)
    return False


def default_operators() -> Sequence[str]:
    return ("AOR", "ROR", "LCR", "CRP", "BCR", "RVR")


def generate_mutants(
    source: str,
    *,
    max_mutants: int = DEFAULT_MAX_MUTANTS,
    operators: Optional[Sequence[str]] = None,
) -> List[Mutant]:
    """生成变异体。输入源码必须能解析，否则返回空列表。"""
    try:
        original = ast.parse(source)
    except SyntaxError:
        return []

    allowed = set(operators) if operators else set(default_operators())
    candidates = [item for item in _candidates(original) if item[3] in allowed]
    # 确定性抽样：按 (行, 列, 算子, 遍历索引) 排序后取前 N 个。
    # 不用随机数——否则同一份测试在两次评测里会得到不同的杀伤率。
    candidates.sort(key=lambda item: (item[1], item[2], item[3], item[0]))

    mutants: List[Mutant] = []
    seen_source: set = set()
    for index, line, column, operator, description in candidates:
        if len(mutants) >= max_mutants:
            break
        tree = ast.parse(source)  # 每次从原始 AST 重新出发，保证单点变异
        if not _mutate_at(tree, index):
            continue
        try:
            mutated = ast.unparse(tree) + "\n"
        except (AttributeError, ValueError):  # pragma: no cover - unparse 极少失败
            continue
        if mutated in seen_source:
            continue
        if _same_ast(mutated, source):
            # 变异在语义上与原程序等价，无法被任何测试杀死，必须剔除，
            # 否则会系统性地低估杀伤率。
            continue
        seen_source.add(mutated)
        mutants.append(
            Mutant(
                mutant_id=f"M{len(mutants) + 1}",
                operator=operator,
                line=line,
                column=column,
                description=description,
                source=mutated,
            )
        )
    return mutants


def _same_ast(left: str, right: str) -> bool:
    try:
        return ast.dump(ast.parse(left)) == ast.dump(ast.parse(right))
    except SyntaxError:
        return True  # 解析不了就当作等价，宁可少算也不少算


def mutation_summary(mutants: Sequence[Mutant]) -> dict:
    """按算子统计变异体数量，用于检查算子偏置。

    若不同变体之间的差异只来自某一种算子（例如覆盖率引导只让它更会写边界测试），
    这个分布就是发现该问题的第一手证据。
    """
    counts: dict = {}
    for mutant in mutants:
        counts[mutant.operator] = counts.get(mutant.operator, 0) + 1
    return counts
