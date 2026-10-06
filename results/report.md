# 测试生成 Agent 评测结果

## 主表

| Variant | All-Pass | Import OK | Line Cov. | Mutation | n(mut) | Turns | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 93.3% | 100.0% | 100.0% ± 0.0% | 91.5% ± 16.2% | 28 | 6.6 | 43,156 | 89.2s |
| *官方测试（baseline）* | 93.3% | 100.0% | 97.5% ± 13.7% | 91.6% ± 17.7% | 28 | 0.0 | 0 | 9.3s |

> 官方测试（HumanEval+ 自带测试）在同一套测量下的成绩，作为最强对照锚点。

## A0：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 30 | 0.0% | 0.0% | 0.0% |
| 2 turn | 30 | 86.7% | 36.7% | 86.7% |
| 4 turn | 30 | 100.0% | 66.7% | 100.0% |
| 8 turn | 20 | 100.0% | 90.0% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | max_turns | partial_pass |
|---|---|---|---|
| A0 | 25 | 3 | 2 |

### 失败分类

- `all_pass`（25）：HumanEval/10, HumanEval/103, HumanEval/109, HumanEval/114, HumanEval/120, HumanEval/125, HumanEval/131, HumanEval/136, HumanEval/142, HumanEval/153, HumanEval/158, HumanEval/16, HumanEval/21, HumanEval/27, HumanEval/32, HumanEval/43, HumanEval/49, HumanEval/5, HumanEval/54, HumanEval/60, HumanEval/65, HumanEval/71, HumanEval/87, HumanEval/92, HumanEval/98
- `max_turns`（3）：HumanEval/147, HumanEval/76, HumanEval/82
- `partial_pass`（2）：HumanEval/0, HumanEval/38
