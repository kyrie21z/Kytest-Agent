# 提交证据

formal_v1.csv含100行，paired_v2.csv含180行；这些是从冻结原件导出的最小派生行，
不是原始模型响应。每行带原件路径和SHA-256；expected.json带源报告和CSV哈希。
python scripts/reproduce_submission.py重新核对成员、固定分母、均值和配对统计。

real_run/保留MBPP/127 repeat_2 A5的完整请求/响应、工具事件、原始结果及最终套件。
它是专门用于展示反馈闭环的案例：独立检出2/3到3/3；不是随机代表样本，不替代
全部180次的总体比较。公开MBPP的预训练接触未知。solution.py来自冻结数据。

最新完整重放主分数180/180一致，参考和变异状态179/180一致；严格回执未通过。
唯一差异是A0/MBPP/71 repeat_1的随机大列表揭示上游参考排序缺陷，原始0分保留。
完整原件、严格失败回执和固定种子诊断见精简前Git版本，不能把派生统计重现
称为全部程序重放成功。

ui-comparison.json保存新版A0/A4界面的脚本机制演示与浏览器验收。
两组最终测试相同；A4含刻意错误候选，真实验证器记录失败、拒绝和修正。
ui-run.json、ui-acceptance.json保留上一版真实模型展示回执，其旧视频和截图可在
[a7f07fc归档](https://github.com/kyrie21z/Kytest-Agent/tree/a7f07fc1eae646f9a81583187c58eff7cafe57ef/docs)核对。
