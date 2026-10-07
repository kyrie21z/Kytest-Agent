"""评测层：测量 Agent 产出的测试质量。

**这个包必须位于 Agent 工作区之外。** 评测器是测量仪器，一旦 Agent 能读到它，
或者能读到它使用的 ground truth，实验就不再成立。

模块划分：

- `dataset.py`  实例加载（冻结的 HumanEval+ 子集）
- `workspace.py` 工作区准备（Agent 只能看到 solution.py）
- `metrics.py`  测量：pytest 可通过性 + 覆盖率 + 变异杀伤率
- `runner.py`   批量运行（并发、超时、断点续跑、结构化结果）
- `report.py`   汇总成主表与质量–预算曲线

指标定义以 `docs/evaluation-protocol.md` 为唯一口径。本包不定义指标，只实现它。
"""

from .dataset import Instance, load_dataset
from .metrics import Metrics, collect_metrics, run_pytest_on

__all__ = [
    "Instance",
    "Metrics",
    "collect_metrics",
    "load_dataset",
    "run_pytest_on",
]
