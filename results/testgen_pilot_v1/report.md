# 环境诊断：不可用于机制比较

A0 generic python resolved to system Miniconda without pytest; A4 used the explicit virtualenv interpreter. Entire v1 is environmental diagnosis, not evidence of a mechanism effect. All 30 records and original source are retained.

本轮全部记录保留；不得用于质量优势结论或进入独立评测的决定。

# A4 开发试验结果

开发池五例，每条件每例3次。所有run计入；无效套件的有效杀伤率为0。

| 条件 | runs | all-pass | 有效杀伤率 | token均值 | 生成秒数 |
|---|---:|---:|---:|---:|---:|
| A0 | 15 | 66.7% | 66.7% | 30625 | 43.3 |
| A4 | 15 | 100.0% | 100.0% | 28261 | 50.2 |

完整：True；A4−A0平均有效杀伤率：0.33333333333333337；进入独立评测候选：False。

仅支持开发池上的观察；不能证明总体质量收益。等价变异体未自动排除。

逐实例重复均值、波动、拒绝数量及原始记录见 pilot_summary.json 和 repeat_*。
