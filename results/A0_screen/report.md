# 测试生成 Agent 评测结果

## 主表

| Variant | All-Pass | Import OK | Line Cov. | Mutation | n(mut) | Turns | Tokens | Runtime |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| A0 | 100.0% | 100.0% | 100.0% ± 0.0% | 93.8% ± 12.8% | 117 | 6.7 | 38,195 | 54.5s |

## A0：质量–预算曲线

| Checkpoint | n | 已产出测试 | All-Pass | Line Cov. |
|---:|---:|---:|---:|---:|
| 1 turn | 134 | 0.0% | 0.0% | 0.0% |
| 2 turn | 134 | 92.5% | 43.3% | 91.8% |
| 4 turn | 134 | 99.3% | 73.1% | 98.5% |
| 8 turn | 81 | 100.0% | 96.3% | 100.0% |

### 状态分布（ITT：全部计入分母）

| Variant | all_pass | max_turns |
|---|---|---|
| A0 | 133 | 1 |

### 失败分类

- `all_pass`（133）：HumanEval/1, HumanEval/100, HumanEval/101, HumanEval/102, HumanEval/104, HumanEval/105, HumanEval/106, HumanEval/107, HumanEval/108, HumanEval/11, HumanEval/110, HumanEval/111, HumanEval/112, HumanEval/113, HumanEval/115, HumanEval/116, HumanEval/118, HumanEval/119, HumanEval/12, HumanEval/121, HumanEval/122, HumanEval/123, HumanEval/124, HumanEval/126, HumanEval/127, HumanEval/128, HumanEval/129, HumanEval/13, HumanEval/130, HumanEval/132, HumanEval/133, HumanEval/134, HumanEval/135, HumanEval/137, HumanEval/138, HumanEval/139, HumanEval/14, HumanEval/140, HumanEval/141, HumanEval/143, HumanEval/144, HumanEval/145, HumanEval/146, HumanEval/148, HumanEval/149, HumanEval/15, HumanEval/150, HumanEval/151, HumanEval/152, HumanEval/154, HumanEval/155, HumanEval/156, HumanEval/157, HumanEval/159, HumanEval/160, HumanEval/161, HumanEval/162, HumanEval/163, HumanEval/17, HumanEval/18, HumanEval/19, HumanEval/2, HumanEval/20, HumanEval/22, HumanEval/23, HumanEval/24, HumanEval/25, HumanEval/26, HumanEval/28, HumanEval/29, HumanEval/3, HumanEval/30, HumanEval/31, HumanEval/33, HumanEval/34, HumanEval/35, HumanEval/36, HumanEval/37, HumanEval/39, HumanEval/4, HumanEval/40, HumanEval/41, HumanEval/42, HumanEval/44, HumanEval/45, HumanEval/46, HumanEval/47, HumanEval/48, HumanEval/50, HumanEval/51, HumanEval/52, HumanEval/53, HumanEval/55, HumanEval/56, HumanEval/57, HumanEval/58, HumanEval/59, HumanEval/6, HumanEval/61, HumanEval/62, HumanEval/63, HumanEval/64, HumanEval/66, HumanEval/67, HumanEval/68, HumanEval/69, HumanEval/7, HumanEval/70, HumanEval/72, HumanEval/73, HumanEval/74, HumanEval/75, HumanEval/77, HumanEval/78, HumanEval/79, HumanEval/8, HumanEval/80, HumanEval/81, HumanEval/83, HumanEval/84, HumanEval/85, HumanEval/86, HumanEval/88, HumanEval/89, HumanEval/9, HumanEval/90, HumanEval/91, HumanEval/93, HumanEval/94, HumanEval/95, HumanEval/96, HumanEval/97, HumanEval/99
- `max_turns`（1）：HumanEval/117
