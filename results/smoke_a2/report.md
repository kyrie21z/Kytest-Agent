# 测试生成 Agent 评测结果

## 主表

| Variant | All-Pass | Import OK | Line Cov. | Mutation | n(mut) | Turns | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A2 | 100.0% | 100.0% | 100.0% ± 0.0% | 100.0% ± 0.0% | 1 | 5.0 | 25,239 | 83.8s |

## A2：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 1 | 0.0% | 0.0% | 0.0% |
| 2 turn | 1 | 100.0% | 0.0% | 100.0% |
| 4 turn | 1 | 100.0% | 0.0% | 100.0% |
| 8 turn | 1 | 100.0% | 100.0% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass |
|---|---|
| A2 | 1 |

### 失败分类

- `all_pass`（1）：HumanEval/1
