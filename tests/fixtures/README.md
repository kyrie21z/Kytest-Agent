# 工程回归样本

`humaneval.jsonl` 是既有 HumanEval+ 发布包中的 30 例固定子集，字节保持不变，仅用于离线加载、参考测试与故障池回归。它不构成当前模型质量成绩。

来源：EvalPlus / HumanEval；原有来源说明标注 Apache-2.0（EvalPlus）与 MIT（HumanEval）。完整来源、选取规则及说明见[档案](https://github.com/kyrie21z/Kytest-Agent/blob/development-archive-20261008/benchmarks/DATASET.md)。`official_tests` 保留原 HumanEval 的 `check(candidate)`，不含 EvalPlus 增强输入。

样本每行是一个 JSON 对象，包含 `instance_id`、`prompt`、`solution`、`entry_point`、`official_tests`，可选 `contract`。`prompt` 与 `solution` 拼接为完整源码；参考测试通过 `check(candidate)` 调用目标函数。数据加载器不访问网络，格式错误立即报告。
