# 历史运行派生结果（input-output-v1）

## 主表

| Variant | All-Pass | Import OK | Line Cov. | Mutation | n(mut) | Turns | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 95.0% | 95.0% | 95.0% ± 22.4% | 70.4% ± 17.6% | 20 | 5.8 | 25,079 | 142.0s |
| A1 | 90.0% | 90.0% | 90.0% ± 30.8% | 69.3% ± 19.2% | 20 | 6.0 | 34,034 | 209.4s |
| A2 | 95.0% | 95.0% | 95.0% ± 22.4% | 70.6% ± 21.3% | 20 | 3.1 | 14,830 | 155.5s |
| A3 | 90.0% | 90.0% | 90.0% ± 30.8% | 66.6% ± 23.4% | 20 | 3.2 | 12,770 | 194.8s |
| *官方测试锚点* | 100.0% | 100.0% | 100.0% ± 0.0% | 69.4% ± 14.6% | 20 | 0.0 | 0 | 0.0s |

> 官方测试（HumanEval+ 自带测试）在同一套测量下的成绩，作为最强对照锚点。

## A0：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 20 | 0.0% | 0.0% | 0.0% |
| 2 turn | 20 | 80.0% | 30.0% | 70.6% |
| 4 turn | 19 | 100.0% | 73.7% | 100.0% |
| 8 turn | 13 | 100.0% | 92.3% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | timeout |
|---|---|---|
| A0 | 19 | 1 |

### 失败分类

- `all_pass`（19）：HumanEval/123, HumanEval/128, HumanEval/129, HumanEval/13, HumanEval/137, HumanEval/146, HumanEval/148, HumanEval/149, HumanEval/151, HumanEval/159, HumanEval/163, HumanEval/25, HumanEval/31, HumanEval/39, HumanEval/57, HumanEval/59, HumanEval/75, HumanEval/90, HumanEval/96
- `timeout`（1）：HumanEval/44

## A1：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 20 | 0.0% | 0.0% | 0.0% |
| 2 turn | 20 | 95.0% | 35.0% | 85.0% |
| 4 turn | 18 | 100.0% | 66.7% | 100.0% |
| 8 turn | 12 | 100.0% | 91.7% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | max_turns | timeout |
|---|---|---|---|
| A1 | 17 | 1 | 2 |

### 失败分类

- `all_pass`（17）：HumanEval/128, HumanEval/129, HumanEval/13, HumanEval/137, HumanEval/146, HumanEval/148, HumanEval/149, HumanEval/151, HumanEval/159, HumanEval/163, HumanEval/25, HumanEval/31, HumanEval/57, HumanEval/59, HumanEval/75, HumanEval/90, HumanEval/96
- `max_turns`（1）：HumanEval/123
- `timeout`（2）：HumanEval/39, HumanEval/44

## A2：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 20 | 0.0% | 0.0% | 0.0% |
| 2 turn | 20 | 95.0% | 50.0% | 95.0% |
| 4 turn | 10 | 100.0% | 60.0% | 90.0% |
| 8 turn | 3 | 100.0% | 100.0% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | timeout |
|---|---|---|
| A2 | 19 | 1 |

### 失败分类

- `all_pass`（19）：HumanEval/128, HumanEval/129, HumanEval/13, HumanEval/137, HumanEval/146, HumanEval/148, HumanEval/149, HumanEval/151, HumanEval/159, HumanEval/163, HumanEval/25, HumanEval/31, HumanEval/39, HumanEval/44, HumanEval/57, HumanEval/59, HumanEval/75, HumanEval/90, HumanEval/96
- `timeout`（1）：HumanEval/123

## A3：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 20 | 0.0% | 0.0% | 0.0% |
| 2 turn | 20 | 90.0% | 35.0% | 80.0% |
| 4 turn | 11 | 90.9% | 72.7% | 90.9% |
| 8 turn | 3 | 66.7% | 66.7% | 66.7% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | timeout |
|---|---|---|
| A3 | 18 | 2 |

### 失败分类

- `all_pass`（18）：HumanEval/123, HumanEval/128, HumanEval/129, HumanEval/13, HumanEval/137, HumanEval/146, HumanEval/148, HumanEval/149, HumanEval/151, HumanEval/163, HumanEval/25, HumanEval/31, HumanEval/39, HumanEval/57, HumanEval/59, HumanEval/75, HumanEval/90, HumanEval/96
- `timeout`（2）：HumanEval/159, HumanEval/44
