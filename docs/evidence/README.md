# 统计复核数据

`mbpp.csv` 保留 20 题 × 3 配置 × 3 次生成，共 180 行。它与档案中的原派生 CSV 字节相同；`expected.json` 保留来源哈希、完整任务成员、预设比较和统计结果。

在项目根目录运行 `python scripts/verify_evaluation.py`，成功输出 `all_matches: true`。此检查不调用模型，不重放全部被测程序，也不能独立认证模型服务身份或账单。

原始记录路径相对于[固定开发档案](https://github.com/kyrie21z/Kytest-Agent/tree/development-archive-20261008)。指标、统计单位与限制见[评价说明](../evaluation.md)。
